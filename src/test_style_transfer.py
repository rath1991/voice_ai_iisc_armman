# test_style_transfer.py

from tts_engine import TTSEngine
from audio_style_extractor import analyze_ref_audio, build_caption
from styles import resolve_effective_lang

import soundfile as sf
import numpy as np

def main():
    tts = TTSEngine()

    text = "કૃપયા તમારો આયર્નનો ગોળી ભોજન પછી રોજ લો."
    language = "gu"
    ref_audio_path = "assets/assets_female_gujrati/IISc_SPICORProject_GUJ_F_ENTE_1604.wav"

    # 1. Analyze style from reference audio
    style = analyze_ref_audio(ref_audio_path)
    print("Extracted style:", style)

    # 2. Build a Parler caption
    lang_norm = resolve_effective_lang(language)
    caption = build_caption(style, lang_norm)
    print("Generated caption:", caption)

    # 3. Generate audio
    audio_bytes = tts.synthesize_with_description(
        text=text,
        language=lang_norm,
        description=caption,
    )

    # 4. Save to file
    with open("test_guj_from_ref.wav", "wb") as f:
        f.write(audio_bytes)

    print("Saved: test_guj_from_ref.wav")

if __name__ == "__main__":
    main()
