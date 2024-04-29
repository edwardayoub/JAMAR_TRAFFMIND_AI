import streamlit as st
import logging
from lib import get_s3_status

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_table_with_links(df):
    # Convert DataFrame to HTML, replacing text URL with an HTML link
    df['Download Link'] = df['Download Link'].apply(lambda x: f'<a href="{x}" target="_blank">Download</a>' if x is not None else "")
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Set page configuration
st.set_page_config(page_title="Traffic Tracker - Processed Videos", layout="wide")

st.header("TraffMind AI Traffic Tracker")

# Introduction and user guidance
st.sidebar.header("Navigation")
st.sidebar.markdown("""
**1. Refresh Data**: Click the button below to refresh the list of processed videos.
**2. Download Video**: After refreshing, use the main panel to download your processed videos.
""")

# Main panel for displaying download link
st.markdown("""
Experience our Traffic Tracker's capabilities firsthand. This feature automatically identifies and tracks vehicles with bounding boxes, enhancing traffic video analysis. View and download your processed videos:
""")

refresh = st.sidebar.button('Refresh Data', key='refresh')

# Manage initial load and refresh with session state
if 'first_load' not in st.session_state or refresh:
    st.session_state['first_load'] = False
    # Fetch data
    try:
        data_df = get_s3_status()
        if data_df.empty:
            st.warning("No processed videos found. Please check back later.")
        else:
            # Display data
            show_table_with_links(data_df)
    except Exception as e:
        logger.error("Failed to fetch processed video data: %s", e)
        st.error("Failed to load data. Please try refreshing the page.")

# Footer
st.markdown("""
**Check Status**: Use the link below to check the status of your submissions.
""")
st.page_link("Go to Submission Status", "pages/1_Step 1: Submit Your Video.py")

