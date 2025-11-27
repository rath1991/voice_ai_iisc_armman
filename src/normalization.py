# normalization.py

import re

# simple number words – extend as needed
NUM_WORDS_HI = {
    0: "shoonya", 1: "ek", 2: "do", 3: "teen", 4: "chaar", 5: "paanch",
    6: "chhe", 7: "saat", 8: "aath", 9: "nau", 10: "das",
    100: "sau"
}
NUM_WORDS_EN = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
    5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    100: "hundred"
}
NUM_WORDS_BN = {
    0: "shunno", 1: "ek", 2: "dui", 3: "tin", 4: "char", 5: "pach",
    6: "chhoy", 7: "sat", 8: "aat", 9: "noy", 10: "dosh",
    100: "eksho"  # used with extra words, keep simple
}


def _normalize_whitespace(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _expand_abbreviations(text: str, lang: str) -> str:
    pairs = {
        "en": {
            r"\bDr\.": "doctor",
            r"\bNo\.": "number",
            r"\bkg\b": "kilogram",
        },
        "hi": {
            r"\bDr\.": "डॉक्टर",
        },
        "bn": {
            r"\bDr\.": "ডাক্তার",
        },
    }
    lang_pairs = pairs.get(lang, {})
    for pattern, repl in lang_pairs.items():
        text = re.sub(pattern, repl, text)
    return text


def _number_to_words_en(n: int) -> str:
    # trivial impl for small numbers – enough for demo
    if n in NUM_WORDS_EN:
        return NUM_WORDS_EN[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        tens_word = {
            2: "twenty", 3: "thirty", 4: "forty",
            5: "fifty", 6: "sixty", 7: "seventy",
            8: "eighty", 9: "ninety",
        }.get(tens, "")
        if ones == 0:
            return tens_word
        return f"{tens_word} {NUM_WORDS_EN[ones]}"
    # fallback
    return str(n)


def _number_to_words_hi(n: int) -> str:
    # SUPER crude – you can improve later
    if n in NUM_WORDS_HI:
        return NUM_WORDS_HI[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        # cheat: just spell digits
        return " ".join(NUM_WORDS_HI[int(d)] for d in str(n))
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        res = f"{NUM_WORDS_HI[hundreds]} sau"
        if rest:
            res += " " + " ".join(NUM_WORDS_HI[int(d)] for d in str(rest))
        return res
    return str(n)


def _number_to_words_bn(n: int) -> str:
    # also crude
    if n in NUM_WORDS_BN:
        return NUM_WORDS_BN[n]
    return str(n)


def _replace_numbers(text: str, lang: str) -> str:
    def repl(match):
        num_str = match.group(0)
        try:
            n = int(num_str)
        except ValueError:
            return num_str
        if lang == "en":
            return _number_to_words_en(n)
        elif lang in {"hi", "bho", "mag", "hne", "mai"}:
            return _number_to_words_hi(n)
        elif lang == "bn":
            return _number_to_words_bn(n)
        else:
            return num_str

    return re.sub(r"\d+", repl, text)


def normalize_text(text: str, lang: str) -> str:
    """
    Minimal text normalization for Round 1:
    - whitespace
    - abbreviations
    - number expansion
    """
    text = _normalize_whitespace(text)
    text = _expand_abbreviations(text, lang)
    text = _replace_numbers(text, lang)
    return text
