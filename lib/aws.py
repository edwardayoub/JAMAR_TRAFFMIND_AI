import boto3


access_key = 'AKIAR6R7K5AHM72MI4NS'
secret_key = '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'
region = 'us-east-2'

def download_file(bucket_name, file_name):

    s3_client = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_client.download_file(bucket_name, file_name, file_name)

def list_files(bucket_name, prefix):
    
    s3 = boto3.client("s3", region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = s3.list_objects_v2(Bucket=bucket_name)

    files = []
    for obj in response.get('Contents', []):
        files.append(obj['Key'])

    return files