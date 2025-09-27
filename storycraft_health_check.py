import sys
import time
import importlib
import os

print("🔍 Starting StoryCraft AI Health Check...\n")

start_time = time.time()

# 1. Python version check
print(f"Python Version: {sys.version}\n")

# 2. Check required packages
required_packages = [
    "streamlit",
    "Pillow",
    "fpdf",
    "streamlit_drawable_canvas",
    "google.generativeai",
    "elevenlabs"
]

print("Checking required packages...")
for pkg in required_packages:
    try:
        module = importlib.import_module(pkg)
        print(f"✅ {pkg} is installed (version: {getattr(module, '__version__', 'unknown')})")
    except ImportError:
        print(f"❌ {pkg} is NOT installed!")

print("\n")

# 3. Check API keys
print("Checking API keys...")
google_key = os.getenv("GOOGLE_API_KEY")
elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

print(f"Google API Key: {'SET ✅' if google_key else 'MISSING ❌'}")
print(f"ElevenLabs API Key: {'SET ✅' if elevenlabs_key else 'MISSING ❌'}\n")

# 4. Test ElevenLabs voice load
try:
    import elevenlabs.api
    import elevenlabs.utils
    print("Testing ElevenLabs voices load...")
    elevenlabs.api.set_api_key(elevenlabs_key)
    voice_list = elevenlabs.api.voices()
    print(f"✅ Loaded {len(voice_list)} voices successfully")
except Exception as e:
    print(f"❌ ElevenLabs voice load failed: {e}")

# 5. Test Google Gemini setup
try:
    import google.generativeai as genai
    genai.configure(api_key=google_key)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    print("Testing Google Gemini model...")
    test_resp = model.generate_content("Hello")
    print(f"✅ Gemini model working: {test_resp.text[:50]}...")
except Exception as e:
    print(f"❌ Google Gemini test failed: {e}")

# 6. Measure startup time
end_time = time.time()
print(f"\n⏱ Health check completed in {end_time - start_time:.2f} seconds")
