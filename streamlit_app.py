import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.title("📚 StoryCraft AI – AI Storybook Generator")

option = st.radio("Choose input method:", ["Upload Image", "Draw Doodle", "Type Text"])

if option == "Upload Image":
    uploaded = st.file_uploader("Upload your doodle", type=["png", "jpg", "jpeg"])
    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Your uploaded doodle")

elif option == "Draw Doodle":
    canvas = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",
        stroke_width=5,
        stroke_color="#000000",
        background_color="#ffffff",
        height=300,
        width=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    if canvas.image_data is not None:
        img = Image.fromarray((canvas.image_data).astype("uint8"))
        st.image(img, caption="Your doodle sketch")

elif option == "Type Text":
    description = st.text_area("Describe your doodle:")
    if description:
        st.write(f"✏️ Your doodle description: {description}")
