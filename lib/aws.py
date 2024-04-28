import boto3
import os
import pandas as pd

# read keys in from environment variables
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

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

def get_s3_status():
    # Initialize S3 client with provided credentials
    s3 = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    # List unprocessed files
    unprocessed_response = s3.list_objects_v2(Bucket="traffmind-client-unprocessed-jamar")
    if 'Contents' in unprocessed_response:
        unprocessed_files = pd.DataFrame(unprocessed_response['Contents'])
        unprocessed_files['LastModified'] = pd.to_datetime(unprocessed_files['LastModified'])
        unprocessed_files['Video'] = unprocessed_files['Key'].apply(lambda x: x.split('/')[-1].split('.mp4')[0])
        unprocessed_files['LastModified'] = unprocessed_files['LastModified'] - pd.Timedelta(hours=4)
        unprocessed_files['Submission date'] = unprocessed_files['LastModified'].dt.date
        unprocessed_files['Submission Time (EST)'] = unprocessed_files['LastModified'].apply(lambda x: x.time().strftime("%I:%M %p"))
    else:
        unprocessed_files = pd.DataFrame(columns=['Key', 'LastModified', 'Video', 'Submission date', 'Submission Time (EST)'])

    # List processed files
    processed_response = s3.list_objects_v2(Bucket="traffmind-client-processed-jamar")
    if 'Contents' in processed_response:
        processed_files = pd.DataFrame(processed_response['Contents'])
        processed_files['Video'] = processed_files['Key'].apply(lambda x: x.split('/')[-1].split('_median_frame.png')[0])
    else:
        processed_files = pd.DataFrame(columns=['Key', 'Video'])

    # Determine the status of each Video
    unprocessed_files['Status'] = unprocessed_files['Video'].apply(lambda x: 'Finished' if x in processed_files['Video'].tolist() else 'Processing')
    
    # Arrange and sort the final status dataframe
    status_df = unprocessed_files[['Video', 'Submission date', 'Submission Time (EST)', 'Status']]
    status_df = status_df.sort_values(by=['Submission date', 'Submission Time (EST)'], ascending=False).reset_index(drop=True)
    
    return status_df


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
