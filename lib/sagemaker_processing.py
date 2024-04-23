import boto3
import sys
import random
import hashlib


def start_sagemaker_processing_job(infile, environment_variables):
    # Initialize the SageMaker client
    sagemaker_client = boto3.client('sagemaker')

    # Specify the S3 bucket and file paths
    bucket = "traffmind-client-videos-e2"
    out_bucket = "traffmind-client-videos-processed-e2"
    outfile = 'processed_' + infile

    input_path = f's3://{bucket}/{infile}'
    output_path = f's3://{out_bucket}'

    # random number
    random_num = random.randint(0, 1000)

    # hash filename
    hash_object = hashlib.md5(infile.encode())
    hash_filename = hash_object.hexdigest()

    

    # Define the processing job configuration
    processing_job_name = f"{hash_filename}-{random_num}"
    processing_job_config = {
        'ProcessingJobName': processing_job_name,
        'RoleArn': 'arn:aws:iam::134350563342:role/service-role/AmazonSageMaker-ExecutionRole-20240119T144933',
        'AppSpecification': {
            'ImageUri': '134350563342.dkr.ecr.us-east-2.amazonaws.com/traffmind:1.0.45',
        },
        'ProcessingInputs': [{
            'InputName': 'input1',
            'S3Input': {
                'S3Uri': input_path,
                'LocalPath': '/opt/ml/processing/input',
                'S3DataType': 'S3Prefix',
                'S3InputMode': 'File',
                'S3DataDistributionType': 'FullyReplicated'
            }
        }],
        "ProcessingOutputConfig": {
            "Outputs": [{
                "OutputName": "output1",
                
            "S3Output": {
                "S3Uri": output_path,
                "LocalPath": "/opt/ml/processing/output/",
                "S3UploadMode": "EndOfJob"
            }
        }]
        },
        'Environment': environment_variables,
        'ProcessingResources': {
            'ClusterConfig': {
                'InstanceCount': 1,
                'InstanceType': 'ml.c5.18xlarge',
                'VolumeSizeInGB': 1
            }
        },
        'StoppingCondition': {
            'MaxRuntimeInSeconds': 14400
        }
    }

    # Start the processing job
    response = sagemaker_client.create_processing_job(**processing_job_config)
    print(f"Processing job started with ARN: {response['ProcessingJobArn']}")
    return response


def run(infile):
    
    start_sagemaker_processing_job(infile, {"AWS": "True"})