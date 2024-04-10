import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Simulated mapping of submission names to background image files.
# Replace these with your actual data.
background_images = {
    'Submission1': 'background1.jpg',
    'Submission2': 'background2.jpg',
    'Submission3': 'background3.jpg',
}

st.title("Background Detector")

# Introduction and user guidance
st.markdown("""
Explore the power of our background detection technology. This feature allows you to see the extracted background from your previously submitted videos. Here’s how to view your backgrounds:
1. **Select Your Submission**: Use the dropdown menu in the side panel to select one of your previous submissions.
2. **View the Background**: The extracted background image from your selected video will be displayed in the main panel.
""")

# Side panel for selection
with st.sidebar:
    st.header("Select Your Submission")
    # The keys of the dictionary are the submission names.
    selected_submission = st.selectbox("Previous Submissions", options=list(background_images.keys()))

# Main panel for displaying the background image
st.header("Extracted Background Image")

# Retrieve the file path or URL from the dictionary based on the selection
background_image_path = background_images[selected_submission]

# Load and display the background image
st.image(background_image_path, caption=f"Background for {selected_submission}", use_column_width=True)
