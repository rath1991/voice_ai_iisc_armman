# app.py

from dotenv import load_dotenv

load_dotenv()  # if you have HF_TOKEN etc.

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

import base64
import io
import os
import tempfile

from tts_engine import TTSEngine
from config_loader import CONFIG
from styles import SUPPORTED_LANGS
from audio_style_extractor import analyze_ref_audio, build_caption as build_ref_caption


app = FastAPI(
    title="Indic Maternal Health TTS",
    description=(
        "Multilingual, multi-speaker TTS for English + Gujarati (and more), "
        "with preset styles and reference-audio-based style transfer."
    ),
    version="1.0.0",
)

# Global TTS engine
tts_engine = TTSEngine()


class SynthesisRequest(BaseModel):
    text: str
    language: str
    style: str
    speaker_gender: str = "female"


def _validate_language(lang: str) -> None:
    supported_codes = set(SUPPORTED_LANGS.keys()) if isinstance(SUPPORTED_LANGS, dict) else set(SUPPORTED_LANGS)
    if lang not in supported_codes:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{lang}'. Supported: {sorted(supported_codes)}"
        )


@app.post("/synthesize", response_model=dict)
def synthesize(req: SynthesisRequest):
    """
    JSON-based synthesis using preset style + gender.
    Returns base64-encoded WAV audio.
    """
    _validate_language(req.language)

    try:
        audio_bytes = tts_engine.synthesize_with_style(
            text=req.text,
            language=req.language,
            style=req.style,
            speaker_gender=req.speaker_gender,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {e}")

    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "audio_base64": audio_b64,
        "sample_rate": tts_engine.sample_rate,
        "language": req.language,
        "style": req.style,
        "speaker_gender": req.speaker_gender,
    }


@app.post("/synthesize_wav")
def synthesize_wav(req: SynthesisRequest):
    """
    JSON-based synthesis using preset style + gender.
    Returns a streaming WAV response (audio/wav).
    """
    _validate_language(req.language)

    try:
        audio_bytes = tts_engine.synthesize_with_style(
            text=req.text,
            language=req.language,
            style=req.style,
            speaker_gender=req.speaker_gender,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {e}")

    buf = io.BytesIO(audio_bytes)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'attachment; filename="tts_output.wav"'
        },
    )


@app.post("/synthesize_from_ref")
async def synthesize_from_ref(
    text: str = Form(...),
    language: str = Form("gu"),
    fallback_style: str = Form("empathetic_motherly"),
    fallback_gender: str = Form("female"),
    ref_audio: UploadFile = File(None),
):
    """
    Style-transfer mode:

    - If ref_audio is provided:
        * Save temp WAV
        * Analyze style (pitch, speed, energy, noisiness)
        * Build Parler caption
        * Synthesize with description
    - If ref_audio is missing or analysis fails:
        * Fallback to preset style+gender
    """
    _validate_language(language)

    caption = None

    if ref_audio is not None:
        # Save to a temporary file
        suffix = os.path.splitext(ref_audio.filename or ".wav")[-1]
        if suffix.lower() not in [".wav", ".flac", ".mp3", ".ogg"]:
            suffix = ".wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            tmp.write(await ref_audio.read())

        try:
            style = analyze_ref_audio(tmp_path)
            caption = build_ref_caption(style, language)
        except Exception as e:
            # Log and continue to fallback
            print(f"[WARN] Reference style analysis failed: {e}")
            caption = None
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    try:
        if caption:
            # Use reference-audio caption
            audio_bytes = tts_engine.synthesize_with_description(
                text=text,
                language=language,
                description=caption,
            )
        else:
            # Fallback: preset style
            audio_bytes = tts_engine.synthesize_with_style(
                text=text,
                language=language,
                style=fallback_style,
                speaker_gender=fallback_gender,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {e}")

    buf = io.BytesIO(audio_bytes)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'attachment; filename="tts_ref_style.wav"'
        },
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "model_id": CONFIG["model_id"], "sample_rate": tts_engine.sample_rate}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
