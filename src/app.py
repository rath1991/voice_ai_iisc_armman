# app.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import base64
import io
import os
import tempfile
import shutil

# Local modules
from tts_engine import TTSEngine
from config_loader import CONFIG
from styles import SUPPORTED_LANGS, get_speaker_name
from audio_style_extractor import analyze_ref_audio, build_caption as build_ref_caption

app = FastAPI(
    title="Indic Maternal Health TTS",
    description="Multilingual TTS with Style Transfer & Specific Speaker Control",
    version="1.1.0",
)

# Initialize Engine Global
print("[Server] Initializing TTS Engine...")
tts_engine = TTSEngine()
print("[Server] Engine Ready.")

class SynthesisRequest(BaseModel):
    text: str
    language: str
    style: str
    speaker_gender: str = "female"

def _validate_language(lang: str):
    # Flatten dict keys if needed
    valid_keys = SUPPORTED_LANGS.keys() if isinstance(SUPPORTED_LANGS, dict) else SUPPORTED_LANGS
    if lang not in valid_keys:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")

@app.get("/health")
def health_check():
    return {
        "status": "ok", 
        "model": CONFIG["model_id"], 
        "device": str(tts_engine.device)
    }

@app.post("/synthesize", response_model=dict)
def synthesize(req: SynthesisRequest):
    """
    Standard synthesis using preset styles (e.g., 'empathetic_motherly').
    """
    _validate_language(req.language)
    try:
        audio_bytes = tts_engine.synthesize_with_style(
            text=req.text,
            language=req.language,
            style=req.style,
            speaker_gender=req.speaker_gender,
        )
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return {
            "audio_base64": audio_b64,
            "sample_rate": tts_engine.sample_rate
        }
    except Exception as e:
        print(f"[Error] Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize_wav")
def synthesize_wav(req: SynthesisRequest):
    """
    Returns audio/wav binary stream.
    """
    _validate_language(req.language)
    try:
        audio_bytes = tts_engine.synthesize_with_style(
            text=req.text,
            language=req.language,
            style=req.style,
            speaker_gender=req.speaker_gender,
        )
        return StreamingResponse(
            io.BytesIO(audio_bytes), 
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=output.wav"}
        )
    except Exception as e:
        print(f"[Error] WAV Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synthesize_from_ref")
async def synthesize_from_ref(
    text: str = Form(...),
    language: str = Form("gu"),
    fallback_style: str = Form("empathetic_motherly"),
    fallback_gender: str = Form("female"),
    ref_audio: UploadFile = File(None),
):
    """
    Style Transfer Endpoint:
    1. Analyzes uploaded audio (pitch, speed, gender).
    2. Identifies the best high-quality speaker (e.g., 'Neha' for Gujarati) matching that gender.
    3. Generates a prompt combining the Named Speaker + Extracted Style.
    """
    _validate_language(language)
    
    caption = None
    
    if ref_audio:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp_path = tmp.name
        
        try:
            # Write uploaded bytes to temp file
            with open(tmp_path, "wb") as buffer:
                shutil.copyfileobj(ref_audio.file, buffer)
            
            # 1. Analyze Audio
            print(f"[Server] Analyzing reference audio: {ref_audio.filename}")
            style_attrs = analyze_ref_audio(tmp_path)
            print(f"[Server] Extracted Attributes: {style_attrs}")

            # 2. Resolve Speaker Identity (Crucial for quality)
            # Use the gender detected from audio, falling back to form input
            detected_gender = style_attrs.get("gender_hint", fallback_gender)
            
            # Lookup best speaker name (e.g., 'Neha', 'Mary')
            best_speaker_name = get_speaker_name(language, detected_gender)
            print(f"[Server] Selected Base Speaker: {best_speaker_name}")

            # 3. Build Caption
            caption = build_ref_caption(style_attrs, language, speaker_name=best_speaker_name)
            print(f"[Server] Generated Caption: {caption}")

        except Exception as e:
            print(f"[Warning] Reference analysis failed: {e}")
            caption = None # Fallback triggers below
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    try:
        if caption:
            # Generate using the dynamic style-transfer caption
            audio_bytes = tts_engine.synthesize_with_description(
                text=text,
                language=language,
                description=caption
            )
        else:
            # Fallback to preset if no audio or analysis failed
            print("[Server] Using fallback style.")
            audio_bytes = tts_engine.synthesize_with_style(
                text=text,
                language=language,
                style=fallback_style,
                speaker_gender=fallback_gender
            )
            
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=ref_style_output.wav"}
        )

    except Exception as e:
        print(f"[Error] Ref Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)