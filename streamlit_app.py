import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from fpdf import FPDF
from PIL import Image
import os

st.set_page_config(page_title="StoryCraft AI", page_icon="📚")

# Load lightweight models
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-small")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-small")
story_gen = pipeline("text-generation", model="sshleifer/tiny-gpt2")

def generate_caption(image):
    image = Image.open(image).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_length=50)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def generate_story(captions, theme="fantasy"):
    prompt = f"Write a short children's story in a {theme} style connecting these scenes:\n"
    for i, cap in enumerate(captions, 1):
        prompt += f"Scene {i}: {cap}\n"
    output = story_gen(prompt, max_length=200, do_sample=True, temperature=0.7)
    story = output[0]["generated_text"]
    return story

def create_pdf(images, story_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    story_pages = story_text.split("\n")

    for i, img in enumerate(images):
        pdf.add_page()
        img_path = f"temp_{i}.png"
        Image.open(img).save(img_path)
        pdf.image(img_path, x=10, y=20, w=90)
        os.remove(img_path)

        pdf.set_font("Arial", size=12)
        pdf.set_xy(110, 20)
        pdf.multi_cell(90, 10, story_pages[i] if i < len(story_pages) else "")

    pdf_path = "storybook.pdf"
    pdf.output(pdf_path)
    return pdf_path

st.title("📚 StoryCraft AI – AI Storybook Generator")
st.write("Turn messy kids' doodles, drawings, or typed descriptions into a fun AI-generated storybook!")

uploaded_images = st.file_uploader("Upload Images", type=["jpg", "png"], accept_multiple_files=True)
theme = st.selectbox("Choose Theme", ["fantasy", "adventure", "mystery", "comedy"])
doodle_text = st.text_area("Or describe your doodle if no image uploaded:")

if st.button("Generate Storybook"):
    if uploaded_images:
        captions = [generate_caption(img) for img in uploaded_images]
        images = uploaded_images
    else:
        captions = [doodle_text] if doodle_text else ["A blank page"]
        images = []

    story = generate_story(captions, theme)
    if images:
        pdf_file = create_pdf(images, story)
        st.download_button("Download Storybook PDF", open(pdf_file, "rb"), file_name="storybook.pdf")
    st.subheader("Generated Story:")
    st.text_area("Story", story, height=300)
