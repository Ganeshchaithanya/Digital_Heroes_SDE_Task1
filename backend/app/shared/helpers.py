"""
Shared helper functions.
"""
from typing import List


def clean_text(text: str) -> str:
    """Normalize whitespace in text strings."""
    if not text:
        return ""
    return " ".join(text.split()).strip()


def count_words(text: str) -> int:
    """Accurately count words in a string."""
    cleaned = clean_text(text)
    if not cleaned:
        return 0
    return len(cleaned.split())
