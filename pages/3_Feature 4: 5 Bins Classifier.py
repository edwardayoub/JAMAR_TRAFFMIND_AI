import os
import streamlit as st 
import numpy as np
from io import BytesIO
import tensorflow as tf
import cv2
from keras.preprocessing import image as image_utils
import PIL.ImageOps
from PIL import Image

# Function to preprocess the image for the model
def prepare_image(image_path):
    img = Image.open(image_path)
    img = img.resize((100, 100), Image.LANCZOS)  # Resize like the training images
    img = PIL.ImageOps.invert(img)
    img = image_utils.img_to_array(img)
    img = img / 255.0  # Normalize the image
    img = img.reshape(1, 100, 100, 3)  # Reshape for the model (batch_size, height, width, channels)
    return img
    
def app():
    st.set_page_config(page_title="Vehicle Classification Interface", layout="wide")
    
    st.header("Vehicle Type Classifier")
    st.subheader("Classify different types of vehicles in images")

    st.markdown("""
    **Welcome to the Vehicle Type Classifier!** This tool uses advanced neural networks to classify vehicle types from images. Follow the steps below to upload your image and get classification results:
    """)
    
    # Step 1: Upload Image
    st.markdown("""
    **1. Upload Image**: Drag and drop or select an image file for prediction. Supported format: JPEG.
    """)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg"])
    
    # Step 2: Identify and Predict
    if uploaded_file is not None:
        st.markdown("""
        **2. Identify and Predict**: Click 'Identify' to process the image and classify the type of vehicle.
        """)
        if st.button('Identify', key='identify'):
            # Step 3: Results
            st.markdown("""
            **3. Results**: View the image and its classified vehicle type below.
            """)
            st.write("Classifying...")
            preprocessed_image = prepare_image(uploaded_file)
            model_path = "./model/traffmind_weather_beta1.h5"
            loaded_model = tf.keras.models.load_model(model_path)
            predictions = loaded_model.predict(preprocessed_image)
            classes = ['Passenger Vehicles', 'Light Trucks', 'Buses', 'Single Unit Vehicles', 'Combination Units']
            prediction = classes[np.argmax(predictions)]
            st.write('Prediction: %s' % (prediction))
            st.image(image, caption='Uploaded Image.', use_column_width=False)


if __name__=='__main__':
    app()
