import streamlit as st
from lib import get_s3_status
def show_table_with_links(df):
    # Convert DataFrame to HTML, replacing text URL with an HTML link
    df['Download Link'] = df['Download Link'].apply(lambda x: f'<a href="{x}" target="_blank">Download</a>' if x is not None else "")
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)


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
    show_table_with_links(data_df)
    st.session_state['first_load'] = False
