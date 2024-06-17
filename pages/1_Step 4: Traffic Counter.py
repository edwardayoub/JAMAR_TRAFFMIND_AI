import streamlit as st
from lib.aws import list_files_paginated, download_file
import pandas as pd

# Set page configuration
st.set_page_config(page_title="TraffMind AI Traffic Counter", layout="wide")

st.header("TraffMind AI Traffic Counter")

# Manage initial load and refresh with session state
if 'first_load' not in st.session_state:
    name_to_key = {}
    names = list_files_paginated("jamar","outputs/", file_type='txt')
    # get just file names
    name_to_key = {name.split('/')[-1]: name for name in names}

    names = [name.split('/')[-1] for name in names]
    st.session_state['first_load'] = True
    st.session_state['names'] = names

refresh = st.button('Refresh Counts', key='refresh')

# Dropdown for selecting counts file
count_file_name = st.selectbox("Select a count file", st.session_state.get('names', []))

if count_file_name:
    # download the file from s3
    key = name_to_key[count_file_name]
    download_file("jamar", key, count_file_name)


    count_file_path = count_file_name
    try:
        with open(count_file_path, 'r') as f:

            d = eval(f.readlines()[0])
            # remove empty dicts from list
            d = [x for x in d if x]
            # remove index column

            rows = []

            for i in d:
                for class_number in range(1, 7):
                    row = {'class': class_number}
                    for feature, values in i.items():
                        row[feature] = values.get(class_number, 0)
                    rows.append(row)
            final_df = pd.DataFrame(rows)

            st.write(final_df)
    except Exception as e:
        st.error(f"Error loading counts file: {e}")



