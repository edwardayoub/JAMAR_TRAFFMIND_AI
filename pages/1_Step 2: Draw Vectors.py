import streamlit as st
from PIL import Image
from lib.aws import list_files_paginated, extract_first_frame, convert_lines_to_vectors, write_vectors_to_s3, convert_vectors_to_lines
from lib.sagemaker_processing import run
import draw_lines
from collections import defaultdict
import logging
import base64
import cv2

logger = logging.getLogger(st.__name__)

# Function to handle button clicks
def handle_click(direction, index):
    st.session_state[f"button_{index}"] = direction

st.set_page_config(page_title="TraffMind AI Traffic Counter", layout="wide")

st.header("TraffMind AI Draw Vectors")
stroke_width = 3
drawing_mode = "line"
bg_image = None

# Manage initial load and refresh with session state
if 'vector_names' not in st.session_state:
    names = list_files_paginated("jamar", "client_upload/", file_type='*')
    st.session_state['vector_names'] = [name.split('/')[-1] for name in names]

if 'names_to_vectors' not in st.session_state:
    st.session_state['names_to_vectors'] = defaultdict(list)

# Dropdown for selecting a background image
bg_video_name = st.selectbox("Select a video to draw vectors on", st.session_state['vector_names'])

@st.cache_data
def get_first_frame(video_name):
    return extract_first_frame("jamar", f"client_upload/{video_name}")

@st.cache_data
def frame_to_base64(frame):
    _, encoded_frame = cv2.imencode('.png', frame)
    return base64.b64encode(encoded_frame).decode('utf-8')

if bg_video_name:
    if 'bg_video_name' not in st.session_state or st.session_state['bg_video_name'] != bg_video_name:
        frame = get_first_frame(bg_video_name)
        if frame is not None:
            image_height, image_width, _ = frame.shape
            st.session_state.image_height = image_height
            st.session_state.image_width = image_width
            st.session_state['bg_image'] = frame_to_base64(frame)
            st.session_state['bg_video_name'] = bg_video_name
            st.session_state['canvas_result'] = None  # Clear canvas

lines = []

if 'bg_image' in st.session_state:
    lines = draw_lines.draw_lines(
        st.session_state['bg_image'],
        st.session_state['image_width'],
        st.session_state['image_height'],
        lines=convert_vectors_to_lines(st.session_state['names_to_vectors'][bg_video_name]),
        key=st.session_state['bg_video_name'] + "_lines"
    )

if lines:
    vectors = convert_lines_to_vectors(lines)
    st.session_state['vectors'] = vectors
    st.session_state['names_to_vectors'][bg_video_name] = vectors

    for i, (x1, y1, x2, y2) in enumerate(vectors):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f":blue[Vector {i + 1}]")
        with col2:
            directions_list = ["N", "E", "S", "W"]
            option = st.selectbox(f"Vector {i + 1} Direction", directions_list, key=f"direction_{i}")
            if option:
                handle_click(option, i)

    if st.button("Save vectors and submit job"):
        file_type = st.session_state.get('bg_video_name').split('.')[-1]

        v = {}
        # Create a dictionary of directions to vectors
        for i, (x1, y1, x2, y2) in enumerate(vectors):
            v[st.session_state.get(f'button_{i}', 'Unknown')] = ((x1, y1), (x2, y2))

        # Save vectors to S3
        write_vectors_to_s3(v, "jamar", f'submissions/{st.session_state.get("bg_video_name").replace("." + file_type, "")}/vectors.txt')

        # Run the processing job
        run(st.session_state.get("bg_video_name"))
        st.write(f"Vectors saved!")
        st.write(f"Job submitted!")

    refresh = st.button('Refresh Videos', key='refresh')
    if refresh:
        names = list_files_paginated("jamar", "client_upload/", file_type='*')
        st.session_state['vector_names'] = [name.split('/')[-1] for name in names]

    st.markdown("""
    **3. Check Status**: Click the following link to check the status of your submission.
    """)
    st.page_link(
        "pages/1_Step 3: Traffic Tracker and Classifier.py",
        label=":blue[Step 3: Traffic Tracker and Classifier]",
        disabled=False
    )