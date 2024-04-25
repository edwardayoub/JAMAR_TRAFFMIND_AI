import streamlit as st
from lib import get_s3_status

# Streamlit page setup
st.title("S3 Bucket Processing Status")

if st.button('Refresh Data'):
    if region and access_key and secret_key:
        # Fetch data
        data_df = get_s3_status()
        # Display data
        st.dataframe(data_df)
    else:
        st.error("Please enter all AWS credentials.")
