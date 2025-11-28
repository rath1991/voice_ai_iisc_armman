#!/usr/bin/env python3
"""
API Testing Script for TTS Synthesis API
Tests the API endpoints with various languages and styles.
All generated audio files are saved into the 'test_outputs' subdirectory.
"""

import requests
import json
import sys
from pathlib import Path

# Import styles module to show speaker and description info
try:
    from styles import build_caption, get_speaker_name, get_available_speakers
except ImportError:
    build_caption = None
    get_speaker_name = None
    get_available_speakers = None

BASE_URL = "http://localhost:8000"

# Directory to store generated WAV files
OUTPUT_DIR = Path(__file__).parent / "test_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def test_health():
    """Test the /health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Error: {e}")
        return False


def test_post_synthesize(text, language="hi", style="empathetic_motherly", speaker_gender="female"):
    """Test POST /synthesize endpoint (JSON + base64 audio)"""
    print(f"\nTesting POST /synthesize...")
    print(f"  Text: {text[:50]}...")
    print(f"  Language: {language}, Style: {style}, Gender: {speaker_gender}")
    
    # Show speaker and description info if available
    if get_speaker_name:
        speaker = get_speaker_name(language, speaker_gender)
        if speaker:
            print(f"  Speaker: {speaker}")
    
    if build_caption:
        description = build_caption(language, style, speaker_gender)
        print(f"  Description: {description[:100]}...")
    
    url = f"{BASE_URL}/synthesize"
    data = {
        "text": text,
        "language": language,
        "style": style,
        "speaker_gender": speaker_gender
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Sample Rate: {result['sample_rate']} Hz")
            print(f"  Duration: {result['duration_ms']:.2f} ms")
            print(f"  Audio Base64 Length: {len(result['audio_base64'])} chars")
            return True
        else:
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"  Error: {e}")
        return False


def test_post_synthesize_wav(
    text,
    language="hi",
    style="empathetic_motherly",
    speaker_gender="female",
    output_filename="test_output_post.wav",
):
    """
    Test POST /synthesize_wav endpoint.
    Saves the WAV file into the 'test_outputs' subdirectory.
    """
    print(f"\nTesting POST /synthesize_wav...")
    print(f"  Text: {text[:50]}...")
    print(f"  Language: {language}, Style: {style}, Gender: {speaker_gender}")
    
    # Show speaker and description info if available
    if get_speaker_name:
        speaker = get_speaker_name(language, speaker_gender)
        if speaker:
            print(f"  Speaker: {speaker}")
    
    if build_caption:
        description = build_caption(language, style, speaker_gender)
        print(f"  Description: {description[:100]}...")
    
    url = f"{BASE_URL}/synthesize_wav"
    data = {
        "text": text,
        "language": language,
        "style": style,
        "speaker_gender": speaker_gender
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            output_path = OUTPUT_DIR / output_filename
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"  Saved to: {output_path}")
            print(f"  File size: {len(response.content)} bytes")
            return True
        else:
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"  Error: {e}")
        return False


def run_tests_from_json(json_file="api_test_texts.json"):
    """Run tests from the JSON test file"""
    json_path = Path(__file__).parent / json_file
    
    if not json_path.exists():
        print(f"Error: {json_file} not found at {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    print("=" * 60)
    print("Running API Tests")
    print("=" * 60)
    print(f"Output WAV files will be stored in: {OUTPUT_DIR}")
    
    # Test health endpoint
    if not test_health():
        print("\nHealth check failed. Is the server running?")
        return
    
    # Run a few sample tests
    test_cases = test_data["test_cases"][:5]  # Test first 5 cases
    
    print("\n" + "=" * 60)
    print("Running Sample Test Cases")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: {test_case['description']}")
        print(f"{'='*60}")
        
        text = test_case["text"]
        language = test_case["language"]
        style = test_case["style"]
        speaker_gender = test_case["speaker_gender"]
        
        # Test POST /synthesize (JSON + base64)
        test_post_synthesize(
            text,
            language,
            style,
            speaker_gender
        )
        
        # Test POST /synthesize_wav (binary WAV)
        wav_filename = f"test_output_{i}_{language}_{style}_{speaker_gender}_post.wav"
        # Clean filename a bit (no spaces)
        wav_filename = wav_filename.replace(" ", "_")
        
        test_post_synthesize_wav(
            text,
            language,
            style,
            speaker_gender,
            wav_filename
        )
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Custom test from command line arguments
        text = sys.argv[1]
        language = sys.argv[2] if len(sys.argv) > 2 else "hi"
        style = sys.argv[3] if len(sys.argv) > 3 else "empathetic_motherly"
        speaker_gender = sys.argv[4] if len(sys.argv) > 4 else "female"
        
        print("Testing with custom parameters...")
        print(f"Output WAV files will be stored in: {OUTPUT_DIR}")
        test_health()
        test_post_synthesize(text, language, style, speaker_gender)
        test_post_synthesize_wav(
            text,
            language,
            style,
            speaker_gender,
            "custom_test_output_post.wav"
        )
    else:
        # Run tests from JSON file
        run_tests_from_json()
