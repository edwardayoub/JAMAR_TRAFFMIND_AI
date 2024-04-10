import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Simulated mapping of submission names to obstacle detection result images.
# Replace these with your actual data.
obstacle_detection_images = {
    'Submission1': 'obstacle1.jpg',
    'Submission2': 'obstacle2.jpg',
    'Submission3': 'obstacle3.jpg',
}

st.title("TraffMind AI Obstacle Detector")

# Introduction and user guidance
st.markdown("""
Discover the capabilities of our obstacle detection technology. This advanced feature automatically identifies obstacles in the camera's view, significantly improving the quality of video processing for traffic analysis. Follow these steps to view obstacle detection results:
1. **Select Your Submission**: Use the dropdown menu in the side panel to choose one of your previous video submissions.
2. **View Obstacle Detection Results**: The detected obstacles from your selected video will be displayed in the main panel.
""")

# Side panel for selection
with st.sidebar:
    st.header("Select Your Submission")
    # The keys of the dictionary are the submission names.
    selected_submission = st.selectbox("Previous Submissions", options=list(obstacle_detection_images.keys()))

# Main panel for displaying the obstacle detection image
st.header("Detected Obstacles Image")

try:
    # Retrieve the file path or URL from the dictionary based on the selection
    obstacle_image_path = obstacle_detection_images[selected_submission]
    
    # Attempt to display the obstacle detection image
    st.image(obstacle_image_path, caption=f"Detected Obstacles for {selected_submission}", use_column_width=True)
except Exception as e:
    st.error("The obstacle detection image for this submission is currently unavailable.")
