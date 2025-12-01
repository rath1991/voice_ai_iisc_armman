# audio_style_extractor.py

import numpy as np
import librosa


def analyze_ref_audio(audio_path: str) -> dict:
    """
    Analyse reference audio and return coarse style attributes:
    - pitch: low / medium / high (for internal use, we will soften this in caption)
    - speed: slow / medium / fast
    - energy: calm / neutral / expressive
    - gender_hint: male / female (from F0, best-effort)
    - noisiness: qualitative description
    """
    y, sr = librosa.load(audio_path, sr=None, mono=True)

    # --- Pitch (F0) ---
    try:
        f0 = librosa.yin(y, fmin=50, fmax=400)
        f0_valid = f0[f0 > 0]
        mean_f0 = float(np.median(f0_valid)) if len(f0_valid) else 180.0
    except Exception:
        mean_f0 = 180.0

    if mean_f0 < 130:
        pitch = "low"
    elif mean_f0 < 220:
        pitch = "medium"
    else:
        pitch = "high"

    # --- Tempo / speaking rate ---
    try:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    except Exception:
        tempo = 110.0

    if tempo < 90:
        speed = "slow"
    elif tempo < 130:
        speed = "medium"
    else:
        speed = "fast"

    # --- Energy / expressivity ---
    rms = librosa.feature.rms(y=y)[0]
    mean_rms = float(np.mean(rms))
    std_rms = float(np.std(rms))

    if mean_rms < 0.03 and std_rms < 0.02:
        energy = "calm"
    elif mean_rms < 0.06:
        energy = "neutral"
    else:
        energy = "expressive"

    # --- Gender hint from F0 (best-effort, not perfect) ---
    # Typical rough ranges:
    #   male:   ~80–165 Hz
    #   female: ~165–255 Hz
    if mean_f0 <= 160:
        gender_hint = "male"
    elif mean_f0 >= 180:
        gender_hint = "female"
    else:
        # ambiguous band → default to female (more common in your use-case)
        gender_hint = "female"

    # --- Noisiness via spectral flatness ---
    S = np.abs(librosa.stft(y))
    flatness = np.mean(librosa.feature.spectral_flatness(S=S))
    if flatness < 0.2:
        noisiness = "with almost no background noise"
    elif flatness < 0.4:
        noisiness = "with a bit of background noise"
    else:
        noisiness = "with noticeable background noise"

    return {
        "pitch": pitch,
        "speed": speed,
        "energy": energy,
        "gender_hint": gender_hint,
        "noisiness": noisiness,
    }


def build_caption(style: dict, language: str, gender_override: str | None = None) -> str:
    """
    Turn style attributes into a Parler-style description string.

    - Gender can be male/female based on reference OR overridden explicitly.
    - Pitch extremes are softened in wording to avoid super-boomy or squeaky voices.
    """
    lang_phrase = {
        "gu": "Gujarati",
        "hi": "Hindi",
        "bn": "Bengali",
        "en": "Indian English",
        "mr": "Marathi",
        "te": "Telugu",
        "kn": "Kannada",
    }.get(language, "an Indian language")

    # Decide gender: override > style hint > default female
    if gender_override in ("male", "female"):
        gender_phrase = gender_override
    else:
        gender_phrase = style.get("gender_hint", "female")

    # Soften pitch categories in wording to avoid muffled sound
    raw_pitch = style.get("pitch", "medium")
    if raw_pitch == "low":
        pitch_phrase = "a slightly lower, warm pitch"
    elif raw_pitch == "high":
        pitch_phrase = "a slightly higher, bright pitch"
    else:
        pitch_phrase = "a natural, medium pitch"

    # Clamp speed phrases a bit (fast → “medium-fast”)
    raw_speed = style.get("speed", "medium")
    if raw_speed == "slow":
        speed_phrase = "a slow, unhurried speaking pace"
    elif raw_speed == "fast":
        speed_phrase = "a medium-fast, energetic pace"
    else:
        speed_phrase = "a natural, medium speaking pace"

    energy = style.get("energy", "calm")
    noisiness = style.get("noisiness", "with almost no background noise")

    return (
        f"A {lang_phrase} {gender_phrase} speaker with {pitch_phrase} and {speed_phrase}, "
        f"sounding {energy} but still clear and controlled. The tone is warm and reassuring, "
        f"like a health worker calmly guiding a pregnant woman in a low-income community. "
        f"The voice is easy to understand, and the recording is clear and close-mic, {noisiness}."
    )
