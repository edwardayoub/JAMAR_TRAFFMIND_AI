import streamlit as st
from lib import get_s3_status

# Streamlit page setup
st.title("S3 Bucket Processing Status")

# Manage initial load and refresh with session state
if 'first_load' not in st.session_state:
    st.session_state['first_load'] = True

if st.session_state['first_load'] or st.button('Refresh Data'):
    # Fetch data
    data_df = get_s3_status(region, access_key, secret_key)
    # Display data
    st.dataframe(data_df)
    st.session_state['first_load'] = False
