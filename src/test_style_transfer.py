# test_style_transfer.py

from tts_engine import TTSEngine
from audio_style_extractor import analyze_ref_audio
from styles import resolve_effective_lang, get_speaker_name, SUPPORTED_LANGS
import os
import random

# Global list of test scenarios for easy switching
TEST_SCENARIOS = {
    "GUJ_FEMALE_STYLE": {
        "text": "કૃપયા તમારો આયર્નનો ગોળી ભોજન પછી રોજ લો.",
        "language_code": "gu",
        "speaker_accent_code": "gu", # Force speaker anchor to Gujarati (Neha)
        "ref_audio_path": "assets/assets_female_gujrati/IISc_SPICORProject_GUJ_F_ENTE_1604.wav",
        "description": "Base Gujarati Female Style Transfer (Neha). Expected: Female voice, speaking Gujarati."
    },
    "EN_ACCENT_TRANSFER": {
        "text": "Hello, doctor has advised you to take the iron tablets exactly one time per day, after breakfast.",
        "language_code": "gu", 
        "speaker_accent_code": "gu", # Force speaker anchor to Gujarati (Neha) for accent.
        "ref_audio_path": "assets/assets_female_gujrati/IISc_SPICORProject_GUJ_F_ENTE_1604.wav",
        "description": "Accent Transfer Test. We use English text but force the Gujarati speaker's accent. Expected: Female voice, Gujarati-accented English."
    },
    "GUJ_MALE_STYLE": {
        "text": "તમારું આરોગ્ય ખૂબ જ મહત્વપૂર્ણ છે, તેથી પૂરતો આરામ લો.",
        "language_code": "gu",
        "speaker_accent_code": "gu", # Force speaker anchor to Gujarati (Yash)
        "ref_audio_path": "assets/assets_male_gujrati/IISc_SPICORProject_EN_M_ENTE_1609.wav", 
        "description": "Male Style Transfer Test. Expected: Male voice (Yash), speaking Gujarati."
    }
}


def run_test_case(tts: TTSEngine, scenario_key: str):
    """Executes a single test scenario."""
    scenario = TEST_SCENARIOS[scenario_key]
    
    text = scenario["text"]
    language_code = scenario["language_code"] # Language for text normalization
    speaker_accent_code = scenario["speaker_accent_code"] # Language for speaker/accent selection
    ref_audio_path = scenario["ref_audio_path"]
    
    print(f"\n=======================================================")
    print(f"TEST CASE: {scenario_key} - {scenario['description']}")
    print(f"Text: '{text}'")
    print(f"Ref Audio: {ref_audio_path}")
    print(f"=======================================================")

    if not os.path.exists(ref_audio_path):
        print(f"Error: Reference audio file NOT FOUND at {ref_audio_path}. Skipping.")
        return

    # --- STEP 1: Analyze Audio (Pitch + Timbre) ---
    print(f"\n1. Analyzing Reference Audio...")
    style = analyze_ref_audio(ref_audio_path)
    print(f"   Extracted Style: {style}")

    # --- STEP 2: Dynamic Speaker Selection ---
    detected_gender = style.get("gender_hint", "female")
    
    # We use the speaker_accent_code (e.g., 'gu') to select the speaker (Neha).
    base_accent_lang = resolve_effective_lang(speaker_accent_code) 
    best_speaker = get_speaker_name(base_accent_lang, detected_gender)
    
    # We use the speaker_accent_code to get the full language name for the prompt.
    language_full_name = SUPPORTED_LANGS.get(speaker_accent_code, "Indian language")

    print(f"\n2. Dynamic Speaker Selection:")
    print(f"   Detected Gender: {detected_gender}")
    print(f"   Selected Speaker (Voice Anchor): {best_speaker}")
    print(f"   Language Name for Prompt (Accent): {language_full_name}")

    # --- STEP 3: Construct Caption Manually ---
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
    
    # Assemble the final prompt
    # The language name here determines the accent/pronunciation library used by Parler-TTS.
    caption = (
        f"{best_speaker} speaks {language_full_name} {pitch_desc} and {speed_desc}. "
        f"The recording is of very high quality, very clear audio, close up, with almost no background noise."
    )
    
    print(f"\n3. Final Generated Caption:\n   '{caption}'")

    # --- STEP 4: Generate Audio ---
    output_filename = f"test_{scenario_key.lower()}.wav"
    print(f"\n4. Synthesizing Audio to {output_filename}...")
    
    # CRITICAL: We pass the language_code ('en') for text normalization,
    # but the ACCENT is forced by the 'caption' built with 'gu'.
    audio_bytes = tts.synthesize_with_description(
        text=text,
        language=language_code, 
        description=caption,
    )

    # --- STEP 5: Save ---
    with open(output_filename, "wb") as f:
        f.write(audio_bytes)

    print(f"\n✓ Success! Saved output to: {output_filename}")


def main():
    print("Initializing TTS Engine...")
    tts = TTSEngine()

    # =======================================================
    # !!! SELECT YOUR TEST CASE HERE !!!
    # =======================================================
    
    # Test 1: Standard Gujarati Style Transfer (Neha speaks Gujarati)
    run_test_case(tts, "GUJ_FEMALE_STYLE")
    
    # Test 2: Accent Transfer (Neha speaks English)
    run_test_case(tts, "EN_ACCENT_TRANSFER")
    
    # Optional: Run the male test (if you have a male audio file)
    # run_test_case(tts, "GUJ_MALE_STYLE") 


if __name__ == "__main__":
    main()