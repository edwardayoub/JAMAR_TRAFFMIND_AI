import streamlit as st
from PIL import Image
import base64

st.set_page_config(layout="wide")

# Simulated mapping of submission names to processed video files.
# Replace these with your actual data.
processed_videos = {
    'Submission1': 'processed_video1.mp4',
    'Submission2': 'processed_video2.mp4',
    'Submission3': 'processed_video3.mp4',
}

st.title("Traffic Tracker Processed Videos")

# Introduction and user guidance
st.markdown("""
Experience our Traffic Tracker's capabilities firsthand. This feature automatically identifies and tracks vehicles with bounding boxes, enhancing traffic video analysis. Follow the steps below to view and download your processed videos:
1. **Select Your Submission**: Use the dropdown menu in the side panel to select one of your video submissions.
2. **View Processed Video**: The processed video with vehicle tracking will be displayed in the main panel.
3. **Download Video**: Click the download button below to download your processed video.
""")

# Side panel for submission selection and download
with st.sidebar:
    st.header("Select Your Submission")
    # Dropdown menu for selecting a submission
    selected_submission = st.selectbox("Previous Submissions", options=list(processed_videos.keys()))

    # Retrieve the file path or URL from the dictionary based on the selection
    processed_video_path = processed_videos[selected_submission]

    # Display a download button if the video is available
    if processed_video_path:
        # This example assumes local file paths; adjust accordingly if using URLs
        file_path = processed_video_path  # Ensure this is the correct path to the file on the server
        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="Download Processed Video",
                data=file,
                file_name=processed_video_path,
                mime="video/mp4"
            )

# Main panel for displaying the processed video
st.header("Processed Video with Traffic Tracker")

if processed_video_path:
    # Attempt to display the processed video
    st.video(processed_video_path)
else:
    st.error("The processed video for this submission is currently unavailable.")
