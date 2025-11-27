# tts_engine.py

import os
import torch
import numpy as np
import soundfile as sf
from typing import Tuple, Optional

from config_loader import CONFIG
from normalization import normalize_text
from styles import build_caption, resolve_effective_lang

from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
from huggingface_hub import login as hf_login


class TTSEngine:
    def __init__(self):
        self.model_id = CONFIG["model_id"]
        self.sample_rate = CONFIG["sample_rate"]

        device_name = CONFIG["device"]
        self.device = torch.device(device_name if torch.cuda.is_available() else "cpu")

        # Get Hugging Face token from environment variable or config
        self.hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or CONFIG.get("hf_token")

        print(f"[TTS] Loading {self.model_id} on {self.device}...")
        
        # Authenticate with Hugging Face if token is provided
        if self.hf_token:
            print("[TTS] Authenticating with Hugging Face token...")
            try:
                hf_login(token=self.hf_token, add_to_git_credential=False)
            except Exception as e:
                print(f"[TTS] Warning: Could not login with token: {e}")
        
        # Prepare kwargs for from_pretrained calls
        model_kwargs = {}
        if self.hf_token:
            model_kwargs["token"] = self.hf_token
        
        # Load model using ParlerTTSForConditionalGeneration
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
            self.model_id,
            **model_kwargs
        ).to(self.device)
        self.model.eval()
        
        # Load tokenizer for prompts
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            **model_kwargs
        )
        
        # Load description tokenizer (for captions)
        self.description_tokenizer = AutoTokenizer.from_pretrained(
            self.model.config.text_encoder._name_or_path,
            **model_kwargs
        )
        
        # Get actual sample rate from model config
        if hasattr(self.model.config, 'sampling_rate'):
            self.sample_rate = self.model.config.sampling_rate
        
        print("[TTS] Model loaded.")

    @torch.inference_mode()
    def synthesize(self, text: str, lang_code: str, style: str, speaker_gender: str):
        """
        Synthesize speech from text using the Indic Parler-TTS model.
        
        Args:
            text: Text to convert to speech
            lang_code: Language code (e.g., 'hi', 'en', 'bn')
            style: Style description (e.g., 'empathetic_motherly')
            speaker_gender: Speaker gender ('male' or 'female')
        
        Returns:
            Tuple of (audio_array, sample_rate)
        """
        # Normalize text
        norm_text = normalize_text(text, lang_code)
        
        # Build caption/description
        description = build_caption(lang_code, style, speaker_gender)
        
        # Tokenize description and prompt
        description_input_ids = self.description_tokenizer(
            description, 
            return_tensors="pt"
        ).to(self.device)
        
        prompt_input_ids = self.tokenizer(
            norm_text, 
            return_tensors="pt"
        ).to(self.device)
        
        # Generate audio
        generation = self.model.generate(
            input_ids=description_input_ids.input_ids,
            attention_mask=description_input_ids.attention_mask,
            prompt_input_ids=prompt_input_ids.input_ids,
            prompt_attention_mask=prompt_input_ids.attention_mask
        )
        
        # Extract audio array (generation output is already the audio)
        audio_arr = generation.cpu().numpy().squeeze()
        
        return audio_arr, self.sample_rate

    def save(self, wav, sr, path):
        sf.write(path, wav, sr)
