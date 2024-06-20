import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch
from torchvision import transforms
import cv2

from lib import download_file, send_discord_notification

st.set_page_config(page_title="Vehicle Detection Interface", layout="wide")



device = 'cuda' if torch.cuda.is_available() else 'cpu'


@st.cache_resource
def get_model():
    from ultralytics import RTDETR, YOLO
    import supervision as sv
    download_file('traffmind-models', 'rtdetr-l.pt', 'rtdetr-l.pt')

    class_model_path = './model/yolov8-cls.yaml'
    check_point_dir = './model/yolov8n-cls-20240508-002451.pt'

    state_dict = torch.load(check_point_dir, map_location=device)
    class_model = YOLO(class_model_path)  # Assuming YOLO is a class you have defined or imported
    class_model = class_model.model.model
    class_model.to(device)
    class_model.eval()
    class_model.load_state_dict(state_dict)
    return class_model

class_model = get_model()


@st.cache_resource
def load_model():
    from ultralytics import RTDETR
    return RTDETR('rtdetr-l.pt')  # Path to your model

model = load_model()

size = 256
transform = transforms.Compose([
    transforms.Resize((size, size)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
color_map = {
        'bin 1': 'red',
        'bin 2': 'blue',
        'bin 3': 'green',
        'bin 4': 'yellow',
        'bin 5': 'purple',
        'bin 6': 'orange'
    }

def get_class_of_cropped_frame(cropped_frame, model, device):
    pil_image = Image.fromarray(cropped_frame)
    image_tensor = transform(pil_image).unsqueeze(0).to(device)
    with torch.no_grad():
        predictions = model(image_tensor)
    classes = ['bin 2', 'bin 3', 'bin 4', 'bin 5', 'bin 6']
    top_class_idx = torch.argmax(predictions, dim=1).item()
    top_class = classes[top_class_idx]
    return top_class

# Function to apply detections to a frame
def apply_detections_to_frame(frame, detections, class_results):
    pil_frame = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_frame, 'RGBA')

    # Get bounding box coordinates and class names
    detections_xyxy = detections.xyxy
    detections_class = class_results

    # Iterate over detections and class names
    for det, cls in zip(detections_xyxy, detections_class):
        x1, y1, x2, y2 = det
        # Get color for the class, default to white if class not in map
        box_color = color_map.get(cls, 'white')
        draw.rectangle([x1, y1, x2, y2], outline=box_color, width=3)

    return pil_frame

# Function to detect objects and draw bounding boxes
def detect_objects_and_draw(image):
    from ultralytics import RTDETR, YOLO
    import supervision as sv
    frame = np.array(image)
    original_frame = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Load the model and perform detection

    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    print(detections)
    
    # Filter detections and convert to PIL
    detections = detections[(detections['class_name'] == 'car') | (detections['class_name'] == 'truck') | (detections['class_name'] == 'bus') | (detections['class_name'] == 'motorcycle')]
    detections = detections[(detections.confidence > 0.6)]
    class_results = []    
    for i in range(len(detections.xyxy)):
        det = detections.xyxy[i]
        x1, y1, x2, y2 = map(int, det)  # Convert coordinates to integers
        cropped_frame = frame[y1:y2, x1:x2]
        if detections.data['class_name'][i] == 'motorcycle':
            result = 'bin 1'
        else:
            result = get_class_of_cropped_frame(cropped_frame, class_model, device)
        class_results.append(result)
    pil_frame = apply_detections_to_frame(original_frame, detections, class_results)
    
    return pil_frame


def app():
    
    st.header("Vehicle Detection System")
    st.subheader("Detect vehicles in uploaded images using advanced neural networks")

    st.markdown("""
    **Welcome to the Vehicle Detection System!** This tool leverages advanced neural networks to identify and classify various types of vehicles in images. Follow the steps below to upload your image and see the detection in action:
    """)
    
    st.markdown("""
    **1. Upload Image**: Drag and drop or select an image file to start the vehicle detection process. Supported formats: JPEG, PNG.
    """)

    
    # add text desciptions for bins and colored
    st.markdown(f"""
        <div style="background-color:black; padding:10px;">
        <span style="color:{color_map['bin 1']};">Bin 1: Motorcycles</span>, 
        <span style="color:{color_map['bin 2']};">Bin 2: Passenger Vehicles</span>, 
        <span style="color:{color_map['bin 3']};">Bin 3: Light Trucks</span>, 
        <span style="color:{color_map['bin 4']};">Bin 4: Buses</span>, 
        <span style="color:{color_map['bin 5']};">Bin 5: Single-unit Vehicles</span>, 
        <span style="color:{color_map['bin 6']};">Bin 6: Combination Units</span>
        </div>
        """, unsafe_allow_html=True)
                
    # Upload Image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    
    # Detect and Display
    if uploaded_file is not None:
        st.markdown("""
        **2. Detect and Classify**: Click 'Detect' to process your image and highlight the vehicles based on the type.
        """)
        if st.button('Detect', key='detect'):
            send_discord_notification(uploaded_file.name, uploaded_file.size / (1024 * 1024), "6 Bins Classifier Submission", "An image has been submitted to the 6 Bins Classifier!", 0xFC440F)
            st.markdown("""
            **3. Results**: View the image with detected vehicles, color-coded by type, shown below.
            """)
            image = Image.open(uploaded_file)
            processed_image = detect_objects_and_draw(image)
            st.image(processed_image, caption='Detected Vehicles', use_column_width=True)

if __name__=='__main__':
    app()
