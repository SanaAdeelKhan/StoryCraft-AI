# streamlit_app.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageStat
from fpdf import FPDF
import google.generativeai as genai
import io
import os
import numpy as np
import tempfile
import random
import traceback

st.set_page_config(page_title="StoryCraft AI", layout="wide")
st.title("📚 StoryCraft AI – AI Storybook Generator")
st.markdown("Turn kids’ messy doodles, drawings, or text into magical AI-generated stories!")

# ---- Configure Gemini API safely ----
api_key = os.getenv("GOOGLE_API_KEY")
try:
    # Streamlit secrets support
    if (not api_key) and ("GOOGLE_API_KEY" in st.secrets):
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    # st.secrets may not exist locally; ignore
    pass

genai_available = False
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        genai_available = True
    except Exception as e:
        # model creation/access failed (maybe no access to that exact model)
        st.warning("Gemini API key detected but model access failed. App will use a fallback story generator.\n" 
                   "See logs for details.")
        st.write("**(Gemini error)**", str(e))
        genai_available = False
else:
    st.info("No GOOGLE_API_KEY found. You can still type descriptions or draw/upload images; "
            "the app will use a local fallback story generator. To enable Gemini, add your API key "
            "in Streamlit Secrets as `GOOGLE_API_KEY` and redeploy.")

# ---- Sidebar: input method (3 options) ----
st.sidebar.header("Choose Input Method")
option = st.sidebar.radio("Select how to start:", ["Upload Images", "Draw a Doodle", "Type Description"])

uploaded_files = []
drawn_image = None
typed_description = None

if option == "Upload Images":
    uploaded_files = st.file_uploader(
        "Upload doodles or drawings", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )

elif option == "Draw a Doodle":
    canvas = st_canvas(
        fill_color="rgba(255,255,255,1)",
        stroke_width=4,
        stroke_color="#000000",
        background_color="#ffffff",
        width=400,
        height=300,
        drawing_mode="freedraw",
        key="canvas"
    )
    if canvas.image_data is not None:
        # canvas.image_data is a numpy array (H x W x 4)
        arr = (canvas.image_data).astype("uint8")
        drawn_image = Image.fromarray(arr)

elif option == "Type Description":
    typed_description = st.text_area("Describe your doodle or scene here (comma-separated for multiple items):")

# ---- Theme ----
theme = st.selectbox("Choose Story Theme", ["fantasy", "adventure", "mystery", "comedy"], index=0)

# ---- Helper: simple local caption from image (dominant color + name) ----
def basic_caption_from_image(pil_img: Image.Image, filename: str = "doodle"):
    try:
        thumb = pil_img.convert("RGB").resize((32, 32))
        stat = ImageStat.Stat(thumb)
        r, g, b = stat.mean[:3]
        if (r > g) and (r > b):
            color = "red"
        elif (g > r) and (g > b):
            color = "green"
        elif (b > r) and (b > g):
            color = "blue"
        else:
            color = "multi-colored"
        caption = f"A messy childlike doodle titled '{filename}' with dominant color {color} and playful crayon-style strokes."
        return caption
    except Exception:
        return f"A playful doodle named '{filename}'"

# ---- Story generation via Gemini (if available) or fallback ----
def generate_story_via_gemini(captions, theme="fantasy"):
    # Compose a helpful instruction-style prompt
    prompt = (
        f"Write a short, child-friendly story (about 200-400 words) in a {theme} style that connects these scenes. "
        "Keep language simple (age 4-9), use lively imagery, give a main character name, and include a positive ending.\n\n"
    )
    for i, cap in enumerate(captions, 1):
        prompt += f"Scene {i}: {cap}\n"
    prompt += "\nMake it imaginative, warm, and easy to read aloud."

    # call Gemini
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # bubble up the exception for the caller to handle
        raise

def local_fallback_story(captions, theme="fantasy"):
    # deterministic-ish hero name
    names = ["Mina", "Ali", "Zara", "Sam", "Luna", "Noor", "Omar", "Ivy"]
    hero = random.choice(names)
    story_lines = []
    story_lines.append(f"Once upon a bright morning, {hero} discovered a tiny mystery.")
    for i, cap in enumerate(captions, 1):
        story_lines.append(f"In scene {i}, {hero} saw {cap.lower()}. {hero} wondered what it could mean.")
    story_lines.append(f"With curiosity and kindness, {hero} solved the small mystery and learned something new.")
    story_lines.append("They celebrated with a big smile and a silly dance, and everyone clapped.")
    return "\n\n".join(story_lines)

# ---- PDF creation ----
def create_pdf(images, story_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # split story into paragraphs
    paragraphs = [p.strip() for p in story_text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [story_text]

    for i, img in enumerate(images):
        pdf.add_page()
        # save image to a temporary path
        tmpf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        try:
            img_rgb = img.convert("RGB")
            img_rgb.save(tmpf.name)
            pdf.image(tmpf.name, x=10, y=20, w=90)
        finally:
            tmpf.close()
            os.remove(tmpf.name)

        pdf.set_font("Arial", size=12)
        pdf.set_xy(110, 20)
        paragraph = paragraphs[i] if i < len(paragraphs) else paragraphs[-1]
        pdf.multi_cell(90, 8, paragraph)

    # if there are more paragraphs than images, append them on extra pages
    if len(paragraphs) > len(images):
        for p in paragraphs[len(images):]:
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, p)

    out_tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    out_tmp.close()
    pdf.output(out_tmp.name)
    return out_tmp.name

# ---- Main action ----
if st.button("✨ Generate Storybook"):
    try:
        captions = []
        images = []

        if uploaded_files:
            for f in uploaded_files:
                img = Image.open(f).convert("RGB")
                images.append(img)
                captions.append(basic_caption_from_image(img, getattr(f, "name", "upload")))
        elif drawn_image is not None:
            images.append(drawn_image)
            captions.append(basic_caption_from_image(drawn_image, "canvas_doodle"))
        elif typed_description and typed_description.strip():
            # allow multiple items separated by commas
            items = [i.strip() for i in typed_description.split(",") if i.strip()]
            captions = items if items else [typed_description.strip()]
        else:
            st.warning("Please upload, draw, or type a description to create a storybook.")
            st.stop()

        # Try Gemini if available
        story = None
        if genai_available:
            try:
                with st.spinner("Generating story using Gemini..."):
                    story = generate_story_via_gemini(captions, theme)
            except Exception as e:
                st.error("Gemini generation failed — using local fallback story instead.")
                st.write("Error summary:", str(e))
                story = local_fallback_story(captions, theme)
        else:
            # no API key -> use fallback
            story = local_fallback_story(captions, theme)

        # Display story
        st.subheader("Generated Story")
        st.text_area("Story", story, height=300)

        # If we have images, produce PDF
        if images:
            with st.spinner("Creating PDF..."):
                pdf_path = create_pdf(images, story)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Storybook (PDF)", f, file_name="storybook.pdf")
            # optionally remove pdf file
            try:
                os.remove(pdf_path)
            except Exception:
                pass

    except Exception as e:
        st.error("An unexpected error occurred while generating the storybook.")
        st.write(traceback.format_exc())
