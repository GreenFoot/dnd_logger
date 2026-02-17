"""Lightweight i18n module — dict-based translations with tr() lookup."""

import importlib
import logging

log = logging.getLogger(__name__)

_current_lang: str = "en"
_strings: dict[str, str] = {}


def tr(key: str, **kwargs) -> str:
    """Look up a translation key, format with kwargs, fall back to key itself."""
    text = _strings.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def set_language(lang: str) -> None:
    """Load English as base, then overlay the requested language."""
    global _current_lang, _strings

    # Always start from English base
    try:
        en_mod = importlib.import_module(".en", package=__name__)
        _strings = dict(en_mod.STRINGS)
    except ImportError:
        log.error("Could not load English translations (i18n/en.py)")
        _strings = {}

    # Overlay target language (skip if English)
    if lang != "en":
        try:
            lang_mod = importlib.import_module(f".{lang}", package=__name__)
            _strings.update(lang_mod.STRINGS)
        except ImportError:
            log.warning("No translation module for '%s', falling back to English", lang)

    _current_lang = lang


def get_language() -> str:
    """Return the active language code."""
    return _current_lang
