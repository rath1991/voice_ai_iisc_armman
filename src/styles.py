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


# Per-language, per-gender style configs using REAL Indic Parler speakers
# These are aligned with the documentation you pasted.
LANG_SPEAKER_STYLES = {
    # Hindi
    "hi": {
        "female": {
            "default_speaker": "Divya",
            "styles": {
                "empathetic_motherly": (
                    "Divya's voice is warm and caring, with a natural Hindi accent. "
                    "She speaks at a slightly slow pace with gentle expressiveness, "
                    "as if counselling someone, in a very clear, close-up recording with almost no background noise."
                ),
                "neutral_nurse": (
                    "Divya's voice is calm and neutral, with a clear Hindi accent, "
                    "moderate speaking speed, and a very clean, close recording suitable for medical advice."
                ),
                "urgent_alert": (
                    "Divya's voice is serious and firm, with a natural Hindi accent. "
                    "She speaks slightly faster than normal, clearly emphasizing warning phrases, "
                    "in a very clear, close-sounding recording with no background noise."
                ),
                "friend_casual": (
                    "Divya speaks in a friendly, conversational Hindi tone, at a normal pace, "
                    "slightly expressive and relaxed, with a clear, close-sounding recording."
                ),
            },
        },
        "male": {
            "default_speaker": "Rohit",
            "styles": {
                "empathetic_motherly": (
                    "Rohit's voice is gentle and reassuring, with a natural Hindi accent. "
                    "He speaks at a slightly slow pace with soft expressiveness, "
                    "in a very clear close-up recording with almost no background noise."
                ),
                "neutral_nurse": (
                    "Rohit's voice is neutral and clear, with a natural Hindi accent, "
                    "moderate speaking rate, and a clean, close recording suitable for health information."
                ),
                "urgent_alert": (
                    "Rohit's voice is firm and serious, with a natural Hindi accent. "
                    "He speaks at a slightly fast pace, clearly emphasizing urgent parts, "
                    "with a very clear, close recording and minimal background noise."
                ),
                "friend_casual": (
                    "Rohit speaks in a relaxed, conversational Hindi tone, with a natural accent, "
                    "normal speed, slightly expressive delivery, and a clear close-sounding recording."
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
                    "Aditi speaks with a warm, caring Bengali tone and natural Kolkata accent. "
                    "Her voice has a slightly high pitch, slow pace, and gentle expressiveness, "
                    "captured in a very clear, close recording with almost no background noise."
                ),
                "neutral_nurse": (
                    "Aditi speaks with a neutral Bengali accent, normal pace, "
                    "clear articulation, and a very clean, close-sounding recording suitable for medical guidance."
                ),
                "urgent_alert": (
                    "Aditi speaks with a serious Bengali tone and natural accent, "
                    "slightly fast pace, and clear emphasis on warning phrases, in a close, noise-free recording."
                ),
                "friend_casual": (
                    "Aditi speaks in a friendly, conversational Bengali tone, "
                    "moderate pace, slightly expressive, with a clear, close recording."
                ),
            },
        },
        "male": {
            "default_speaker": "Arjun",
            "styles": {
                "empathetic_motherly": (
                    "Arjun speaks gently with a soft Bengali accent, slightly slow pace, "
                    "and emotional warmth, captured in a clear, close-sounding recording."
                ),
                "neutral_nurse": (
                    "Arjun speaks with a neutral Bengali accent, moderate pace, "
                    "clear delivery and a clean close recording."
                ),
                "urgent_alert": (
                    "Arjun speaks with a serious Bengali tone, slightly fast pace, "
                    "and clear emphasis on important warnings, in a very clear recording."
                ),
                "friend_casual": (
                    "Arjun speaks in a relaxed, conversational Bengali tone, "
                    "normal pace, slightly expressive, with a close, clear recording."
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
                    "Sunita speaks with a warm, caring Marathi tone, slightly slow pace, "
                    "and expressive delivery, in a very clear, close recording."
                ),
                "neutral_nurse": (
                    "Sunita speaks with a clear Marathi accent, neutral tone, "
                    "moderate pace, and a clean close-sounding recording."
                ),
                "urgent_alert": (
                    "Sunita speaks firmly with a serious Marathi tone, slightly fast pace, "
                    "and clear stress on warning phrases, in a noise-free close recording."
                ),
                "friend_casual": (
                    "Sunita speaks in a friendly, conversational Marathi tone, "
                    "normal speed, slightly expressive, and clearly recorded."
                ),
            },
        },
        "male": {
            "default_speaker": "Sanjay",
            "styles": {
                "empathetic_motherly": (
                    "Sanjay speaks gently with emotional warmth in a Marathi accent, "
                    "slightly slow pace, and clear close recording."
                ),
                "neutral_nurse": (
                    "Sanjay speaks with a neutral Marathi tone, moderate pace, "
                    "and a very clear close-sounding recording."
                ),
                "urgent_alert": (
                    "Sanjay speaks with a serious Marathi tone, fast pace, "
                    "and clear emphasis on urgent content, in a clean recording."
                ),
                "friend_casual": (
                    "Sanjay speaks in a relaxed, conversational Marathi tone, "
                    "normal pace, and slightly expressive delivery with a clear recording."
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
                    "Lalitha speaks with a warm, caring Telugu tone, slightly slow pace, "
                    "and gentle expressiveness, in a very clear, close recording."
                ),
                "neutral_nurse": (
                    "Lalitha speaks in a neutral Telugu accent, moderate pace, "
                    "and clear, close recording suitable for instructions."
                ),
                "urgent_alert": (
                    "Lalitha speaks with a serious Telugu tone, slightly fast pace, "
                    "and clear stress on warning phrases, in a close, noise-free recording."
                ),
                "friend_casual": (
                    "Lalitha speaks in a friendly, conversational Telugu tone, "
                    "normal speed, slightly expressive, with clear audio."
                ),
            },
        },
        "male": {
            "default_speaker": "Prakash",
            "styles": {
                "empathetic_motherly": (
                    "Prakash speaks gently with emotional warmth in a Telugu accent, "
                    "slightly slow pace, and clear close recording."
                ),
                "neutral_nurse": (
                    "Prakash speaks in a neutral Telugu tone, moderate pace, "
                    "and a clean, close recording."
                ),
                "urgent_alert": (
                    "Prakash speaks with a serious Telugu tone, fast pace, "
                    "and sharp emphasis on urgent parts, captured clearly."
                ),
                "friend_casual": (
                    "Prakash speaks in a relaxed, conversational Telugu tone, "
                    "normal pace, slightly expressive, and clearly recorded."
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
                    "Anu speaks with a warm, caring Kannada tone, slightly slow pace, "
                    "and gentle expressiveness, in a clear, close-sounding recording."
                ),
                "neutral_nurse": (
                    "Anu speaks with a neutral Kannada accent, moderate pace, "
                    "and clean, close recording suitable for health counselling."
                ),
                "urgent_alert": (
                    "Anu speaks with a serious Kannada tone, slightly fast pace, "
                    "and clear emphasis on warnings, in a very clear recording."
                ),
                "friend_casual": (
                    "Anu speaks in a friendly, conversational Kannada tone, "
                    "normal speed, slightly expressive, with clear audio."
                ),
            },
        },
        "male": {
            "default_speaker": "Suresh",
            "styles": {
                "empathetic_motherly": (
                    "Suresh speaks gently with emotional warmth in a Kannada accent, "
                    "slightly slow pace, and a clear close recording."
                ),
                "neutral_nurse": (
                    "Suresh speaks in a neutral Kannada tone, moderate speed, "
                    "and a clean, close-sounding recording."
                ),
                "urgent_alert": (
                    "Suresh speaks with a firm Kannada tone, slightly fast pace, "
                    "and clear emphasis on urgent content, in a noise-free recording."
                ),
                "friend_casual": (
                    "Suresh speaks in a relaxed, conversational Kannada tone, "
                    "normal pace, slightly expressive, and clearly recorded."
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
                    "Neha speaks with a warm, caring Gujarati tone, slightly slow pace, "
                    "and emotional warmth, in a very clear, close recording."
                ),
                "neutral_nurse": (
                    "Neha speaks with a neutral Gujarati accent, moderate pace, "
                    "and a clean, close-sounding recording."
                ),
                "urgent_alert": (
                    "Neha speaks with a serious Gujarati tone, slightly fast pace, "
                    "and clear emphasis on warnings, in a very clear recording."
                ),
                "friend_casual": (
                    "Neha speaks in a friendly, conversational Gujarati tone, "
                    "normal pace, slightly expressive, with clear audio."
                ),
            },
        },
        "male": {
            "default_speaker": "Yash",
            "styles": {
                "empathetic_motherly": (
                    "Yash speaks gently with emotional warmth in a Gujarati accent, "
                    "slightly slow pace, and clear close recording."
                ),
                "neutral_nurse": (
                    "Yash speaks in a neutral Gujarati tone, moderate speed, "
                    "and a clean, close recording."
                ),
                "urgent_alert": (
                    "Yash speaks with a firm Gujarati tone, slightly fast pace, "
                    "and clear stress on urgent phrases, in a noise-free recording."
                ),
                "friend_casual": (
                    "Yash speaks in a relaxed, conversational Gujarati tone, "
                    "normal pace, slightly expressive, with clear audio."
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
                    "Mary speaks in Indian English with a warm, caring tone. "
                    "Her voice has a slightly slow pace, gentle expressiveness, "
                    "and very clear, close-up audio, suitable for counselling pregnant women."
                ),
                "neutral_nurse": (
                    "Mary speaks in neutral Indian English, moderate speed, "
                    "clear articulation, and a clean close recording suitable for medical instructions."
                ),
                "urgent_alert": (
                    "Mary speaks in serious Indian English, slightly fast, "
                    "with clear emphasis on warning phrases and a very clear, close-sounding recording."
                ),
                "friend_casual": (
                    "Mary speaks in a friendly, conversational Indian English tone, "
                    "normal pace, slightly expressive, with clear audio."
                ),
            },
        },
        "male": {
            "default_speaker": "Thoma",
            "styles": {
                "empathetic_motherly": (
                    "Thoma speaks in Indian English with a gentle, reassuring tone, "
                    "slightly slow pace, and clear close recording."
                ),
                "neutral_nurse": (
                    "Thoma speaks in neutral Indian English, moderate speed, "
                    "and a clean close-sounding recording with clear articulation."
                ),
                "urgent_alert": (
                    "Thoma speaks in serious Indian English, slightly fast pace, "
                    "with clear stress on urgent phrases, and very clear audio."
                ),
                "friend_casual": (
                    "Thoma speaks in a relaxed, conversational Indian English tone, "
                    "normal pace, slightly expressive, with clear audio."
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
      - A real Indic speaker name (Divya, Rohit, Aditi, etc.)
      - Per-language, per-style descriptions
      - Optional dialect note for Bhojpuri / Magadhi / Chhattisgarhi / Maithili
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
