# app.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import io
import os
import tempfile
import shutil
from typing import Optional

# NOTE: If running locally and experiencing "RuntimeError: Form data requires python-multipart",
# please install it using: pip install python-multipart
# Local modules
from tts_engine import TTSEngine
from config_loader import CONFIG
# CRITICAL IMPORTS from styles.py
from styles import SUPPORTED_LANGS, get_speaker_name, resolve_effective_lang 
from audio_style_extractor import analyze_ref_audio
# REMOVED: from lang_manager import detect_text_language 

app = FastAPI(
    title="Voice tech for all: TTS Synthesizer",
    description="Implements the required API specification for style transfer TTS.",
    version="2.1.0",
)

# Global TTS engine
print("[Server] Initializing TTS Engine...")
tts_engine = TTSEngine()
# Ensure sample rate is available from engine object
# We use setattr for safety, accessing the model config directly where possible
setattr(tts_engine, 'default_sample_rate', getattr(tts_engine.model.config, "sampling_rate", CONFIG.get("sample_rate", 24000)))
print("[Server] Engine Ready.")


# --- Helper Functions for API Spec Adherence ---

def _validate_language_spec(lang: str) -> str:
    """
    Validates the language string (which might be a full name like 'kannada') 
    and returns the 2-letter code (e.g., 'kn').
    """
    valid_codes = set(SUPPORTED_LANGS.keys())
    # Create a map from full name (lowercase) to 2-letter code
    # This handles full names like 'bhojpuri' or 'kannada'
    reverse_map = {v.lower(): k for k, v in SUPPORTED_LANGS.items()}
    
    lang_lower = lang.lower()
    
    if lang_lower in valid_codes:
        return lang_lower # Already a valid code (e.g., 'gu')
    elif lang_lower in reverse_map:
        return reverse_map[lang_lower] # Map full name to code (e.g., 'kannada' -> 'kn')
    
    raise HTTPException(status_code=400, detail=f"Unsupported language '{lang}'.")

def _validate_text_spec(text: str, lang_code: str):
    """Ensure English text is lowercase, as required by the specification."""
    if lang_code == 'en' and text != text.lower():
        raise HTTPException(
            status_code=400,
            detail="For English, the input text must be lowercase, as required by the specification."
        )
    return text

def _build_caption_from_ref_spec(style: dict, lang_code: str) -> str:
    """
    Builds the high-quality, named-speaker prompt using only the required inputs (lang_code and style).
    This logic is based on the robust transfer demonstrated in test_style_transfer.py.
    """
    # 1. Determine Gender from Audio Analysis
    detected_gender = style.get("gender_hint", "female")
    
    # 2. Select Speaker (e.g., 'Neha' for gu)
    # The language code controls both accent and speaker anchor
    base_accent_lang = resolve_effective_lang(lang_code) 
    best_speaker = get_speaker_name(base_accent_lang, detected_gender)
    
    # 3. Get Full Language Name for the prompt (e.g., 'Gujarati')
    language_full_name = SUPPORTED_LANGS.get(lang_code, "Indian language")

    # 4. Map Style Attributes (Pitch/Speed)
    pitch_val = style.get("pitch", "medium")
    pitch_map = {
        "low": "with a slightly deep, warm pitch",
        "high": "with a slightly high, clear pitch",
        "medium": "with a natural, balanced pitch"
    }
    pitch_desc = pitch_map.get(pitch_val, "with a natural, balanced pitch")

    speed_val = style.get("speed", "medium")
    speed_map = {
        "slow": "at a slow, unhurried pace",
        "fast": "at a slightly fast, energetic pace",
        "medium": "at a moderate, natural pace"
    }
    speed_desc = speed_map.get(speed_val, "at a moderate, natural pace")
    
    # 5. Assemble the final prompt
    caption = (
        f"{best_speaker} speaks {language_full_name} {pitch_desc} and {speed_desc}. "
        f"The recording is of very high quality, very clear audio, close up, with almost no background noise."
    )
    
    return caption


# --- API Endpoint (Matching Specification) ---

@app.post("/Get_Inference")
async def Get_Inference(
    # Mandatory parameter 1: The input text
    text: str = Form(..., description="The input text to be converted into speech. English text must be lowercase."),
    # Mandatory parameter 2: The language
    lang: str = Form(..., description="The language of the input text."),
    # Mandatory parameter 3: The reference WAV file
    speaker_wav: UploadFile = File(..., description="A reference WAV file representing the speaker's voice."),
):
    """
    GET/Get_Inference (Implemented as POST for file upload)
    Generates speech audio using the provided text, language, and reference speaker style.
    """
    
    # 1. Validation and Language Code Resolution (Handles 'kannada' -> 'kn')
    lang_code = _validate_language_spec(lang)
    validated_text = _validate_text_spec(text, lang_code)
    
    caption = None
    tmp_path = None
    
    # 2. Handle File Upload and Analysis (Mandatory Speaker WAV)
    
    # Create temp file
    suffix = os.path.splitext(speaker_wav.filename or "file.wav")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name
        # Copy uploaded file stream into the temporary file
        shutil.copyfileobj(speaker_wav.file, tmp)
    
    try:
        # 3. Analyze Audio (extracting style and gender)
        print(f"[Server] Analyzing reference audio for style and gender...")
        style_attrs = analyze_ref_audio(tmp_path)
        
        # 4. Build Robust Caption (Style Transfer)
        # lang_code is used here for both text normalization AND speaker/accent selection
        caption = _build_caption_from_ref_spec(style=style_attrs, lang_code=lang_code)
        print(f"[Server] Final Caption: {caption}")

    except Exception as e:
        print(f"[Error] Audio analysis or caption building failed: {e}")
        # Per spec, speaker_wav is Mandatory. If analysis fails, we return a 500 error.
        raise HTTPException(status_code=500, detail=f"Reference audio analysis failed: {e}. Please ensure the speaker_wav file is a valid, high-quality audio recording.")

    finally:
        # Clean up the temporary file
        if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)

    # 5. Synthesis
    try:
        audio_bytes = tts_engine.synthesize_with_description(
            text=validated_text,
            language=lang_code, 
            description=caption,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

    # 6. Response (Matching Spec: 200 OK, Content-Type: audio/wav)
    buf = io.BytesIO(audio_bytes)
    buf.seek(0)
    
    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'attachment; filename="synthesized_speech.wav"',
            "X-Language-Code": lang_code
        },
    )


@app.get("/health")
def health_check():
    # Keep standard health check
    return {"status": "ok", "model_id": CONFIG["model_id"], "sample_rate": tts_engine.default_sample_rate}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)