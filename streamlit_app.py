import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from fpdf import FPDF
import google.generativeai as genai
import io
import os

# 🔑 Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Main text model (fast + supports multimodal)
text_model = genai.GenerativeModel("models/gemini-2.5-flash")

# Optional image generation model
image_model = genai.GenerativeModel("models/imagen-4.0-fast-generate-001")

st.set_page_config(page_title="StoryCraft AI", layout="wide")

st.title("📚 StoryCraft AI – AI Storybook Generator")
st.markdown("Turn kids’ messy doodles, drawings, or text into magical AI-generated stories!")

# --- Input Options ---
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
        width=300,
        height=300,
        drawing_mode="freedraw",
        key="canvas"
    )
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

# --- Story Generation ---
def generate_story(captions, theme="Fantasy"):
    prompt = f"Write a short children's story in a {theme} style based on these scenes:\n"
    for i, cap in enumerate(captions, 1):
        prompt += f"Scene {i}: {cap}\n"

    # Add theme-specific instructions
    if theme == "Moral":
        prompt += "\nMake sure the story ends with a clear moral life lesson for kids."
    elif theme == "Islamic":
        prompt += "\nKeep the story child-friendly with Islamic values: honesty, kindness, respect, dua, helping parents, etc."

    try:
        response = text_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"(Fallback Story) Once upon a time, there was a doodle that became a magical adventure. [Error: {e}]"

# --- Illustration Generation ---
def generate_illustration(scene_text, idx):
    try:
        response = image_model.generate_content([scene_text], stream=True)
        response.resolve()
        img_data = response.images[0]
        img = Image.open(io.BytesIO(img_data))
        return img
    except Exception as e:
        st.warning(f"Illustration for scene {idx} failed: {e}")
        return None

# --- PDF Creation ---
def create_pdf(images, story_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    story_pages = story_text.split("\n")
    for i, img in enumerate(images):
        pdf.add_page()
        img_path = f"temp_{i}.png"
        img.save(img_path)
        pdf.image(img_path, x=10, y=20, w=90)
        os.remove(img_path)

        pdf.set_font("Arial", size=12)
        pdf.set_xy(110, 20)
        pdf.multi_cell(90, 10, story_pages[i] if i < len(story_pages) else "")

    pdf_path = "storybook.pdf"
    pdf.output(pdf_path)
    return pdf_path

# --- Main ---
if st.button("✨ Generate Storybook"):
    captions = []

    if uploaded_files:
        for f in uploaded_files:
            img = Image.open(f).convert("RGB")
            captions.append(f"A doodle of {os.path.basename(f.name)}")
    elif drawn_image:
        captions.append("A child’s doodle drawing (messy but creative!)")
    elif typed_description:
        captions.append(typed_description)
    else:
        st.warning("Please upload, draw, or describe something!")
        st.stop()

    # Generate story
    story = generate_story(captions, theme)
    st.subheader("Generated Story")
    st.write(story)

    # Collect or generate images
    images = []
    if uploaded_files:
        images = [Image.open(f).convert("RGB") for f in uploaded_files]
    elif drawn_image:
        images = [drawn_image]
    elif typed_description:
        # Optional: generate illustrations
        st.info("Generating AI illustrations for your story...")
        for i, scene in enumerate(story.split("\n"), 1):
            img = generate_illustration(scene, i)
            if img:
                images.append(img)

    if images:
        pdf_file = create_pdf(images, story)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Storybook (PDF)", f, file_name="storybook.pdf")
