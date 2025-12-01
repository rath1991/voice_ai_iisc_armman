# tts_engine.py

import io
from typing import Optional

import numpy as np
import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

from config_loader import CONFIG
from normalization import normalize_text
from styles import build_caption, resolve_effective_lang


class TTSEngine:
    """
    Wrapper around Indic Parler-TTS.

    Responsibilities:
    - Load model + tokenizers once.
    - Provide:
        * synthesize_with_style(text, language, style, speaker_gender)
        * synthesize_with_description(text, language, description)
    - Return audio as WAV bytes.
    """

    def __init__(self) -> None:
        cfg = CONFIG

        self.model_id: str = cfg["model_id"]
        self.sample_rate: int = cfg.get("sample_rate", 24000)
        
        # Determine device: check CUDA availability even if config says "cuda"
        requested_device = cfg.get("device", "cuda" if torch.cuda.is_available() else "cpu")
        
        # Always verify CUDA is actually available before using it
        if requested_device.startswith("cuda"):
            if not torch.cuda.is_available():
                print(f"[TTSEngine] Warning: CUDA requested but not available. Falling back to CPU.")
                self.device_str = "cpu"
            else:
                self.device_str = requested_device
        else:
            self.device_str = requested_device
        
        # Convert to torch.device for proper handling
        self.device = torch.device(self.device_str)

        # Load model + tokenizers
        self._load_model_and_tokenizers()

    def _load_model_and_tokenizers(self) -> None:
        """Load Indic Parler-TTS and both tokenizers."""
        print(f"[TTSEngine] Loading model: {self.model_id} on {self.device}")

        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
            self.model_id
        )
        
        # Move model to device (will fallback to CPU if CUDA unavailable)
        try:
            self.model = self.model.to(self.device)
        except Exception as e:
            print(f"[TTSEngine] Warning: Could not move model to {self.device}: {e}")
            print(f"[TTSEngine] Falling back to CPU")
            self.device = torch.device("cpu")
            self.device_str = "cpu"
            self.model = self.model.to(self.device)
        
        self.model.eval()

        # Prompt / transcript tokenizer
        self.prompt_tokenizer = AutoTokenizer.from_pretrained(self.model_id)

        # Description / caption tokenizer
        self.description_tokenizer = AutoTokenizer.from_pretrained(
            self.model.config.text_encoder._name_or_path
        )

        print(f"[TTSEngine] Model and tokenizers loaded on {self.device}.")

    def _to_wav_bytes(self, audio_arr: np.ndarray) -> bytes:
        """
        Convert a float waveform to WAV bytes using the configured sample rate.
        """
        # Ensure 1D float32
        audio_arr = np.asarray(audio_arr, dtype=np.float32).squeeze()

        buf = io.BytesIO()
        sf.write(buf, audio_arr, self.sample_rate, format="WAV")
        buf.seek(0)
        return buf.read()

    def synthesize_with_description(
        self,
        text: str,
        language: str,
        description: str,
    ) -> bytes:
        """
        Core generation method:
         - Normalize text
         - Tokenize description + prompt
         - Call Indic Parler-TTS generate(...)
         - Return WAV bytes
        """
        # Use your minimal normalization
        lang_norm = resolve_effective_lang(language)
        normalized_text = normalize_text(text, lang_norm)

        # Tokenize caption/description
        desc_inputs = self.description_tokenizer(
            description,
            return_tensors="pt",
            truncation=True,
        ).to(self.device)

        # Tokenize prompt/text
        prompt_inputs = self.prompt_tokenizer(
            normalized_text,
            return_tensors="pt",
            truncation=True,
        ).to(self.device)

        with torch.no_grad():
            generation = self.model.generate(
                input_ids=desc_inputs.input_ids,
                attention_mask=desc_inputs.attention_mask,
                prompt_input_ids=prompt_inputs.input_ids,
                prompt_attention_mask=prompt_inputs.attention_mask,
            )

        audio_arr = generation.cpu().numpy().squeeze()
        return self._to_wav_bytes(audio_arr)

    def synthesize_with_style(
        self,
        text: str,
        language: str,
        style: str,
        speaker_gender: str = "female",
    ) -> bytes:
        """
        High-level interface: language + style + gender → caption → TTS.
        Uses styles.build_caption() to get Parler description.
        """
        lang_norm = resolve_effective_lang(language)
        caption = build_caption(lang_norm, style, speaker_gender)
        return self.synthesize_with_description(text, lang_norm, caption)
