# audio_style_extractor.py

import numpy as np
import librosa

def analyze_ref_audio(audio_path: str) -> dict:
    """
    Analyzes reference audio to extract style and gender.
    Uses a Voting System (Pitch + Timbre) to fix gender misclassification.
    """
    # Default fallback style
    style = {
        "pitch": "medium",
        "speed": "medium",
        "energy": "neutral",
        "gender_hint": "female", # Safe default for maternal context
        "noisiness": "with almost no background noise"
    }

    try:
        # Load audio (mono)
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        if len(y) == 0: return style

        # --- FEATURE 1: PITCH (F0) ---
        # Yin is robust for fundamental frequency
        f0 = librosa.yin(y, fmin=60, fmax=300)
        f0_valid = f0[f0 > 0]
        
        if len(f0_valid) > 0:
            median_f0 = float(np.median(f0_valid))
        else:
            median_f0 = 180.0 # Fallback

        # --- FEATURE 2: TIMBRE (Spectral Centroid) ---
        # This is the "Brightness" of the voice. 
        # Deep female voices often have higher centroids (>1700Hz) than deep male voices (<1500Hz).
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        avg_centroid = float(np.mean(cent))

        # --- ROBUST GENDER CLASSIFICATION LOGIC ---
        # Rule 1: Clear Pitch Boundaries
        if median_f0 < 110:
            gender_decision = "male"       # Very deep
        elif median_f0 > 175:
            gender_decision = "female"     # Clearly high
        else:
            # Rule 2: The "Ambiguous Zone" (110Hz - 175Hz)
            # This is where we use Timbre (Centroid) as the tie-breaker.
            if avg_centroid > 1800:
                gender_decision = "female" # Deep but bright (Female)
            else:
                gender_decision = "male"   # Deep and dark (Male)

        style["gender_hint"] = gender_decision
        
        # --- Pitch Description (Relative to detected gender) ---
        # A 160Hz Female is "Low Pitch". A 160Hz Male is "High Pitch".
        if gender_decision == "female":
            if median_f0 < 180: style["pitch"] = "low"
            elif median_f0 > 240: style["pitch"] = "high"
            else: style["pitch"] = "medium"
        else: # Male
            if median_f0 < 100: style["pitch"] = "low"
            elif median_f0 > 140: style["pitch"] = "high"
            else: style["pitch"] = "medium"

        # --- FEATURE 3: SPEED (Onset Density) ---
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        avg_tempo = tempo[0] if isinstance(tempo, np.ndarray) else tempo

        if avg_tempo < 95: style["speed"] = "slow"
        elif avg_tempo > 135: style["speed"] = "fast"
        else: style["speed"] = "medium"

        # --- FEATURE 4: ENERGY ---
        rms = librosa.feature.rms(y=y)[0]
        if np.std(rms) > 0.03: style["energy"] = "expressive"
        elif np.mean(rms) < 0.02: style["energy"] = "calm"
        else: style["energy"] = "neutral"

        # --- FEATURE 5: NOISE ---
        S = np.abs(librosa.stft(y))
        flatness = np.mean(librosa.feature.spectral_flatness(S=S))
        if flatness < 0.05: style["noisiness"] = "with almost no background noise"
        elif flatness < 0.2: style["noisiness"] = "with a bit of background noise"
        else: style["noisiness"] = "with noticeable background noise"

        print(f"[Extractor] F0: {median_f0:.1f}Hz | Centroid: {avg_centroid:.0f}Hz | Decision: {gender_decision}")

    except Exception as e:
        print(f"[Extractor] Analysis Error: {e}")
        return style

    return style


def build_caption(style: dict, language: str, speaker_name: str = None) -> str:
    """
    Constructs the prompt.
    """
    lang_map = {
        "gu": "Gujarati", "hi": "Hindi", "bn": "Bengali", "en": "Indian English",
        "mr": "Marathi", "te": "Telugu", "kn": "Kannada", "bho": "Hindi",
        "mag": "Hindi", "hne": "Hindi", "mai": "Hindi"
    }
    
    lang_phrase = lang_map.get(language, "Indian language")
    
    # 1. Subject
    if speaker_name:
        intro = f"{speaker_name} speaks"
    else:
        gender = style.get("gender_hint", "female")
        intro = f"A {lang_phrase} {gender} speaker speaks"

    # 2. Style Mapping
    p_val = style.get("pitch", "medium")
    if p_val == "low": pitch_phrase = "with a slightly deep, warm pitch"
    elif p_val == "high": pitch_phrase = "with a slightly high, clear pitch"
    else: pitch_phrase = "with a natural, balanced pitch"

    s_val = style.get("speed", "medium")
    if s_val == "slow": speed_phrase = "at a slow, unhurried pace"
    elif s_val == "fast": speed_phrase = "at a slightly fast, energetic pace"
    else: speed_phrase = "at a moderate, natural pace"

    e_val = style.get("energy", "neutral")
    if e_val == "calm": tone_phrase = "sounding calm and soothing"
    elif e_val == "expressive": tone_phrase = "sounding animated and expressive"
    else: tone_phrase = "sounding clear and neutral"

    noise_phrase = style.get("noisiness", "with almost no background noise")

    # 3. Assemble
    caption = (
        f"{intro} {pitch_phrase} and {speed_phrase}, {tone_phrase}. "
        f"The recording is of very high quality, very clear audio, close up, {noise_phrase}."
    )

    return caption