import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from fpdf import FPDF
import google.generativeai as genai
import io
import os
import re
from elevenlabs import generate, set_api_key

# --- Setup ---
st.set_page_config(
    page_title="StoryCraft AI",
    layout="wide",
    page_icon="📚"
)

# --- Styles ---
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #ffecd2, #fcb69f, #ff9a9e, #fad0c4);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background: radial-gradient(circle, rgba(255,255,255,0.4) 1px, transparent 1px);
        background-size: 20px 20px;
        animation: sparkle 3s linear infinite;
    }
    @keyframes sparkle {
        0% { background-position: 0 0; }
        100% { background-position: 20px 20px; }
    }
    .stButton>button {
        background-color: #ff77a9;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, background-color 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #ff5599;
    }
    .stTextArea>textarea {
        background-color: #fff8dc;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }
    h1, h2, h3 {
        color: #4b0082;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- Logo ---
logo_path = "storycraft_logo.png"
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    st.image(logo_img, width=150, caption="StoryCraft AI Logo")

st.title("📚 StoryCraft AI – Magical Storybook Generator")

# --- API Setup ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
text_model = genai.GenerativeModel("models/gemini-2.5-flash")

set_api_key(os.getenv("ELEVENLABS_API_KEY"))

st.markdown("Turn kids’ doodles, drawings, or descriptions into magical AI stories — and listen to them!")

# --- Input Options ---
st.sidebar.header("Choose Input Method")
option = st.sidebar.radio("Select how to start:", ["Upload Images", "Draw a Doodle", "Type Description"])

uploaded_files = []
drawn_image = None
typed_description = None

clear_canvas = st.sidebar.button("🧹 Clear Canvas")
if clear_canvas:
    st.session_state["canvas_cleared"] = True

if option == "Upload Images":
    uploaded_files = st.file_uploader("Upload doodles or drawings", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

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
theme = st.selectbox("Choose Story Theme", ["Adventure", "Comedy", "Fantasy", "Friendship", "Mystery", "Moral", "Islamic"], index=0)

# --- Helpers ---
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

def short_story_name(story_text):
    words = re.findall(r'\w+', story_text)
    return " ".join(words[:5]) if words else "storybook"

def safe_filename(text):
    filename = re.sub(r'\W+', '_', text.lower()).strip("_")
    return f"{filename}_storybook.pdf"

def create_pdf(story_text, short_name, doodle_path=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path)
    pdf.set_font("DejaVu", size=16)

    # Story Title in PDF
    pdf.cell(0, 10, short_name, ln=True, align="C")
    pdf.ln(5)

    if doodle_path:
        try:
            pdf.image(doodle_path, w=120)
            pdf.ln(5)
        except Exception as e:
            print(f"Error adding doodle to PDF: {e}")

    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, story_text)

    pdf_path = safe_filename(short_name)
    pdf.output(pdf_path)
    return pdf_path

def text_to_speech(text, voice_name="Rachel"):
    try:
        audio = generate(text=text, voice=voice_name, model="eleven_multilingual_v1")
        return audio
    except Exception as e:
        st.error(f"TTS generation failed: {e}")
        return None

# --- Main Logic ---
if st.button("✨ Generate Storybook with TTS"):
    captions = []
    base_name = "storybook"
    doodle_path = None

    if uploaded_files:
        for f in uploaded_files:
            captions.append(f"A doodle of {os.path.basename(f.name)}")
        base_name = os.path.splitext(os.path.basename(uploaded_files[0].name))[0]
        doodle_path = f"{base_name}_upload.png"
        with open(doodle_path, "wb") as f:
            f.write(uploaded_files[0].getbuffer())

    elif drawn_image:
        img_bytes = io.BytesIO()
        drawn_image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        detect_prompt = """
        You are an art teacher for kids.
        Look at this doodle and guess what object it represents (like star, moon, sun, house, tree, etc).
        Answer in 1-3 words only.
        """
        try:
            detect_response = text_model.generate_content([detect_prompt, {"mime_type": "image/png", "data": img_bytes}])
            object_name = detect_response.text.strip()
        except Exception as e:
            object_name = "Unknown"

        captions.append(f"A child’s doodle of {object_name}")
        base_name = object_name.replace(" ", "_")
        doodle_path = f"{base_name}_doodle.png"
        drawn_image.save(doodle_path)

    elif typed_description:
        captions.append(typed_description)
        base_name = typed_description[:20].replace(" ", "_")
    else:
        st.warning("Please upload, draw, or describe something!")
        st.stop()

    story = generate_story(captions, theme)
    st.subheader("📖 Generated Story")
    st.write(story)

    short_name = short_story_name(story)

    st.subheader("🔊 Story Audio Playback")
    audio_data = text_to_speech(story, voice_name="Rachel")
    if audio_data:
        st.audio(audio_data, format="audio/mp3")

    pdf_file = create_pdf(story, short_name, doodle_path)
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Storybook (PDF)", f, file_name=pdf_file)
