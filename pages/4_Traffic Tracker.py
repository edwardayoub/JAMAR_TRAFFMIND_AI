import streamlit as st
from lib import download_file, list_files

st.set_page_config(layout="wide")

# Example list of processed videos - this list is empty to simulate the current situation
processed_videos = list_files('traffmind-client-videos-processed-e2', '*')  # Update this with actual processed videos once available

st.title("Traffic Tracker Processed Videos")

# Introduction and user guidance
st.markdown("""
Experience our Traffic Tracker's capabilities firsthand. This feature automatically identifies and tracks vehicles with bounding boxes, enhancing traffic video analysis. Follow the steps below to view and download your processed videos:
1. **Select Your Submission**: Use the dropdown menu in the side panel to select one of your video submissions.
2. **View Processed Video**: The processed video with vehicle tracking will be displayed in the main panel.
3. **Download Video**: A download button will appear below the dropdown menu if a processed video is available.
""")

# Side panel for submission selection
with st.sidebar:
    st.header("Select Your Submission")
    # Dropdown menu for selecting a submission
    selected_submission = st.selectbox("Previous Submissions", options=processed_videos)

# Main panel for displaying the processed video
st.header("Processed Video with Traffic Tracker")

# if video selected, display download button, if clicked, download the video
if processed_videos:
    if selected_submission:
        if st.button("Download Video"):
            download_file('traffmind-client-videos-processed-e2', selected_submission)
            with open(selected_submission, "rb") as file:
                file_bytes = file.read()
            # auto click the download button

            st.download_button(label="Click here to download the processed video", data=file_bytes, file_name=selected_submission)

else:
    # Display a message indicating that no processed videos are currently available
    st.warning("There are no processed videos available at this time. Please check back later.")
