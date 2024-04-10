import streamlit as st

st.set_page_config(layout="wide")

# Example list of processed videos - this list is empty to simulate the current situation
processed_videos = []  # Update this with actual processed videos once available

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

if processed_videos:
    # If there are processed videos available, attempt to display the selected video
    selected_video_path = processed_videos[selected_submission] if selected_submission in processed_videos else None
    if selected_video_path:
        st.video(selected_video_path)
        # Display a download button for the selected video
        with open(selected_video_path, "rb") as file:
            st.sidebar.download_button(
                label="Download Processed Video",
                data=file,
                file_name=selected_video_path.split('/')[-1],  # Assuming the path format allows this
                mime="video/mp4"
            )
else:
    # Display a message indicating that no processed videos are currently available
    st.warning("There are no processed videos available at this time. Please check back later.")
