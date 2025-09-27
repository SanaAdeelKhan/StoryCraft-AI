import streamlit as st
import google.generativeai as genai
import os

# 🔑 Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 👉 Debug: check available models
try:
    from google.generativeai import list_models
    available = list_models()
    st.sidebar.write("✅ Available models:", [m.name for m in available])
except Exception as e:
    st.sidebar.write("⚠️ Could not list models:", str(e))
