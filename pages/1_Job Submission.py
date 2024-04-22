import streamlit as st
import logging
import boto3
from botocore.exceptions import ClientError
import requests

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


def usage_demo():

    access_key = 'AKIAR6R7K5AHM72MI4NS'
    secret_key = '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'
    s3_client = boto3.client("s3", region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    url = generate_presigned_url(
        s3_client, "put_object", {"Bucket": 'traffmind-client-videos-e2', "Key": '902-962_Standard_SCU2AD_raw_tracker_output.mp4'}, 1000
    )

    with open('/Users/clayoneil/dev/video-analysis/demo_output/2024-04-04-17-00-28/902-962_Standard_SCU2AD_raw_tracker_output.mp4', "rb") as object_file:
        object_text = object_file.read()
    response = requests.put(url, data=object_text)

    if response is not None:
        print("Got response:")
        print(f"Status: {response.status_code}")
        print(response.text)

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

st.header("TraffMind AI Job Submission")

st.markdown("""
Welcome to our video traffic analysis portal. Here, you can submit your traffic videos for analysis. Follow the steps below to get started:
1. **Select a Video**: Choose the video you want to analyze by uploading it.
2. **Name Your Submission**: Enter a unique name for your submission to easily track your analysis.
3. **Submit**: Click the submit button to send your video for processing.
""")

# File uploader for video selection
uploaded_video = st.file_uploader("Upload your video", type=['mp4'])

if uploaded_video is not None:
    # Display the name of the uploaded file
    st.sidebar.write("Selected Video: ", uploaded_video.name)
else:
    st.sidebar.write("Please upload a video to proceed.")


# Submit button
if st.sidebar.button("Submit"):
    if uploaded_video is not None:
        st.sidebar.success("Your submission is received!")
        

        access_key = 'AKIAR6R7K5AHM72MI4NS'
        secret_key = '4aPgrXY+Zk9Q3yAVfzZB+mZG9ui0gJLUS4zY5UvF'
        s3_client = boto3.client("s3", region_name='us-east-2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        url = generate_presigned_url(
            s3_client, "put_object", {"Bucket": 'traffmind-client-videos-e2', "Key": uploaded_video.name}, 1000
        )
     
        response = requests.put(url, data=uploaded_video.getvalue())

        if response is not None:
            print("Got response:")
            print(f"Status: {response.status_code}")
            print(response.text)
        # Process the video file
        # Example: Save the uploaded file to a directory (if necessary)
        # with open(os.path.join("path_to_directory", uploaded_video.name), "wb") as f:
        #     f.write(uploaded_video.getvalue())
    else:
        st.sidebar.error("Please upload a video and provide a name for your submission.")

