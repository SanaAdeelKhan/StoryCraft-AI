import streamlit as st
from streamlit_drawable_canvas import st_canvas
import google.generativeai as genai
from PIL import Image
import io
import base64

# --- Setup ---
st.set_page_config(page_title="Doodle to Story", page_icon="⭐", layout="wide")
st.title("🎨✨ Doodle to Magical Story")

# Gemini API setup
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
story_model = "models/gemini-2.5-pro"
image_model = "models/imagen-4.0-generate-001"

st.write("Draw anything (like ⭐, ☁, 🌙). AI will guess what you drew and turn it into a magical story with illustrations!")

# --- Drawing Canvas ---
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=4,
    stroke_color="#000000",
    background_color="#ffffff",
    width=400,
    height=400,
    drawing_mode="freedraw",
    key="canvas",
    update_streamlit=True
)

# --- Clear Button ---
if st.button("🧹 Clear Canvas"):
    st.experimental_rerun()

# --- Process doodle ---
if canvas_result.image_data is not None:
    # Convert canvas to image
    img = Image.fromarray((canvas_result.image_data).astype("uint8"))

    # Convert to bytes for Gemini
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    if st.button("✨ Create Story from My Doodle"):
        with st.spinner("Looking at your doodle..."):
            # --- Step 1: Recognize Object ---
            detect_prompt = """
            You are an art teacher for kids.
            Look at this doodle and guess what object it represents (like star, moon, sun, house, tree, etc).
            If unclear, pick something fun it could look like.
            Answer in 1-3 words only.
            """
            detect_response = genai.GenerativeModel(story_model).generate_content(
                [detect_prompt, {"mime_type": "image/png", "data": img_bytes}]
            )
            object_name = detect_response.text.strip()

            # --- Step 2: Generate Story ---
            story_prompt = f"""
            A child has drawn a {object_name}.
            Create a short magical story (under 120 words) featuring this {object_name}.
            Make it fun, imaginative, and kid-friendly.
            """
            story_response = genai.GenerativeModel(story_model).generate_content(story_prompt)
            story_text = story_response.text

            st.subheader("📖 Your Magical Story")
            st.write(story_text)

            # --- Step 3: Generate 3 Story Illustrations ---
            st.subheader("🎨 Illustration Options")
            img_prompts = [
                f"Children’s book style cute illustration of a {object_name} from this story: {story_text}",
                f"Fantasy art dreamy illustration of a {object_name} inspired by the story: {story_text}",
                f"Minimalist pastel illustration of a {object_name} from the story: {story_text}"
            ]

            cols = st.columns(3)
            for i, ip in enumerate(img_prompts):
                with cols[i]:
                    try:
                        img_out = genai.GenerativeModel(image_model).generate_content(ip)
                        image_base64 = img_out.candidates[0].content.parts[0].inline_data.data
                        image_bytes = base64.b64decode(image_base64)
                        st.image(image_bytes, use_column_width=True, caption=f"Option {i+1}")
                    except Exception as e:
                        st.error(f"Image {i+1} failed: {e}")
