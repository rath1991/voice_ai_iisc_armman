# styles.py

from config_loader import CONFIG

# Language codes are validated using this
SUPPORTED_LANGS = CONFIG["supported_languages"]

# Dialect codes from your API → base language for style config
DIALECT_TO_BASE_LANG = {
    "bho": "hi",   # Bhojpuri → Hindi base
    "mag": "hi",   # Magadhi → Hindi base
    "hne": "hi",   # Chhattisgarhi → Hindi base (hne is your code)
    "mai": "hi",   # Maithili → Hindi base for now (text is still Maithili)
}

# Available speakers per language (from Indic Parler-TTS documentation)
LANG_SPEAKERS = {
    "hi": {"female": ["Divya", "Rani"], "male": ["Rohit", "Aman"]},
    "bn": {"female": ["Aditi", "Rashmi", "Riya"], "male": ["Arjun", "Arnav", "Tapan"]},
    "mr": {"female": ["Sunita", "Radha", "Isha"], "male": ["Sanjay", "Nikhil", "Varun"]},
    "te": {"female": ["Lalitha"], "male": ["Prakash", "Kiran"]},
    "kn": {"female": ["Anu", "Vidya"], "male": ["Suresh", "Chetan"]},
    "gu": {"female": ["Neha"], "male": ["Yash"]},
    "en": {"female": ["Mary", "Swapna", "Meera", "Sneha", "Tisha", "Priya", "Gauri", "Nisha", "Kavya", "Riya"], 
           "male": ["Thoma", "Dinesh", "Jatin", "Aakash", "Kabir", "Chingkhei", "Thoiba", "Tarun", "Raghav", "Ravi", "Vikas"]},
}

# Per-language, per-gender style configs using REAL Indic Parler speakers
# Enhanced with Indic Parler-TTS control parameters: background noise, reverberation, 
# expressivity, pitch, speaking rate, and voice quality
LANG_SPEAKER_STYLES = {
    # Hindi
    "hi": {
        "female": {
            "default_speaker": "Divya",
            "styles": {
                "empathetic_motherly": (
                    "Divya speaks with a warm, caring tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a slightly high pitch with gentle expressiveness and emotional depth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Divya speaks at a moderate pace with a neutral tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for medical advice and health information."
                ),
                "urgent_alert": (
                    "Divya speaks with a serious, firm tone at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear emphasis and expressiveness on warning phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and no background noise."
                ),
                "friend_casual": (
                    "Divya speaks in a friendly, conversational tone at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive and animated delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Rohit",
            "styles": {
                "empathetic_motherly": (
                    "Rohit speaks with a gentle, reassuring tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with soft expressiveness and emotional warmth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Rohit speaks at a moderate pace with a neutral, clear tone in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for health information."
                ),
                "urgent_alert": (
                    "Rohit speaks with a firm, serious tone at a slightly fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with clear emphasis and expressiveness on urgent parts, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Rohit speaks in a relaxed, conversational tone at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },

    # Bengali
    "bn": {
        "female": {
            "default_speaker": "Aditi",
            "styles": {
                "empathetic_motherly": (
                    "Aditi speaks with a warm, caring Bengali tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a slightly high pitch with gentle expressiveness and emotional depth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Aditi speaks at a moderate pace with a neutral Bengali tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for medical guidance."
                ),
                "urgent_alert": (
                    "Aditi speaks with a serious Bengali tone at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear emphasis and expressiveness on warning phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and no background noise."
                ),
                "friend_casual": (
                    "Aditi speaks in a friendly, conversational Bengali tone at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive and animated delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Arjun",
            "styles": {
                "empathetic_motherly": (
                    "Arjun speaks with a gentle, soft Bengali tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Arjun speaks at a moderate pace with a neutral Bengali tone in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "urgent_alert": (
                    "Arjun speaks with a serious Bengali tone at a slightly fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with clear emphasis and expressiveness on important warnings, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Arjun speaks in a relaxed, conversational Bengali tone at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },

    # Marathi
    "mr": {
        "female": {
            "default_speaker": "Sunita",
            "styles": {
                "empathetic_motherly": (
                    "Sunita speaks with a warm, caring Marathi tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a slightly high pitch with expressive delivery and emotional warmth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Sunita speaks at a moderate pace with a neutral Marathi tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for medical instructions."
                ),
                "urgent_alert": (
                    "Sunita speaks with a serious, firm Marathi tone at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear stress and expressiveness on warning phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and no background noise."
                ),
                "friend_casual": (
                    "Sunita speaks in a friendly, conversational Marathi tone at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Sanjay",
            "styles": {
                "empathetic_motherly": (
                    "Sanjay speaks with a gentle Marathi tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Sanjay speaks at a moderate pace with a neutral Marathi tone in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "urgent_alert": (
                    "Sanjay speaks with a serious Marathi tone at a fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with clear emphasis and expressiveness on urgent content, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Sanjay speaks in a relaxed, conversational Marathi tone at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },

    # Telugu
    "te": {
        "female": {
            "default_speaker": "Lalitha",
            "styles": {
                "empathetic_motherly": (
                    "Lalitha speaks with a warm, caring Telugu tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with gentle expressiveness and emotional depth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Lalitha speaks at a moderate pace with a neutral Telugu tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for instructions."
                ),
                "urgent_alert": (
                    "Lalitha speaks with a serious Telugu tone at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear stress and expressiveness on warning phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and no background noise."
                ),
                "friend_casual": (
                    "Lalitha speaks in a friendly, conversational Telugu tone at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive and animated delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Prakash",
            "styles": {
                "empathetic_motherly": (
                    "Prakash speaks with a gentle Telugu tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Prakash speaks at a moderate pace with a neutral Telugu tone in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "urgent_alert": (
                    "Prakash speaks with a serious Telugu tone at a fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with sharp emphasis and expressiveness on urgent parts, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Prakash speaks in a relaxed, conversational Telugu tone at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },

    # Kannada
    "kn": {
        "female": {
            "default_speaker": "Anu",
            "styles": {
                "empathetic_motherly": (
                    "Anu speaks with a warm, caring Kannada tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with gentle expressiveness and emotional depth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Anu speaks at a moderate pace with a neutral Kannada tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for health counselling."
                ),
                "urgent_alert": (
                    "Anu speaks with a serious Kannada tone at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear emphasis and expressiveness on warnings, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Anu speaks in a friendly, conversational Kannada tone at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive and animated delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Suresh",
            "styles": {
                "empathetic_motherly": (
                    "Suresh speaks with a gentle Kannada tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Suresh speaks at a moderate pace with a neutral Kannada tone in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "urgent_alert": (
                    "Suresh speaks with a firm Kannada tone at a slightly fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with clear emphasis and expressiveness on urgent content, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Suresh speaks in a relaxed, conversational Kannada tone at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },

    # Gujarati
    "gu": {
        "female": {
            "default_speaker": "Neha",
            "styles": {
                "empathetic_motherly": (
                    "Neha speaks with a warm, caring Gujarati tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Neha speaks at a moderate pace with a neutral Gujarati tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "urgent_alert": (
                    "Neha speaks with a serious Gujarati tone at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear emphasis and expressiveness on warnings, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Neha speaks in a friendly, conversational Gujarati tone at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Yash",
            "styles": {
                "empathetic_motherly": (
                    "Yash speaks with a gentle Gujarati tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "Yash speaks at a moderate pace with a neutral Gujarati tone in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "urgent_alert": (
                    "Yash speaks with a firm Gujarati tone at a slightly fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with clear stress and expressiveness on urgent phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "Yash speaks in a relaxed, conversational Gujarati tone at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },

    # English (Indian English accent)
    "en": {
        "female": {
            "default_speaker": "Mary",
            "styles": {
                "empathetic_motherly": (
                    "A female speaker with an Indian English accent delivers warm, caring speech with a slightly slow pace in a close-sounding environment. "
                    "Her voice has a slightly high pitch with gentle expressiveness and emotional depth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "A female speaker with an Indian English accent delivers neutral speech at a moderate pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for medical instructions."
                ),
                "urgent_alert": (
                    "A female speaker with an Indian English accent delivers serious, firm speech at a slightly fast pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with clear emphasis and expressiveness on warning phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and no background noise."
                ),
                "friend_casual": (
                    "A female speaker with an Indian English accent delivers friendly, conversational speech at a normal pace in a close-sounding environment. "
                    "Her voice has a balanced pitch with slightly expressive and animated delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
        "male": {
            "default_speaker": "Thoma",
            "styles": {
                "empathetic_motherly": (
                    "A male speaker with an Indian English accent delivers gentle, reassuring speech with a slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with soft expressiveness and emotional warmth, "
                    "delivered with moderate speed. The recording is of very high quality, very clear, "
                    "with the speaker's voice sounding close up and almost no background noise."
                ),
                "neutral_nurse": (
                    "A male speaker with an Indian English accent delivers neutral, clear speech at a moderate pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise, "
                    "suitable for health information."
                ),
                "urgent_alert": (
                    "A male speaker with an Indian English accent delivers firm, serious speech at a slightly fast pace in a close-sounding environment. "
                    "His voice has a moderate pitch with clear stress and expressiveness on urgent phrases, "
                    "delivered with faster than normal speed. The recording is of very high quality, very clear audio, "
                    "with the speaker's voice sounding close up and minimal background noise."
                ),
                "friend_casual": (
                    "A male speaker with an Indian English accent delivers relaxed, conversational speech at a normal pace in a close-sounding environment. "
                    "His voice has a balanced pitch with slightly expressive delivery, "
                    "moderate speed. The recording is of high quality, clear audio, "
                    "with the speaker's voice sounding close up and only minimal background noise."
                ),
            },
        },
    },
}


def resolve_effective_lang(lang_code: str) -> str:
    """
    Map dialect codes like 'bho', 'mag', 'hne', 'mai' to a base language for style selection.
    """
    return DIALECT_TO_BASE_LANG.get(lang_code, lang_code)


def build_caption(lang_code: str, style: str, speaker_gender: str = "female") -> str:
    """
    Build a Parler-style description caption using:
      - A real Indic speaker name (Divya, Rohit, Aditi, etc.) where applicable
      - Per-language, per-style descriptions with Indic Parler-TTS control parameters
      - Optional dialect note for Bhojpuri / Magadhi / Chhattisgarhi / Maithili
    
    Control parameters used:
    - Background Noise: clear, minimal, almost no background noise
    - Reverberation: close-sounding environment
    - Expressivity: gentle, slight, expressive, animated
    - Pitch: slightly high, moderate, balanced
    - Speaking Rate: slightly slow, moderate, normal, slightly fast, faster
    - Voice Quality: very high quality, very clear audio, clear audio
    """
    base_lang = resolve_effective_lang(lang_code)

    # Fallback to Hindi config if we don't have a dedicated style config
    lang_cfg = LANG_SPEAKER_STYLES.get(base_lang) or LANG_SPEAKER_STYLES["hi"]

    gender_key = "male" if speaker_gender and speaker_gender.lower() == "male" else "female"
    if gender_key not in lang_cfg:
        gender_key = "female"

    gender_cfg = lang_cfg[gender_key]
    styles = gender_cfg["styles"]

    # Fallback to a neutral style if the requested one is missing
    if style not in styles:
        # Try "neutral_nurse" first, else pick any
        style_desc = styles.get("neutral_nurse") or next(iter(styles.values()))
    else:
        style_desc = styles[style]

    caption = style_desc

    # Dialect note for Bhojpuri / Magadhi / Chhattisgarhi / Maithili
    if lang_code == "bho":
        caption += " The speech has a natural Bhojpuri-influenced Hindi regional accent, suitable for rural North India."
    elif lang_code == "mag":
        caption += " The speech has a natural Magadhi-flavoured Hindi accent, reflecting the Magadh region."
    elif lang_code == "hne":
        caption += " The speech has a natural Chhattisgarhi-flavoured Hindi accent, as spoken in central India."
    elif lang_code == "mai":
        caption += " The speech is delivered in a Maithili-influenced Hindi accent, reflecting the Mithila region."

    return caption


def get_speaker_name(lang_code: str, speaker_gender: str = "female") -> str:
    """
    Get the default speaker name for a given language and gender.
    Returns the speaker name if available, otherwise returns None.
    """
    base_lang = resolve_effective_lang(lang_code)
    lang_cfg = LANG_SPEAKER_STYLES.get(base_lang) or LANG_SPEAKER_STYLES["hi"]
    
    gender_key = "male" if speaker_gender and speaker_gender.lower() == "male" else "female"
    if gender_key not in lang_cfg:
        gender_key = "female"
    
    return lang_cfg[gender_key].get("default_speaker", None)


def get_available_speakers(lang_code: str, speaker_gender: str = "female") -> list:
    """
    Get list of available speakers for a given language and gender.
    Returns empty list if not available.
    """
    base_lang = resolve_effective_lang(lang_code)
    speakers = LANG_SPEAKERS.get(base_lang, {})
    return speakers.get(speaker_gender.lower(), [])
