#!/usr/bin/env python3
"""
API Testing Script for TTS Synthesis API
Tests the API endpoints with various languages and styles.
All generated audio files are saved into the 'test_outputs' subdirectory.
"""

import requests
import json
from pathlib import Path
import click

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
        print(f"  Description: {description}")
        print(f"  Description Length: {len(description)} chars")
    
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
    language="bn",
    style="Bengali - Alternative Male Speaker Showcase (Arjun - Soft Caring)",
    speaker_gender="male",
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
        print(f"  Description: {description}")
        print(f"  Description Length: {len(description)} chars")
    
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


@click.group(invoke_without_command=True)
@click.option('--base-url', default="http://localhost:8000", help='Base URL of the API server')
@click.pass_context
def cli(ctx, base_url):
    """API Testing Script for TTS Synthesis API"""
    global BASE_URL
    BASE_URL = base_url
    
    # If no subcommand is provided, run round1 by default for Round 1 focus
    if ctx.invoked_subcommand is None:
        ctx.invoke(round1)


@cli.command()
@click.argument('text')
@click.option('--language', '-l', default='hi', help='Language code (default: hi)')
@click.option('--style', '-s', default='empathetic_motherly', 
              help='Style (default: empathetic_motherly)')
@click.option('--speaker-gender', '-g', default='female', 
              type=click.Choice(['male', 'female'], case_sensitive=False),
              help='Speaker gender (default: female)')
@click.option('--output', '-o', default='custom_test_output_post.wav',
              help='Output filename (default: custom_test_output_post.wav)')
def custom(text, language, style, speaker_gender, output):
    """Test API with custom parameters"""
    print("Testing with custom parameters...")
    print(f"Output WAV files will be stored in: {OUTPUT_DIR}")
    test_health()
    test_post_synthesize(text, language, style, speaker_gender)
    test_post_synthesize_wav(
        text,
        language,
        style,
        speaker_gender,
        output
    )


@cli.command()
@click.option('--json-file', '-j', default='api_test_texts.json',
              help='JSON test file path (default: api_test_texts.json)')
@click.option('--limit', '-n', type=int, default=5,
              help='Number of test cases to run (default: 5)')
@click.option('--languages', '-lang', multiple=True,
              help='Filter by language codes (can be used multiple times, e.g., -lang gu -lang en)')
def json_tests(json_file, limit, languages):
    """Run tests from JSON test file"""
    json_path = Path(__file__).parent / json_file
    
    if not json_path.exists():
        click.echo(f"Error: {json_file} not found at {json_path}", err=True)
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Filter by languages if specified
    all_test_cases = test_data["test_cases"]
    if languages:
        languages = [lang.lower() for lang in languages]
        filtered_cases = [tc for tc in all_test_cases if tc.get("language", "").lower() in languages]
        click.echo(f"Filtered to {len(filtered_cases)} test case(s) for languages: {', '.join(languages)}")
        test_cases = filtered_cases[:limit]
    else:
        test_cases = all_test_cases[:limit]
    
    if not test_cases:
        click.echo("No test cases found matching the criteria.", err=True)
        return
    
    print("=" * 60)
    print("Running API Tests")
    print("=" * 60)
    print(f"Output WAV files will be stored in: {OUTPUT_DIR}")
    
    # Test health endpoint
    if not test_health():
        print("\nHealth check failed. Is the server running?")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Running {len(test_cases)} Test Case(s)")
    print(f"{'=' * 60}")
    
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


@cli.command()
@click.option('--json-file', '-j', default='api_test_texts.json',
              help='JSON test file path (default: api_test_texts.json)')
@click.option('--limit', '-n', type=int, default=None,
              help='Number of test cases to run (default: all Gujarati and English cases)')
def round1(json_file, limit):
    """
    Run Round 1 tests focusing on Gujarati and English (Indian) TTS.
    Tests accent and style transfer capabilities for Round 1 submission.
    """
    json_path = Path(__file__).parent / json_file
    
    if not json_path.exists():
        click.echo(f"Error: {json_file} not found at {json_path}", err=True)
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Filter to only Gujarati (gu) and English (en) test cases
    round1_languages = ['gu', 'en']
    filtered_cases = [
        tc for tc in test_data["test_cases"] 
        if tc.get("language", "").lower() in round1_languages
    ]
    
    if not filtered_cases:
        click.echo("No Gujarati or English test cases found in the JSON file.", err=True)
        return
    
    # Apply limit if specified
    if limit:
        filtered_cases = filtered_cases[:limit]
    
    click.echo("=" * 70)
    click.echo("ROUND 1: Gujarati & English (Indian) TTS Testing")
    click.echo("Focus: Accent and Style Transfer")
    click.echo("=" * 70)
    click.echo(f"Found {len(filtered_cases)} test case(s) for Gujarati and English")
    click.echo(f"Output WAV files will be stored in: {OUTPUT_DIR}")
    
    # Test health endpoint
    if not test_health():
        click.echo("\nHealth check failed. Is the server running?", err=True)
        return
    
    click.echo(f"\n{'=' * 70}")
    click.echo(f"Running {len(filtered_cases)} Round 1 Test Case(s)")
    click.echo(f"{'=' * 70}")
    
    for i, test_case in enumerate(filtered_cases, 1):
        click.echo(f"\n{'='*70}")
        click.echo(f"Test Case {i}/{len(filtered_cases)}: {test_case['description']}")
        click.echo(f"Language: {test_case['language'].upper()} | Style: {test_case['style']} | Gender: {test_case['speaker_gender']}")
        click.echo(f"{'='*70}")
        
        text = test_case["text"]
        language = test_case["language"]
        style = test_case["style"]
        speaker_gender = test_case["speaker_gender"]
        
        # Show full description before testing
        if build_caption:
            description = build_caption(language, style, speaker_gender)
            click.echo(f"\n📝 Full Description Parameter:")
            click.echo(f"   {description}")
            click.echo(f"   Length: {len(description)} characters")
        
        if get_speaker_name:
            speaker = get_speaker_name(language, speaker_gender)
            if speaker:
                click.echo(f"   Speaker: {speaker}")
        
        # Test POST /synthesize (JSON + base64)
        test_post_synthesize(
            text,
            language,
            style,
            speaker_gender
        )
        
        # Test POST /synthesize_wav (binary WAV)
        wav_filename = f"round1_{i}_{language}_{style}_{speaker_gender}_post.wav"
        # Clean filename a bit (no spaces)
        wav_filename = wav_filename.replace(" ", "_").replace("/", "_")
        
        test_post_synthesize_wav(
            text,
            language,
            style,
            speaker_gender,
            wav_filename
        )
    
    click.echo("\n" + "=" * 70)
    click.echo("Round 1 Tests completed!")
    click.echo(f"Generated {len(filtered_cases)} audio files in: {OUTPUT_DIR}")
    click.echo("=" * 70)


if __name__ == "__main__":
    cli()
