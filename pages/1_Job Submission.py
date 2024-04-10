import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Example list of videos - assuming this could be empty or have invalid entries
video_list = ['Video1.mp4', 'Video2.mp4', 'Video3.mp4']  # Update this with actual videos

st.header("Job Submission for Video Traffic Analysis")

st.markdown("""
Welcome to our video traffic analysis portal. Here, you can submit your traffic videos for analysis. Follow the steps below to get started:
1. **Select a Video**: Choose the video you want to analyze from the dropdown menu.
2. **Name Your Submission**: Enter a unique name for your submission to easily track your analysis.
3. **Submit**: Click the submit button to send your video for processing.
""")

# Video selection dropdown
selected_video = st.selectbox("Select a video", options=video_list)

# Submission name input
submission_name = st.text_input("Submission Name", placeholder="Enter a name for your submission...")

# Submit button
if st.button("Submit"):
    st.success(f"Submission '{submission_name}' for '{selected_video}' received!")

# Attempt to preview the selected video only if it exists in the list
if selected_video and selected_video in video_list:
    # The preview is only attempted if `selected_video` is in `video_list`
    try:
        st.video(selected_video)
    except Exception as e:
        st.error("The selected video is currently unavailable for preview.")
else:
    # If the list is empty or the selected video is not in the list
    st.warning("The selected video is not available for preview.")
