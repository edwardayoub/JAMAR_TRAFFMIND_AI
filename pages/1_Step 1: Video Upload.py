import streamlit as st
import logging
import os
import streamlit.components.v1 as components

# Initialize logger
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Header
st.header("TraffMind AI Job Submission")

# Step 1: Select a video
st.markdown("""
**1. Select a Video**: Upload a video file to start the job submission process. Only MP4 and h264 formats are supported.
""")

# Iframe for file upload and submission
components.iframe("https://traffmind-upload-ui.s3.us-east-2.amazonaws.com/index.html", height=125)

# Placeholder to capture the file name from the iframe
uploaded_video_name = st.empty()


# Link to check status
st.markdown("""
**2. Draw Vectors**: Before submitting the job, you can draw vectors on the video to track vehicles.
""")

st.page_link(
    "pages/1_Step 2: Draw Vectors.py",
    label=":blue[Step 2: Draw Vectors]",
    disabled=False
)
