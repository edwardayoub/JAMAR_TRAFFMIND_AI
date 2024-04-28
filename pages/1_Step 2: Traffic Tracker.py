import streamlit as st
from lib import list_files, generate_presigned_url

st.set_page_config(layout="wide")

bucket = "traffmind-client-processed-jamar"

# Example list of processed videos
processed_videos = list_files(bucket, '*', 'mp4')  # Update this with actual processed videos once available

st.title("Traffic Tracker Processed Videos")

# Introduction and user guidance
st.markdown("""
Experience our Traffic Tracker's capabilities firsthand. This feature automatically identifies and tracks vehicles with bounding boxes, enhancing traffic video analysis. Follow the steps below to view and download your processed videos:
1. **Select Your Submission**: Use the dropdown menu in the side panel to select one of your video submissions.
2. **View Processed Video**: Click the link provided to directly download the video from the storage service.
""")

# Side panel for submission selection
with st.sidebar:
    st.header("Select Your Submission")
    selected_submission = st.selectbox("Previous Submissions", options=processed_videos)

# Main panel for displaying download link
st.header("Processed Video with Traffic Tracker")

# Check if there are videos
if processed_videos:
    if selected_submission:
        # Generate a pre-signed URL for the selected video
        url = generate_presigned_url(bucket, selected_submission)
        # Display a link for the user to download the video directly
        st.markdown(f"[Download Processed Video]({url})", unsafe_allow_html=True)
else:
    st.warning("There are no processed videos available at this time. Please check back later.")
