import re
import unicodedata


def normalize_text(value: str) -> str:
    """Normaliza texto para búsquedas tolerantes a mayúsculas, tildes y símbolos."""

    text = unicodedata.normalize("NFD", value or "")
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = text.lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("av.", "avenida")
    text = text.replace("av ", "avenida ")
    text = text.replace("cl", "calle")
    text = text.replace("kr", "carrera")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def compact_name(value: str) -> str:
    """Devolver una versión corta para detectar transbordos por nombres similares."""

    text = normalize_text(value)
    removable_words = {
        "est",
        "estacion",
        "portal",
        "transmicable",
        "fincomercio",
        "unicervantes",
        "fng",
        "cc",
        "centro",
        "comercial",
    }
    words = [word for word in text.split() if word not in removable_words]
    return " ".join(words)
