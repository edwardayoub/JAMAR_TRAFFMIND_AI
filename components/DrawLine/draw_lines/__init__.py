import streamlit.components.v1 as components
import os


parent_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(parent_dir, "frontend", "build")

# Create a wrapper function that calls the custom component
def draw_lines(image, width, height):
    return components.declare_component(
        "draw_lines",
        path=frontend_dir,
        #url=frontend_dir
        #url="http://localhost:3001",
    )(image=image, width=width, height=height)