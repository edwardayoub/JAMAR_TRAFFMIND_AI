import streamlit as st
from PIL import Image

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

    # Attempt to display a download button if the video is available
    processed_video_path = processed_videos.get(selected_submission)
    if processed_video_path:
        try:
            with open(processed_video_path, "rb") as file:
                btn = st.download_button(
                    label="Download Processed Video",
                    data=file,
                    file_name=processed_video_path.split('/')[-1],  # Assumes file paths can have directories
                    mime="video/mp4"
                )
        except FileNotFoundError:
            st.error(f"The processed video file for '{selected_submission}' was not found.")

# Main panel for displaying the processed video
st.header("Processed Video with Traffic Tracker")

if processed_video_path:
    try:
        st.video(processed_video_path)
    except FileNotFoundError:
        st.error("The processed video for this submission is currently unavailable.")
