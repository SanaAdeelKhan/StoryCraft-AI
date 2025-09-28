
# 📚 StoryCraft AI – AI Storybook Generator

Turn messy kids’ doodles, classroom sketches, or personal photos into a magical AI-powered storybook ✨

---

## 🚀 Project Overview

**StoryCraft AI** is an interactive web application that transforms children’s doodles, drawings, or text descriptions into magical storybooks — complete with illustrated PDFs and AI-generated narration.

This project was created by **Team Green** for the **CodeFusion Hackathon 2025** —
**Track 2️⃣ Generative AI Projects**: *Create something futuristic and fun with Gen AI!* 🤖

---

### 🎯 Hackathon Context

🔥 **CodeFusion Hackathon 2025**:
A 48-hour innovation challenge where creativity, collaboration, and technology merge to create extraordinary projects. This track encouraged building futuristic and fun projects powered by Generative AI.

**StoryCraft AI** embraces this spirit by merging art, storytelling, and AI to create an immersive, playful experience for children, making learning and creativity more accessible.

---

## 🌟 Features

- **Multiple Input Methods**

  - Upload doodles or drawings
  - Draw directly on a canvas
  - Type a scene description
- **Dynamic Story Generation**

  - AI-generated stories based on images or descriptions
  - Multiple story themes:
    - Adventure
    - Comedy
    - Fantasy
    - Friendship
    - Mystery
    - Moral
    - Islamic
- **Text-to-Speech Integration**

  - Narration with realistic AI voices
- **Custom Storybook PDF**

  - Story title, illustrations, and full text
  - Auto-generated story names for file naming
- **Fun & Interactive UI**

  - Colorful gradient background with sparkle animation
  - Child-friendly design

---

## 📂 Project Structure


StoryCraft-AI/

│

├── fonts/

│   └── DejaVuSans.ttf

├── storycraft_logo.png

├── streamlit_app.py

├── requirements.txt

├── README.md

└── samples/

├── doodle1.png

├── doodle2.png

├── doodle3.png



## 📌 How it Works

1. Choose an input method from the sidebar:
   - Upload an image
   - Draw directly
   - Type a description
2. Select a story theme.
3. Click **"Generate Storybook with TTS"**.
4. View the AI-generated story.
5. Listen to the narrated version.
6. Download the story as a PDF with illustrations.

---

## 🎨 Themes Available

- Adventure
- Comedy
- Fantasy
- Friendship
- Mystery
- Moral
- Islamic

---

## 💻 Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/SanaAdeelKhan/StoryCraft-AI.git
cd StoryCraft-AI
```


2. **Create a virtual environment**

<pre class="overflow-visible!" data-start="2756" data-end="2787"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m venv venv
</span></span></code></div></div></pre>

3. **Activate the virtual environment**

* Windows:

<pre class="overflow-visible!" data-start="2840" data-end="2881"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-powershell"><span>.\venv\Scripts\activate
</span></code></div></div></pre>

* Mac/Linux:

<pre class="overflow-visible!" data-start="2895" data-end="2931"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>source</span><span> venv/bin/activate
</span></span></code></div></div></pre>

4. **Install dependencies**

<pre class="overflow-visible!" data-start="2961" data-end="3004"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
</span></span></code></div></div></pre>

5. **Set API keys**

<pre class="overflow-visible!" data-start="3026" data-end="3147"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>export</span><span> GOOGLE_API_KEY=</span><span>"your_google_generative_ai_api_key"</span><span>
</span><span>export</span><span> ELEVENLABS_API_KEY=</span><span>"your_elevenlabs_api_key"</span><span>
</span></span></code></div></div></pre>

For Windows PowerShell:

<pre class="overflow-visible!" data-start="3172" data-end="3295"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-powershell"><span>setx GOOGLE_API_KEY "your_google_generative_ai_api_key"
setx ELEVENLABS_API_KEY "your_elevenlabs_api_key"
</span></code></div></div></pre>

6. **Run the app**

<pre class="overflow-visible!" data-start="3316" data-end="3358"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>streamlit run streamlit_app.py
</span></span></code></div></div></pre>

Open the link provided in the terminal to access the app.



## 📷 Screenshots & Demos

![Example Screenshot](samples/doodle1.png)

*(Add more screenshots or GIF demos here)*

---

## ⚙ Requirements (`requirements.txt`)

<pre class="overflow-visible!" data-start="3584" data-end="3828"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>streamlit==1.25.0
streamlit-drawable-canvas==0.9.3
Pillow==9.5.0
fpdf2==2.8.4
google-generativeai==0.8.5
elevenlabs==0.2.9
numpy==1.26.4
pandas==2.3.2
typing_extensions==4.15.0
rich<14
markdown-it-py==4.0.0
pygments==2.19.2
mdurl==0.1.2
</span></span></code></div></div></pre>

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

### 🏆 Hackathon Credit

**Team Green** built this project for the  **CodeFusion Hackathon 2025** , competing in the Generative AI Projects track — *Create something futuristic and fun with Gen AI!* 🤖
