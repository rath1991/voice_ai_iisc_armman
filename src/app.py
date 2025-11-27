# app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64, io, soundfile as sf
from dotenv import load_dotenv

# Load environment variables from .env file
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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
