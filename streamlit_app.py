import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from fpdf import FPDF
import google.generativeai as genai
import io
import os

# 🔑 Configure Gemini API (you must set GOOGLE_API_KEY in Streamlit secrets or env)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")  # ✅ Use gemini-pro for text generation

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

# --- Theme Selection ---
theme = st.selectbox(
    "Choose Story Theme", 
    ["Adventure", "Comedy", "Fantasy", "Friendship", "Mystery", "Moral", "Islamic"], 
    index=0
)

# --- Story Generation ---
def generate_story(captions, theme="Fantasy"):
    # Base prompt
    prompt = f"Write a short children's story in a {theme} style based on these scenes:\n"
    for i, cap in enumerate(captions, 1):
        prompt += f"Scene {i}: {cap}\n"

    # Add special instructions for Moral / Islamic
    if theme.lower() == "moral":
        prompt += "\nMake sure the story ends with a clear moral or life lesson suitable for children."
    elif theme.lower() == "islamic":
        prompt += (
            "\nWrite the story with Islamic values (honesty, kindness, respect, dua, helping others). "
            "Keep it child-friendly, simple, and inspiring."
        )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"(Fallback Story) Once upon a time, there was a doodle that became a magical adventure. [Error: {str(e)}]"

# --- PDF Creation ---
def create_pdf(images, story_text, theme):
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

    # --- Add Moral of the Story if theme is Moral / Islamic ---
    if theme.lower() in ["moral", "islamic"]:
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        pdf.multi_cell(0, 10, "✨ Moral of the Story:")
        pdf.set_font("Arial", size=12)
        if theme.lower() == "moral":
            pdf.multi_cell(0, 10, "Always remember: every story has a lesson. Be kind, honest, and helpful!")
        else:
            pdf.multi_cell(0, 10, "Good deeds, honesty, and dua always bring blessings in life.")

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

    # Collect images
    images = []
    if uploaded_files:
        images = [Image.open(f).convert("RGB") for f in uploaded_files]
    elif drawn_image:
        images = [drawn_image]

    if images:
        pdf_file = create_pdf(images, story, theme)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Storybook (PDF)", f, file_name="storybook.pdf")
