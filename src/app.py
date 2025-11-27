# app.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import base64, io, soundfile as sf
from dotenv import load_dotenv

load_dotenv()

from tts_engine import TTSEngine
from config_loader import CONFIG
from styles import SUPPORTED_LANGS


class SynthesisRequest(BaseModel):
    text: str
    language: str = "hi"
    style: str = "empathetic_motherly"
    speaker_gender: str = "female"
    audio_format: str = "wav"


class SynthesisResponse(BaseModel):
    audio_base64: str
    sample_rate: int
    language: str
    style: str
    duration_ms: float


app = FastAPI(
    title="TTS Synthesis API",
    description="Text-to-Speech API with multilingual support and style variations",
    version="1.0.0"
)
engine = TTSEngine()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/synthesize", response_model=SynthesisResponse)
def synthesize_api(req: SynthesisRequest):
    if req.language not in SUPPORTED_LANGS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language {req.language}. Supported: {list(SUPPORTED_LANGS.keys())}"
        )

    wav, sr = engine.synthesize(
        text=req.text,
        lang_code=req.language,
        style=req.style,
        speaker_gender=req.speaker_gender
    )

    buf = io.BytesIO()
    sf.write(buf, wav, sr, format="WAV")
    audio_bytes = buf.getvalue()
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    duration_ms = (len(wav) / sr) * 1000.0

    return SynthesisResponse(
        audio_base64=audio_b64,
        sample_rate=sr,
        language=req.language,
        style=req.style,
        duration_ms=duration_ms
    )


@app.post("/synthesize_wav")
def synthesize_wav_post(req: SynthesisRequest):
    """
    Returns raw WAV audio as HTTP response so the browser can play it.
    POST endpoint - accepts JSON body.
    """
    if req.language not in SUPPORTED_LANGS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language {req.language}. Supported: {list(SUPPORTED_LANGS.keys())}"
        )

    wav, sr = engine.synthesize(
        text=req.text,
        lang_code=req.language,
        style=req.style,
        speaker_gender=req.speaker_gender
    )

    buf = io.BytesIO()
    sf.write(buf, wav, sr, format="WAV")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={
            # inline → browser tries to play;
            # attachment → browser downloads as file.
            "Content-Disposition": 'inline; filename="tts_output.wav"'
        }
    )


@app.get("/synthesize_wav")
def synthesize_wav_get(
    text: str = Query(..., description="Text to synthesize"),
    language: str = Query("hi", description="Language code"),
    style: str = Query("empathetic_motherly", description="Style description"),
    speaker_gender: str = Query("female", description="Speaker gender (male or female)")
):
    """
    Returns raw WAV audio as HTTP response. Automatically downloads the file.
    GET endpoint - accepts query parameters. Useful for direct browser access.
    """
    if language not in SUPPORTED_LANGS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language {language}. Supported: {list(SUPPORTED_LANGS.keys())}"
        )

    wav, sr = engine.synthesize(
        text=text,
        lang_code=language,
        style=style,
        speaker_gender=speaker_gender
    )

    buf = io.BytesIO()
    sf.write(buf, wav, sr, format="WAV")
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="audio/wav",
        headers={
            # attachment → browser downloads as file automatically
            "Content-Disposition": 'attachment; filename="tts_output.wav"'
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
