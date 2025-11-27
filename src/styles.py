# styles.py

from config_loader import CONFIG

BASE_STYLE_CAPTIONS = {
    "empathetic_motherly": (
        "A clear warm female voice, slow pacing, gentle and caring tone as if speaking "
        "to a pregnant woman, no background noise, slightly expressive prosody."
    ),
    "neutral_nurse": (
        "A clear neutral female voice, normal pacing, polite and informative tone, "
        "no background noise, steady prosody."
    ),
    "urgent_alert": (
        "A serious female healthcare worker, slightly fast, urgent tone, emphasizing "
        "important warning phrases, no background noise."
    ),
    "friend_casual": (
        "A friendly young female voice, conversational tone, natural pacing, "
        "slightly expressive informal style."
    )
}

SUPPORTED_LANGS = CONFIG["supported_languages"]

DIALECT_TO_LANG = {
    "bho": "hi",
    "mag": "hi",
    "hne": "hi",
    "mai": "hi"
}

ACCENT_DESCRIPTORS = {
    "hi": "Hindi speaker with a neutral North Indian accent.",
    "bn": "Bengali speaker from Kolkata with a neutral urban accent.",
    "mr": "Marathi speaker with a standard Maharashtrian accent.",
    "te": "Telugu speaker with a standard Andhra/Telangana accent.",
    "kn": "Kannada speaker with a clear Karnataka accent.",
    "gu": "Gujarati speaker with a neutral Gujarati accent.",
    "en": "Indian English speaker with a mild neutral accent.",

    "bho": "Hindi speaker with a Bhojpuri-influenced accent.",
    "mag": "Hindi speaker with a Magadhi-influenced accent.",
    "hne": "Hindi speaker with a Chhattisgarhi-influenced accent.",
    "mai": "Hindi speaker with a Maithili-influenced accent."
}


def resolve_effective_lang(lang_code: str) -> str:
    return DIALECT_TO_LANG.get(lang_code, lang_code)


def build_caption(lang_code: str, style: str, speaker_gender: str = "female") -> str:
    style_desc = BASE_STYLE_CAPTIONS.get(style, BASE_STYLE_CAPTIONS["neutral_nurse"])
    accent_desc = ACCENT_DESCRIPTORS.get(lang_code, "Indian speaker with neutral accent.")

    if speaker_gender.lower() == "male":
        gender_phrase = "male voice"
    else:
        gender_phrase = "female voice"

    caption = f"A {gender_phrase}. {accent_desc} {style_desc}"
    return caption
