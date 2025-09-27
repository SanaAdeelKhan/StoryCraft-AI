if st.button("✨ Generate Storybook"):
    with st.spinner("Generating story... 📖"):
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

        story = generate_story(captions, theme)

    st.subheader("📖 Generated Story")
    st.write(story)

    st.session_state["generated_story"] = story

# --- Separate TTS Button ---
if "generated_story" in st.session_state:
    if st.button("🔊 Generate & Play Story Audio"):
        with st.spinner("Generating speech... 🎙️"):
            audio_data = text_to_speech(st.session_state["generated_story"], voice_name="Rachel")
        if audio_data:
            st.audio(audio_data, format="audio/mp3")

    if st.button("📥 Download Storybook PDF"):
        pdf_file = create_pdf(st.session_state["generated_story"])
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f, file_name="storybook.pdf")
