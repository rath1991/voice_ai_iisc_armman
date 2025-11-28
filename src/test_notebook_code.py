# ============================================

# ============================================

# ============================================
# Cell 1: Setup and Imports
# ============================================
import os
import sys
from dotenv import load_dotenv
import soundfile as sf
import numpy as np
import IPython.display as ipd

# Load environment variables
load_dotenv()

# Import TTS engine
from tts_engine import TTSEngine
from config_loader import CONFIG

# ============================================
# Cell 2: Check Authentication
# ============================================
# Check for authentication token
hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")

if hf_token:
    print(f"✓ Found HF_TOKEN (length: {len(hf_token)})")
else:
    print("⚠️  WARNING: No HF_TOKEN found!")
    print("Please set HF_TOKEN environment variable or use .env file")
    print("You can also run: hf auth login")

# ============================================
# Cell 3: Initialize TTS Engine
# ============================================
print("Initializing TTS Engine...")
try:
    engine = TTSEngine()
    print("✓ TTS Engine initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize TTS Engine: {e}")
    raise

# ============================================
# Cell 4: Test Synthesis - Hindi
# ============================================
# Test with Hindi text
text = "नमस्ते, यह एक परीक्षण है।"
language = "hi"
style = "empathetic_motherly"
speaker_gender = "female"

print(f"Text: {text}")
print(f"Language: {language}")
print(f"Style: {style}")
print(f"Gender: {speaker_gender}")
print("\nSynthesizing...")

audio, sample_rate = engine.synthesize(
    text=text,
    lang_code=language,
    style=style,
    speaker_gender=speaker_gender
)

print(f"✓ Generated audio:")
print(f"  - Sample rate: {sample_rate} Hz")
print(f"  - Length: {len(audio)} samples")
print(f"  - Duration: {len(audio) / sample_rate:.2f} seconds")

# Save audio file
output_file = "test_hindi.wav"
sf.write(output_file, audio, sample_rate)
print(f"\n✓ Saved to {output_file}")

# ============================================
# Cell 5: Play Audio (Hindi)
# ============================================
# Play audio in notebook
ipd.Audio(audio, rate=sample_rate)

# ============================================
# Cell 6: Test Synthesis - English
# ============================================
# Test with English text
text = "Hello, this is a test of the text to speech system."
language = "en"
style = "neutral_nurse"
speaker_gender = "female"

print(f"Text: {text}")
print(f"Language: {language}")
print(f"Style: {style}")
print(f"Gender: {speaker_gender}")
print("\nSynthesizing...")

audio, sample_rate = engine.synthesize(
    text=text,
    lang_code=language,
    style=style,
    speaker_gender=speaker_gender
)

print(f"✓ Generated audio:")
print(f"  - Sample rate: {sample_rate} Hz")
print(f"  - Length: {len(audio)} samples")
print(f"  - Duration: {len(audio) / sample_rate:.2f} seconds")

# Save audio file
output_file = "test_english.wav"
sf.write(output_file, audio, sample_rate)
print(f"\n✓ Saved to {output_file}")

# ============================================
# Cell 7: Play Audio (English)
# ============================================
# Play audio in notebook
ipd.Audio(audio, rate=sample_rate)

# ============================================
# Cell 8: Test Different Styles (Optional)
# ============================================
# Test different styles
text = "This is a test of different speaking styles."
language = "en"
styles = ["empathetic_motherly", "neutral_nurse", "urgent_alert", "friend_casual"]

for style in styles:
    print(f"\n--- Testing style: {style} ---")
    try:
        audio, sr = engine.synthesize(
            text=text,
            lang_code=language,
            style=style,
            speaker_gender="female"
        )
        output_file = f"test_{style}.wav"
        sf.write(output_file, audio, sr)
        print(f"✓ Saved to {output_file}")
        
        # Play audio
        display(ipd.Audio(audio, rate=sr))
    except Exception as e:
        print(f"✗ Error: {e}")

# ============================================
# Cell 9: Test Different Languages (Optional)
# ============================================
# Test different languages
test_languages = {
    "hi": "नमस्ते, मैं हिंदी में बोल रहा हूँ।",
    "en": "Hello, I am speaking in English.",
    "bn": "হ্যালো, আমি বাংলায় কথা বলছি।"
}

for lang_code, text in test_languages.items():
    print(f"\n--- Testing language: {lang_code} ---")
    print(f"Text: {text}")
    try:
        audio, sr = engine.synthesize(
            text=text,
            lang_code=lang_code,
            style="neutral_nurse",
            speaker_gender="female"
        )
        output_file = f"test_{lang_code}.wav"
        sf.write(output_file, audio, sr)
        print(f"✓ Saved to {output_file}")
        
        # Play audio
        display(ipd.Audio(audio, rate=sr))
    except Exception as e:
        print(f"✗ Error: {e}")

