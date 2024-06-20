import streamlit.components.v1 as components
import os


parent_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(parent_dir, "frontend", "build")

draw_lines_func = components.declare_component(
        "draw_lines",
        path=frontend_dir,
        #url=frontend_dir
        #url="http://localhost:3001",
    )

# Create a wrapper function that calls the custom component
def draw_lines(image, width, height, lines=[], key=None):
    component_value = draw_lines_func(image=image, width=width, height=height, lines=lines, key=key, default=[])
    return component_value