import boto3
import os
import pandas as pd
from pytz import timezone
import hashlib
import requests
import json

# read keys in from environment variables
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
discord_webhook_url = os.getenv("WEBHOOK_URL")

region = 'us-east-2'

def download_file(bucket_name, file_name, path):

    s3_client = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    print(f"Downloading. bucket: {bucket_name}, file: {file_name}, path: {path}")
    s3_client.download_file(bucket_name, path, file_name)

def list_files(bucket_name, prefix, file_type='*'):
    
    s3 = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = s3.list_objects_v2(Bucket=bucket_name)

    files = []
    for obj in response.get('Contents', []):
        if file_type == '*':
            files.append(obj['Key'])
        elif obj['Key'].endswith(file_type):
            files.append(obj['Key'])

    return files

def list_files_paginated(bucket_name, prefix, file_type='*'):

    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects_v2')

    names = []
    
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if type(file_type) is list:
                for ft in file_type:
                    if key.endswith(ft):
                        names.append(key)
            elif file_type == '*' or key.endswith(file_type):
                # get presigned url
                names.append(key)

    return names

def get_s3_status():
    # Initialize SageMaker client
    sm = boto3.client("sagemaker", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    paginator = sm.get_paginator('list_processing_jobs')
    response_iterator = paginator.paginate(
        PaginationConfig={
            'MaxItems': 1000,
            'PageSize': 100,
        }
    )
    
    jobs = {'ProcessingJobSummaries': []}
    for page in response_iterator:
        if 'ProcessingJobSummaries' in page:
            jobs['ProcessingJobSummaries'] += page['ProcessingJobSummaries']

    jobs_df = pd.DataFrame(jobs['ProcessingJobSummaries'])
    jobs_df['hash_name'] = jobs_df['ProcessingJobName'].apply(lambda x: x.split('-')[1])
    jobs_df['CreationTime'] = pd.to_datetime(jobs_df['CreationTime'], utc=True)
    jobs_df['ProcessingEndTime'] = pd.to_datetime(jobs_df['ProcessingEndTime'], utc=True)
    jobs_df['LastModifiedTime'] = pd.to_datetime(jobs_df['LastModifiedTime'], utc=True)

    # Initialize S3 client
    s3 = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    # Check if the bucket is empty
    try:
        unprocessed_files = s3.list_objects_v2(Bucket="traffmind-client-unprocessed-jamar")
        status_df = pd.DataFrame(unprocessed_files['Contents'])
        status_df['hash_name'] = status_df['Key'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())
        status_df['LastModified'] = pd.to_datetime(status_df['LastModified'], utc=True)
        # keep key without extension
        status_df['Key'] = status_df['Key'].apply(lambda x: '.'.join(x.split('.')[:-1]))
    except KeyError:
        status_df = pd.DataFrame(columns=['Key', 'LastModified', 'hash_name'])
    
    # Check if the processed files exist
    try:
        processed_files = s3.list_objects_v2(Bucket="traffmind-client-processed-jamar")
        processed_files_df = pd.DataFrame(processed_files['Contents'])
        processed_files_df['file_path'] = processed_files_df['Key']

        processed_files_df['Key'] = processed_files_df['Key'].apply(lambda x: x.split('/')[1] if '/' in x else x)
        processed_files_df['extension'] = processed_files_df['Key'].apply(lambda x: x.split('.')[-1])
        # remove extension from Key
        processed_files_df = processed_files_df[processed_files_df['extension'].isin(['mp4', 'h264'])]
        processed_files_df['Key'] = processed_files_df['Key'].apply(lambda x: x.split('_2024-')[0])
        processed_files_df = processed_files_df[['Key', 'file_path']]

    except KeyError:
        processed_files_df = pd.DataFrame(columns=['Key', 'file_path'])
    
    try:
        # Merge DataFrames on hash_name
        merged_df = pd.merge(status_df, jobs_df, on='hash_name', how='left')
        time_difference = merged_df['LastModified'] - merged_df['CreationTime']
        merged_df = merged_df[time_difference.abs() <= pd.Timedelta(minutes=5)]

        # Calculate processing duration in hours and format datetime fields for EST
        merged_df['Duration (hrs)'] = ((merged_df['ProcessingEndTime'] - merged_df['CreationTime']).dt.total_seconds() / 3600).round(1)
        est = timezone('America/New_York')
        merged_df['CreationTime'] = merged_df['CreationTime'].dt.tz_convert(est).dt.strftime('%Y-%m-%d %I:%M %p')
        merged_df['ProcessingEndTime'] = merged_df['ProcessingEndTime'].dt.tz_convert(est).dt.strftime('%Y-%m-%d %I:%M %p')
        # merged_df['Key'] = merged_df['Key'].str.replace('.mp4', '', regex=False)
        # merged_df['Key'] = merged_df['Key'].str.replace('.h264', '', regex=False)
        merged_df = pd.merge(merged_df, processed_files_df, on='Key', how='left')
        # add download link if Status is Completed
        merged_df['Download Link'] = merged_df.apply(lambda x: generate_presigned_url("traffmind-client-processed-jamar", x['file_path']) if (x['ProcessingJobStatus'] == 'Completed' and type(x['file_path']) is str) else None, axis=1)

        # Rename columns and filter necessary fields
        merged_df = merged_df.rename(columns={'Key': 'File Name', 'CreationTime': 'Start Time', 'ProcessingEndTime': 'End Time', 'ProcessingJobStatus': 'Status'})
        merged_df = merged_df[['File Name', 'Start Time', 'End Time', 'Duration (hrs)', 'Status', 'Download Link']]
        merged_df.reset_index(drop=True, inplace=True)
        merged_df = merged_df.sort_values(by=['Status', 'End Time'], ascending=[True, False])
    except Exception as e:
        print(f"exception: {e}")
        merged_df = pd.DataFrame(columns=['File Name', 'Start Time', 'End Time', 'Duration (hrs)', 'Status', 'Download Link'])
        merged_df = merged_df.sort_values(by=['Status', 'End Time'], ascending=[True, False])
        # order by Status and End Time

    merged_df = merged_df.sort_values(by=['Start Time'], ascending=False)
    
    return merged_df


import boto3
from botocore.exceptions import ClientError
import logging

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object.

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response

def send_discord_notification(file_name, file_size_mb, title, description, color):
    webhook_url = discord_webhook_url  # Make sure to define your Discord webhook URL
    data = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "fields": [
                {"name": "File Name", "value": file_name, "inline": False},
                {"name": "Size", "value": f"{file_size_mb:.2f} MB", "inline": False}
            ],
            "footer": {
                "text": "Streamlit App Notification"
            }
        }],
        "username": "TraffMind AI"
    }
    response = requests.post(
        webhook_url, data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 204:
        raise Exception(f"Request to Discord returned an error {response.status_code}, the response is:\n{response.text}")



def convert_lines_to_vectors(lines_json):
    vectors = []
    for line in lines_json:
        center_x = line['left']
        center_y = line['top']

        x1 = line['x1']
        y1 = line['y1']
        x2 = line['x2']
        y2 = line['y2']

        # transform into proper coordinates
        x1 = x1 + center_x
        y1 = y1 + center_y

        x2 = x2 + center_x
        y2 = y2 + center_y

        vectors.append((x1, y1, x2, y2))

    return vectors

def write_vectors_to_s3(vectors, bucket, key):
    print(f"Writing vectors to S3: {bucket}/{key}")
    s3_client = boto3.client('s3')
    s3_client.put_object(Body=str(vectors), Bucket=bucket, Key=key)




def extract_first_frame(bucket, key):
    import cv2

    from botocore.config import Config

    my_config = Config(
        signature_version = 's3v4',
    )

    s3_client = boto3.client('s3', config=my_config, region_name="us-east-2", aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    
    # Generate a pre-signed URL to access the video
    url = s3_client.generate_presigned_url('get_object', 
                                           Params={'Bucket': bucket, 'Key': key}, 
                                           ExpiresIn=7600)

    
    # Use OpenCV to capture the first frame
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    cap.release()

    # convert to RGB from BGR without opencv, just permute the channels

    if ret and frame is not None:
        frame = frame[:, :, ::-1]
        return frame
    else:
        print(f'Failed to capture video from {url}')
        return None
