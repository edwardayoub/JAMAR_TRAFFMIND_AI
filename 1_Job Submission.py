import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Example list of videos (replace with actual file paths or URLs)
video_list = ['Video1.mp4', 'Video2.mp4', 'Video3.mp4']

st.header("Job Submission for Video Traffic Analysis")

# Video selection dropdown
selected_video = st.selectbox("Select a video", options=video_list)

# Submission name input
submission_name = st.text_input("Submission Name", placeholder="Enter a name for your submission...")

# Submit button
if st.button("Submit"):
    st.success(f"Submission '{submission_name}' for '{selected_video}' received!")

# Previewing the selected video
st.video(selected_video)
