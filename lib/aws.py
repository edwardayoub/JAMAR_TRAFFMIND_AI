import boto3
import os

# read keys in from environment variables
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

region = 'us-east-2'

def download_file(bucket_name, file_name, path):

    s3_client = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    print(f"Downloading. bucket: {bucket_name}, file: {file_name}, path: {path}")
    s3_client.download_file(bucket_name, path, file_name)

def list_files(bucket_name, prefix):
    
    s3 = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = s3.list_objects_v2(Bucket=bucket_name)

    files = []
    for obj in response.get('Contents', []):
        files.append(obj['Key'])

    return files