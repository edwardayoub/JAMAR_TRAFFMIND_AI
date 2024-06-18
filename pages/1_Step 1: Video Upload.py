import streamlit as st
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Header
st.header("TraffMind AI Job Submission")

# Step 1: Upload Video Using SFTP
st.markdown("""
**1. Upload Video Using SFTP**

You can now upload your videos using an SFTP client such as Cyberduck. Follow the steps below:

### Step-by-Step Guide

1. **Download Cyberduck**:
    - Go to the [Cyberduck website](https://cyberduck.io/download/) and download the version suitable for your operating system.
    - Install Cyberduck following the instructions provided on the website.

    *Screenshots Placeholder*

2. **Login to SFTP Server**:
    - Open Cyberduck.
    - Click on "Open Connection".
    - Select "SFTP (SSH File Transfer Protocol)" from the dropdown menu.

    *Screenshots Placeholder*

3. **Enter Login Details**:
    - Server: `YOUR_SFTP_SERVER`
    - Username: `YOUR_USERNAME`
    - Password: Leave this blank.
    - SSH Private Key: Use the private key we provided to you.

    *Screenshots Placeholder*

4. **Upload Your Video**:
    - Once logged in, navigate to the folder where you want to upload your video.
    - Drag and drop your video file into Cyberduck to upload.

    *Screenshots Placeholder*

5. **Confirmation**:
    - After the upload is complete, you will receive a confirmation email.
    - You can also check the status of your upload on the TraffMind AI portal.

    *Screenshots Placeholder*
""")

# Link to check status
st.markdown("""
**2. Draw Vectors**: Before submitting the job, you can draw vectors on the video to track vehicles.
""")

st.page_link(
    "pages/1_Step 2: Draw Vectors.py",
    label=":blue[Step 2: Draw Vectors]",
    disabled=False
)
