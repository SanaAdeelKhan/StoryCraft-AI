📚 StoryCraft AI – AI Storybook Generator

Turn messy kids’ doodles, classroom sketches, or personal photos into a magical AI-powered storybook ✨

🚀 Project Idea

StoryCraft AI is a platform where users can upload their own drawings, doodles, or photos, and the system will automatically generate a storybook with text + images in a creative layout.

🎨 How it Works

Upload Pictures / Doodles – Users upload one or more pictures (including messy kid drawings ✏️🖍️).

Choose Theme & Style – Fantasy, space adventure, detective, comedy, etc.

AI Generates Story – A connected storyline is written, inspired by the uploaded images or doodle descriptions.

Design the Book – Each page places the picture on one side and the text/story on the other.

Download as PDF – Users can save or print their personalized storybook.

## 🖍️ Sample Doodles → Storybook

Here’s how messy kids’ doodles transform into magical stories:

| Uploaded Doodle | AI Storybook Page |
|-----------------|-------------------|
| ![Doodle 1](samples/doodle1.png) | “Once upon a time, a flying cat explored the skies...” |
| ![Doodle 2](samples/doodle2.png) | “Deep in the forest, two smiling suns guided the hero...” |
| ![Doodle 3](samples/doodle3.png) | “A brave fish jumped out of the water to save its friends...” |

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/1eea18eb-a4da-4655-89c7-0de30a61195c" />

✨ Extra Features (Future Roadmap)

🖌️ AI-enhanced illustrations – Turn doodles into polished digital art.

🎤 AI voice narration – Listen to the story like an audiobook.

🌍 Translations – Generate storybooks in multiple languages.

🎲 Custom endings – Kids can pick different endings for their story.

💡 Why It’s Cool

👩‍👧 Parents can turn kids’ messy doodles into magical storybooks.

👩‍🏫 Teachers can make creative classroom content quickly.

👦 Kids get to imagine, create, and read their own stories.

🎁 Makes a fun and personalized gift idea.

🛠️ Tech Stack

Frontend / UI → Streamlit
 (or Gradio if Hugging Face Space).

Image Captioning → BLIP (Salesforce/blip-image-captioning-base).

Story Generation → Lightweight LLM (Flan-T5 or DistilGPT2 for free CPU usage).

PDF Export → FPDF + Pillow.

📂 Files in Repo

StoryCraft-AI/
│
├── app.py
├── requirements.txt
├── README.md
└── samples/
    ├── doodle1.png
    ├── doodle2.png
    ├── doodle3.png

🌐 Deployment

Fork/clone this repo.

Install dependencies:

pip install -r requirements.txt


Run locally:

streamlit run app.py


Deploy on Streamlit Cloud or Hugging Face Spaces.

🔥 With StoryCraft AI, even the messiest doodles become beautiful adventures kids can keep forever.
