import streamlit as st
from lib import get_s3_status

# Streamlit page setup
st.title("S3 Bucket Processing Status")

refresh = st.button('Refresh Data')

# Manage initial load and refresh with session state
if 'first_load' not in st.session_state:
    st.session_state['first_load'] = True

# Auto-refresh on the initial load or when the refresh button is pressed
if st.session_state['first_load'] or refresh:
    # Fetch data
    data_df = get_s3_status()
    # Display data
    st.dataframe(data_df)
    st.session_state['first_load'] = False
