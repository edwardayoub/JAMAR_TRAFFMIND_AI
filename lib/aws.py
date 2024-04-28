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
    unprocessed_files = s3.list_objects_v2(Bucket="traffmind-client-unprocessed-jamar")
    status_df = pd.DataFrame(unprocessed_files['Contents'])
    
    # Format the dataframe for unprocessed files
    status_df['LastModified'] = pd.to_datetime(status_df['LastModified'])
    status_df['Video'] = status_df['Key'].apply(lambda x: x.split('/')[-1].split('.mp4')[0])
    status_df['LastModified'] = status_df['LastModified'] - pd.Timedelta(hours=4)
    status_df['Submission date'] = status_df['LastModified'].dt.date
    status_df['Submission Time (EST)'] = status_df['LastModified'].apply(lambda x: x.time().strftime("%I:%M %p"))
    
    # List processed files
    processed_files = s3.list_objects_v2(Bucket="traffmind-client-processed-jamar")
    processed_files = pd.DataFrame(processed_files['Contents'])
    
    # Format the dataframe for processed files
    processed_files['Video'] = processed_files['Key'].apply(lambda x: x.split('/')[-1].split('_median_frame.png')[0])
    
    # Determine the status of each Video
    status_df['Status'] = status_df['Video'].apply(lambda x: 'Finished' if x in processed_files['Video'].tolist() else 'Processing')
    
    # Arrange and sort the final status dataframe
    status_df = status_df[['Video', 'Submission date', 'Submission Time (EST)', 'Status']]
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
