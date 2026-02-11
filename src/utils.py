"""Utility functions: resource paths, config I/O, helpers."""

import json
import logging
import os
import sys
from pathlib import Path

log = logging.getLogger(__name__)

_APP_NAME = "IcewindDaleLogger"

_DEFAULT_CONFIG = {
    "api_key": "",
    "audio_device": None,
    "sample_rate": 16000,
    "channels": 1,
    "sessions_dir": "sessions",
    "quest_log_path": "quest_log.html",
    "journal_path": "journal.html",
    "chunk_duration_minutes": 150,
    "transcription_model": "mistral-small-latest",
    "summary_model": "mistral-small-latest",
    "language": "fr",
    "context_bias": [
        "Icewind Dale", "Faerun", "Dungeons & Dragons", "D&D",
        "Dungeon Master", "DM", "NPC", "PC",
        "Initiative", "Armor Class", "AC", "HP", "Hit Points",
        "Saving Throw", "Ability Check", "Skill Check",
        "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma",
        "Spell Slot", "Cantrip", "Multiclass", "Proficiency",
        "Ten-Towns", "Bryn Shander", "Targos", "Lonelywood", "Easthaven",
        "Auril", "Chardalyn", "Duergar", "Reghed",
        "Short Rest", "Long Rest", "Concentration", "Advantage", "Disadvantage",
        "Natural 20", "Critical Hit", "Nat 20"
    ],
}


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


def _data_dir() -> str:
    """Return the user-writable data directory for the app.

    - PyInstaller exe: %APPDATA%/IcewindDaleLogger
    - Dev mode: repo root (where main.py lives)
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), _APP_NAME)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def project_root() -> str:
    """Return the data root directory for config, sessions, journal, etc."""
    return ensure_dir(_data_dir())


def config_path() -> str:
    """Return the path to config.json in the project root."""
    return os.path.join(project_root(), "config.json")


def load_config() -> dict:
    """Load config from disk, merging with defaults for missing keys."""
    cfg = dict(_DEFAULT_CONFIG)
    path = config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            cfg.update(user_cfg)
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(cfg: dict) -> None:
    """Save config dict to disk."""
    path = config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def ensure_dir(path: str) -> str:
    """Create directory if it doesn't exist, return the path."""
    os.makedirs(path, exist_ok=True)
    return path


def sessions_dir(cfg: dict) -> str:
    """Return the absolute path to the sessions directory."""
    sd = cfg.get("sessions_dir", "sessions")
    if not os.path.isabs(sd):
        sd = os.path.join(project_root(), sd)
    return ensure_dir(sd)


def quest_log_path(cfg: dict) -> str:
    """Return the absolute path to the quest log file."""
    ql = cfg.get("quest_log_path", "quest_log.html")
    if not os.path.isabs(ql):
        ql = os.path.join(project_root(), ql)
    return ql


def journal_path(cfg: dict) -> str:
    """Return the absolute path to the journal file."""
    jp = cfg.get("journal_path", "journal.html")
    if not os.path.isabs(jp):
        jp = os.path.join(project_root(), jp)
    return jp


def browser_data_dir() -> str:
    """Return the absolute path to the browser data directory."""
    return ensure_dir(os.path.join(project_root(), "browser_data"))


def format_duration(seconds: int) -> str:
    """Format seconds as HH:MM:SS."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def format_file_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ("o", "Ko", "Mo", "Go"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} To"
