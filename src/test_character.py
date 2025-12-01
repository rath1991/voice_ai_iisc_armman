# simple_character_test.py

import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import os

def main():
    print("Initializing Model directly...")
    
    # 1. Setup Device
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 2. Load Model and Tokenizers
    print("Loading model from ai4bharat/indic-parler-tts...")
    model = ParlerTTSForConditionalGeneration.from_pretrained("ai4bharat/indic-parler-tts").to(device)
    tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indic-parler-tts")
    description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
    
    # 3. Define Input
    # Gujarati text
    prompt = "નમસ્તે. મારું નામ નેહા છે અને હું તમારી મદદ કરવા માટે અહીં છું."
    
    # Explicit description with Language and Name
    description = "Neha speaks Gujarati with a natural, clear voice. The recording is of very high quality, very clear audio, close up."
    
    print(f"Prompt: {prompt}")
    print(f"Description: {description}")

    # 4. Tokenize
    description_input_ids = description_tokenizer(description, return_tensors="pt").to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").to(device)

    # 5. Generate
    print("Generating audio...")
    generation = model.generate(
        input_ids=description_input_ids.input_ids, 
        attention_mask=description_input_ids.attention_mask, 
        prompt_input_ids=prompt_input_ids.input_ids, 
        prompt_attention_mask=prompt_input_ids.attention_mask
    )
    
    # 6. Save
    audio_arr = generation.cpu().numpy().squeeze()
    output_filename = "indic_tts_out.wav"
    sf.write(output_filename, audio_arr, model.config.sampling_rate)
    
    print(f"✓ Success! Saved audio to: {output_filename}")

if __name__ == "__main__":
    main()