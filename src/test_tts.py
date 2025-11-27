"""
Test script for TTS Engine
Can be run in Jupyter Lab or as a standalone script
"""

import os
import sys
from dotenv import load_dotenv
import soundfile as sf
import numpy as np

# Load environment variables
load_dotenv()

# Import TTS engine
from tts_engine import TTSEngine
from config_loader import CONFIG

def test_tts_engine():
    """Test the TTS engine with sample text"""
    
    print("=" * 60)
    print("TTS Engine Test Script")
    print("=" * 60)
    
    # Check for authentication token
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        print("\n⚠️  WARNING: No HF_TOKEN found!")
        print("Please set HF_TOKEN environment variable or use .env file")
        print("You can also run: hf auth login")
        print("\nContinuing anyway...\n")
    else:
        print(f"✓ Found HF_TOKEN (length: {len(hf_token)})")
    
    # Initialize TTS engine
    print("\n[1/4] Initializing TTS Engine...")
    try:
        engine = TTSEngine()
        print("✓ TTS Engine initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize TTS Engine: {e}")
        return False
    
    # Test parameters
    test_cases = [
        {
            "text": "नमस्ते, यह एक परीक्षण है।",
            "language": "hi",
            "style": "empathetic_motherly",
            "speaker_gender": "female",
            "output_file": "test_output_hindi.wav"
        },
        {
            "text": "Hello, this is a test.",
            "language": "en",
            "style": "neutral_nurse",
            "speaker_gender": "female",
            "output_file": "test_output_english.wav"
        }
    ]
    
    print(f"\n[2/4] Running {len(test_cases)} test cases...")
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}/{len(test_cases)} ---")
        print(f"Text: {test_case['text']}")
        print(f"Language: {test_case['language']}")
        print(f"Style: {test_case['style']}")
        print(f"Gender: {test_case['speaker_gender']}")
        
        try:
            # Synthesize audio
            print(f"[3/4] Synthesizing audio...")
            audio, sample_rate = engine.synthesize(
                text=test_case["text"],
                lang_code=test_case["language"],
                style=test_case["style"],
                speaker_gender=test_case["speaker_gender"]
            )
            
            print(f"✓ Audio generated successfully")
            print(f"  - Sample rate: {sample_rate} Hz")
            print(f"  - Audio length: {len(audio)} samples")
            print(f"  - Duration: {len(audio) / sample_rate:.2f} seconds")
            
            # Save audio file
            output_path = test_case["output_file"]
            print(f"[4/4] Saving audio to {output_path}...")
            sf.write(output_path, audio, sample_rate)
            print(f"✓ Audio saved to {output_path}")
            
            results.append({
                "test_case": i,
                "status": "success",
                "output_file": output_path,
                "duration": len(audio) / sample_rate
            })
            
        except Exception as e:
            print(f"✗ Error in test case {i}: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "test_case": i,
                "status": "failed",
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    successful = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - successful
    
    print(f"Total tests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print("\n✓ Generated audio files:")
        for r in results:
            if r["status"] == "success":
                print(f"  - {r['output_file']} ({r['duration']:.2f}s)")
    
    return successful == len(results)


if __name__ == "__main__":
    success = test_tts_engine()
    sys.exit(0 if success else 1)

