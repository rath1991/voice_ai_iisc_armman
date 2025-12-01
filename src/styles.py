# styles.py

from config_loader import CONFIG

SUPPORTED_LANGS = CONFIG["supported_languages"]

DIALECT_TO_BASE_LANG = {
    "bho": "hi",
    "mag": "hi",
    "hne": "hi",
    "mai": "hi",
}

# Explicitly mapping best speakers for Round 1 (English + Gujarati)
LANG_SPEAKERS = {
    "hi": {"female": ["Divya", "Rani"], "male": ["Rohit", "Aman"]},
    "bn": {"female": ["Aditi", "Rashmi"], "male": ["Arjun", "Tapan"]},
    "mr": {"female": ["Sunita", "Radha"], "male": ["Sanjay", "Varun"]},
    "te": {"female": ["Lalitha"], "male": ["Prakash"]},
    "kn": {"female": ["Anu"], "male": ["Suresh"]},
    "gu": {"female": ["Neha"], "male": ["Yash"]},  # CRITICAL: Use these names
    "en": {"female": ["Mary"], "male": ["Thoma"]}, # CRITICAL: Mary/Thoma are best for Indian English
}

LANG_SPEAKER_STYLES = {
    # ... (Keep Hindi, Bengali, Marathi, Telugu, Kannada sections as they were) ...
    # [Insert your existing HI/BN/MR/TE/KN dictionaries here]

    # Gujarati - Ensure "Neha" and "Yash" are used explicitly
    "gu": {
        "female": {
            "default_speaker": "Neha",
            "styles": {
                "empathetic_motherly": (
                    "Neha speaks with a warm, caring Gujarati tone and slightly slow pace in a close-sounding environment. "
                    "Her voice has a moderate pitch with emotional warmth and expressiveness, "
                    "delivered with moderate speed. The recording is of very high quality, very clear."
                ),
                "neutral_nurse": (
                    "Neha speaks at a moderate pace with a neutral Gujarati tone in a close-sounding environment. "
                    "Her voice has a balanced pitch with slight expressiveness, "
                    "delivered at normal speed. The recording is of very high quality, very clear audio."
                ),
                "urgent_alert": (
                    "Neha speaks with a serious Gujarati tone at a slightly fast pace. "
                    "Her voice has a moderate pitch with clear emphasis on warnings, "
                    "delivered with faster than normal speed. The recording is of very high quality."
                ),
                "friend_casual": (
                    "Neha speaks in a friendly, conversational Gujarati tone at a normal pace. "
                    "Her voice has a balanced pitch with slightly expressive delivery. "
                    "The recording is of high quality, clear audio."
                ),
            },
        },
        "male": {
            "default_speaker": "Yash",
            "styles": {
                "empathetic_motherly": (
                    "Yash speaks with a gentle Gujarati tone and slightly slow pace in a close-sounding environment. "
                    "His voice has a moderate pitch with emotional warmth. "
                    "The recording is of very high quality, very clear."
                ),
                "neutral_nurse": (
                    "Yash speaks at a moderate pace with a neutral Gujarati tone. "
                    "His voice has a balanced pitch with slight expressiveness. "
                    "The recording is of very high quality, very clear audio."
                ),
                "urgent_alert": (
                    "Yash speaks with a firm Gujarati tone at a slightly fast pace. "
                    "His voice has a moderate pitch with clear stress on urgent phrases. "
                    "The recording is of very high quality, very clear audio."
                ),
                "friend_casual": (
                    "Yash speaks in a relaxed, conversational Gujarati tone at a normal pace. "
                    "His voice has a balanced pitch with slightly expressive delivery. "
                    "The recording is of high quality."
                ),
            },
        },
    },

    # English - UPDATED to use "Mary" and "Thoma"
    "en": {
        "female": {
            "default_speaker": "Mary",
            "styles": {
                "empathetic_motherly": (
                    "Mary speaks with an Indian English accent in a warm, caring tone with a slightly slow pace. "
                    "Her voice has a slightly high pitch with gentle expressiveness. "
                    "The recording is of very high quality, very clear, close up."
                ),
                "neutral_nurse": (
                    "Mary speaks with an Indian English accent in a neutral, clear tone at a moderate pace. "
                    "Her voice has a balanced pitch with slight expressiveness. "
                    "The recording is of very high quality, very clear audio, suitable for medical instructions."
                ),
                "urgent_alert": (
                    "Mary speaks with an Indian English accent in a serious, firm tone at a slightly fast pace. "
                    "Her voice has a moderate pitch with clear emphasis on warning phrases. "
                    "The recording is of very high quality, very clear audio."
                ),
                "friend_casual": (
                    "Mary speaks with an Indian English accent in a friendly, conversational tone at a normal pace. "
                    "Her voice has a balanced pitch with slightly expressive delivery. "
                    "The recording is of high quality, clear audio."
                ),
            },
        },
        "male": {
            "default_speaker": "Thoma",
            "styles": {
                "empathetic_motherly": (
                    "Thoma speaks with an Indian English accent in a gentle, reassuring tone with a slightly slow pace. "
                    "His voice has a moderate pitch with soft expressiveness. "
                    "The recording is of very high quality, very clear."
                ),
                "neutral_nurse": (
                    "Thoma speaks with an Indian English accent in a neutral, clear tone at a moderate pace. "
                    "His voice has a balanced pitch with slight expressiveness. "
                    "The recording is of very high quality, very clear audio."
                ),
                "urgent_alert": (
                    "Thoma speaks with an Indian English accent in a firm, serious tone at a slightly fast pace. "
                    "His voice has a moderate pitch with clear stress on urgent phrases. "
                    "The recording is of very high quality, very clear audio."
                ),
                "friend_casual": (
                    "Thoma speaks with an Indian English accent in a relaxed, conversational tone at a normal pace. "
                    "His voice has a balanced pitch with slightly expressive delivery. "
                    "The recording is of high quality."
                ),
            },
        },
    },
}

def resolve_effective_lang(lang_code: str) -> str:
    return DIALECT_TO_BASE_LANG.get(lang_code, lang_code)

def get_speaker_name(lang_code: str, speaker_gender: str = "female") -> str:
    base_lang = resolve_effective_lang(lang_code)
    lang_cfg = LANG_SPEAKER_STYLES.get(base_lang) or LANG_SPEAKER_STYLES["hi"]
    gender_key = "male" if speaker_gender and speaker_gender.lower() == "male" else "female"
    return lang_cfg.get(gender_key, {}).get("default_speaker", "Aditi")

def build_caption(lang_code: str, style: str, speaker_gender: str = "female") -> str:
    # (Same as before, but now ensures the styles dictionary uses names like 'Mary'/'Neha')
    base_lang = resolve_effective_lang(lang_code)
    lang_cfg = LANG_SPEAKER_STYLES.get(base_lang) or LANG_SPEAKER_STYLES["hi"]
    gender_key = "male" if speaker_gender and speaker_gender.lower() == "male" else "female"
    
    # Safety fallback
    if gender_key not in lang_cfg: gender_key = "female"
    
    gender_cfg = lang_cfg[gender_key]
    styles = gender_cfg["styles"]
    
    style_desc = styles.get(style) or styles.get("neutral_nurse") or list(styles.values())[0]
    
    caption = style_desc
    
    # Append dialect nuances
    if lang_code == "bho": caption += " The speech has a natural Bhojpuri-influenced Hindi accent."
    elif lang_code == "mag": caption += " The speech has a natural Magadhi-flavoured Hindi accent."
    elif lang_code == "hne": caption += " The speech has a natural Chhattisgarhi-flavoured Hindi accent."
    elif lang_code == "mai": caption += " The speech is delivered in a Maithili-influenced Hindi accent."

    return caption