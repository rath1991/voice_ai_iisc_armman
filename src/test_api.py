# test_style_transfer.py

from tts_engine import TTSEngine
from audio_style_extractor import analyze_ref_audio
from styles import resolve_effective_lang, get_speaker_name

import soundfile as sf
import numpy as np
import os

def main():
    tts = TTSEngine()

    text = "કૃપયા તમારો આયર્નનો ગોળી ભોજન પછી રોજ લો."
    language = "gu"
    # Ensure this path exists or update it to a valid file on your system
    ref_audio_path = "assets/assets_female_gujrati/IISc_SPICORProject_GUJ_F_ENTE_1604.wav"

    if not os.path.exists(ref_audio_path):
        print(f"Error: Reference audio not found at {ref_audio_path}")
        return

    # 1. Analyze style from reference audio
    print(f"Analyzing {ref_audio_path}...")
    style = analyze_ref_audio(ref_audio_path)
    print("Extracted style:", style)

    # 2. Resolve Speaker Identity
    lang_norm = resolve_effective_lang(language)
    
    # Get the detected gender from the analysis (e.g., 'female')
    detected_gender = style.get("gender_hint", "female")
    
    # Look up the high-quality speaker name (e.g., 'Neha' for Guj-Female)
    best_speaker = get_speaker_name(lang_norm, detected_gender)
    print(f"Selected Base Speaker: {best_speaker}")

    # 3. Build Caption (MANUAL FIX)
    # We construct the string here to ensure 'best_speaker' is used.
    # This prevents the "A Gujarati speaker..." fallback which causes low quality.
    
    pitch_val = style.get("pitch", "medium")
    if pitch_val == "low":
        pitch_desc = "with a slightly deep, warm pitch"
    elif pitch_val == "high":
        pitch_desc = "with a slightly high, clear pitch"
    else:
        pitch_desc = "with a natural, balanced pitch"

    speed_val = style.get("speed", "medium")
    if speed_val == "slow":
        speed_desc = "at a slow, unhurried pace"
    elif speed_val == "fast":
        speed_desc = "at a slightly fast, energetic pace"
    else:
        speed_desc = "at a moderate, natural pace"

    # The Magic Formula: "{Name} speaks..." is mandatory for quality
    caption = (
        f"{best_speaker} speaks {pitch_desc} and {speed_desc}. "
        f"The recording is of very high quality, very clear audio, close up, with almost no background noise."
    )
    
    print("Generated caption:", caption)

    # 4. Generate audio
    audio_bytes = tts.synthesize_with_description(
        text=text,
        language=lang_norm,
        description=caption,
    )

    # 5. Save to file
    output_filename = "test_guj_from_ref.wav"
    with open(output_filename, "wb") as f:
        f.write(audio_bytes)

    print(f"Saved: {output_filename}")

if __name__ == "__main__":
    main()