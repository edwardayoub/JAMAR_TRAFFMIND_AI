import streamlit as st
import logging
import boto3
from botocore.exceptions import ClientError
import requests
from lib import run
import os

def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.

    :param s3_client: A Boto3 Amazon S3 client.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method
        )
        raise
    return url

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

st.header("TraffMind AI Job Submission")

st.markdown("""
Welcome to our video traffic analysis portal. Here, you can submit your traffic videos for analysis. Follow the steps below to get started:
1️⃣ **Select a Video**: You can drag and drop or select a video file to upload by clicking the uploader below. Only MP4 format is supported.
""")

# File uploader for video selection
uploaded_video = st.file_uploader("Upload your video", type=['mp4'])

if uploaded_video is not None:
    # Display the name of the uploaded file
    st.sidebar.write("Selected Video: ", uploaded_video.name)
else:
    st.sidebar.write("Please upload a video to proceed.")

st.markdown("""
2️⃣ **Submit**: Click the submit button to send your video for processing.
""")
# Submit button
if st.button("Submit", key='submit'):
    if uploaded_video is not None:
        st.sidebar.success("Your submission is received!")
        print(uploaded_video.name)

        # read keys in from environment variables
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        s3_client = boto3.client("s3", region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        url = generate_presigned_url(
            s3_client, "put_object", {"Bucket": 'traffmind-client-unprocessed-jamar', "Key": uploaded_video.name}, 1000
        )
     
        response = requests.put(url, data=uploaded_video.getvalue())

        if response is not None:
            print("Got response:")
            print(f"Status: {response.status_code}")
            print(response.text)
        
            if response.status_code == 200:
                run(uploaded_video.name)
    else:
        st.sidebar.error("Please upload a video and provide a name for your submission.")

st.markdown("""
3️⃣ **Check Status**: 
""")
st.page_link("pages/2_Job Status.py" ,label = "Click here to check the status of your submission.",disabled=False)

