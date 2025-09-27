import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from fpdf import FPDF
import google.generativeai as genai
import io
import os
import elevenlabs
import base64

# --- Setup ---
st.set_page_config(page_title="StoryCraft AI", layout="wide")
st.title("📚 StoryCraft AI – AI Storybook Generator with TTS")

# Gemini API setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
text_model = genai.GenerativeModel("models/gemini-2.5-flash")

# ElevenLabs API setup
elevenlabs.api_key = os.getenv("ELEVENLABS_API_KEY")

st.markdown("Turn kids’ doodles, drawings, or descriptions into magical AI-generated stories with voice narration!")

# --- Input Options ---
st.sidebar.header("Choose Input Method")
option = st.sidebar.radio("Select how to start:", ["Upload Images", "Draw a Doodle", "Type Description"])

uploaded_files = []
drawn_image = None
typed_description = None

# Clear canvas button
clear_canvas = st.sidebar.button("🧹 Clear Canvas")
if clear_canvas:
    st.session_state["canvas_cleared"] = True

if option == "Upload Images":
    uploaded_files = st.file_uploader(
        "Upload doodles or drawings",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

elif option == "Draw a Doodle":
    if "canvas_cleared" not in st.session_state:
        st.session_state["canvas_cleared"] = False

    canvas = st_canvas(
        fill_color="rgba(255,255,255,1)",
        stroke_width=4,
        stroke_color="#000000",
        background_color="#ffffff",
        width=400,
        height=400,
        drawing_mode="freedraw",
        key="canvas"
    )

    if st.session_state["canvas_cleared"]:
        canvas.image_data = None
        st.session_state["canvas_cleared"] = False

    if canvas.image_data is not None:
        drawn_image = Image.fromarray((canvas.image_data).astype("uint8"))

elif option == "Type Description":
    typed_description = st.text_area("Describe your doodle or scene here:")

# --- Theme ---
theme = st.selectbox(
    "Choose Story Theme",
    ["Adventure", "Comedy", "Fantasy", "Friendship", "Mystery", "Moral", "Islamic"],
    index=0
)

# --- Voice Selection ---
voice = st.selectbox(
    "Choose Narration Voice",
    ["Rachel", "Antoni", "Adam", "Bella"],
    index=0
)

# --- Story Generation ---
def generate_story(captions, theme="Fantasy"):
    prompt = f"Write a short children's story in a {theme} style based on these scenes:\n"
    for i, cap in enumerate(captions, 1):
        prompt += f"Scene {i}: {cap}\n"

    if theme == "Moral":
        prompt += "\nMake sure the story ends with a clear moral life lesson for kids."
    elif theme == "Islamic":
        prompt += "\nKeep the story child-friendly with Islamic values: honesty, kindness, respect, dua, helping parents, etc."

    try:
        response = text_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"(Fallback Story) Once upon a time, there was a doodle that became a magical adventure. [Error: {e}]"

# --- TTS with ElevenLabs ---
from elevenlabs import generate, save

def generate_tts_elevenlabs(text, voice="Rachel", filename="story.mp3"):
    try:
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v1"
        )
        save(audio, filename)
        return filename
    except Exception as e:
        st.warning(f"TTS generation failed: {e}")
        return None

# --- PDF Creation ---
def create_pdf(story_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, story_text)
    pdf_path = "storybook.pdf"
    pdf.output(pdf_path)
    return pdf_path

# --- Main Storybook Logic ---
if st.button("✨ Generate Storybook & Narration"):
    captions = []

    if uploaded_files:
        for f in uploaded_files:
            captions.append(f"A doodle of {os.path.basename(f.name)}")
    elif drawn_image:
        img_bytes = io.BytesIO()
        drawn_image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        detect_prompt = """
        You are an art teacher for kids.
        Look at this doodle and guess what object it represents (like star, moon, sun, house, tree, etc).
        Answer in 1-3 words only.
        """
        detect_response = text_model.generate_content([detect_prompt, {"mime_type": "image/png", "data": img_bytes}])
        object_name = detect_response.text.strip()

        captions.append(f"A child’s doodle of {object_name}")
    elif typed_description:
        captions.append(typed_description)
    else:
        st.warning("Please upload, draw, or describe something!")
        st.stop()

    # Generate Story
    story = generate_story(captions, theme)
    st.subheader("📖 Generated Story")
    st.write(story)

    # Generate TTS narration
    tts_file = generate_tts_elevenlabs(story, voice=voice, filename="story.mp3")
    if tts_file:
        st.audio(tts_file, format="audio/mp3")
        st.download_button("📥 Download Story Narration (MP3)", tts_file, file_name="story.mp3")

    # Create downloadable PDF
    pdf_file = create_pdf(story)
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Storybook (PDF)", f, file_name="storybook.pdf")
