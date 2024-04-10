import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Example list of videos - this list will be empty to simulate your current situation
video_list = []

st.header("Job Submission for Video Traffic Analysis")

# Guide the user through the submission process
st.markdown("""
Welcome to our video traffic analysis portal. Here, you can submit your traffic videos for analysis. Follow the steps below to get started:
1. **Select a Video**: Choose the video you want to analyze from the dropdown menu.
2. **Name Your Submission**: Enter a unique name for your submission to easily track your analysis.
3. **Submit**: Click the submit button to send your video for processing.
""")

if video_list:
    # Video selection dropdown
    selected_video = st.sidebar.selectbox("Select a video", options=video_list)

    # Submission name input
    submission_name = st.sidebar.text_input("Submission Name", placeholder="Enter a name for your submission...")

    # Submit button
    if st.sidebar.button("Submit"):
        st.success(f"Submission '{submission_name}' for '{selected_video}' received!")

    # Previewing the selected video
    st.video(selected_video)
else:
    st.warning("No videos are currently available for submission. Please check back later.")
