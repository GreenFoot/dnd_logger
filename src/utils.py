"""Utility functions: resource paths, config I/O, helpers."""

import json
import logging
import os
import sys

log = logging.getLogger(__name__)

_APP_NAME = "DnD Logger"

# Keys that belong in shared_config.json (synced between players)
SHARED_CONFIG_KEYS = {
    "context_bias",
    "language",
    "transcription_model",
    "summary_model",
    "chunk_duration_minutes",
    "diarize",
    "prompt_summary_system",
    "prompt_condense",
    "prompt_quest_extraction",
}

_DEFAULT_CONFIG = {
    "api_key": "",
    "audio_device": None,
    "sample_rate": 16000,
    "channels": 1,
    "chunk_duration_minutes": 60,
    "transcription_model": "voxtral-mini-latest",
    "summary_model": "mistral-large-latest",
    "language": "en",
    "diarize": False,
    "last_browser_url": "https://www.dndbeyond.com",
    "auto_update_check": True,
    "active_campaign": "",
    "campaigns": {},
    "prompt_summary_system": "",
    "prompt_condense": "",
    "prompt_quest_extraction": "",
    "context_bias": [
        "Dungeons & Dragons",
        "D&D",
        "Dungeon Master",
        "DM",
        "NPC",
        "PC",
        "Initiative",
        "Armor Class",
        "AC",
        "HP",
        "Hit Points",
        "Saving Throw",
        "Ability Check",
        "Skill Check",
        "Strength",
        "Dexterity",
        "Constitution",
        "Intelligence",
        "Wisdom",
        "Charisma",
        "Spell Slot",
        "Cantrip",
        "Multiclass",
        "Proficiency",
        "Short Rest",
        "Long Rest",
        "Concentration",
        "Advantage",
        "Disadvantage",
        "Natural 20",
        "Critical Hit",
        "Nat 20",
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

    - PyInstaller exe: %APPDATA%/DnD Logger
    - Dev mode: repo root (where main.py lives)
    """
    if hasattr(sys, "_MEIPASS"):
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(appdata, _APP_NAME)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def project_root() -> str:
    """Return the data root directory for config, sessions, journal, etc."""
    return ensure_dir(_data_dir())


def config_path() -> str:
    """Return the path to config.json in the project root."""
    return os.path.join(project_root(), "config.json")


# ── Campaign helpers ──────────────────────────────────────


def campaign_dir(name: str) -> str:
    """Return the directory for a given campaign name, creating it if needed."""
    return ensure_dir(os.path.join(project_root(), "campaigns", name))


def active_campaign_name(cfg: dict) -> str:
    """Return the active campaign name from config."""
    return cfg.get("active_campaign", "")


def active_campaign_dir(cfg: dict) -> str:
    """Return the directory for the active campaign."""
    return campaign_dir(active_campaign_name(cfg))


def campaign_drive_config(cfg: dict, name: str | None = None) -> dict:
    """Return the Drive config dict for a campaign (default: active campaign)."""
    if name is None:
        name = active_campaign_name(cfg)
    return cfg.get("campaigns", {}).get(name, {})


def list_campaigns(cfg: dict) -> list[str]:
    """Return sorted list of campaign names from the campaigns/ directory."""
    campaigns_root = os.path.join(project_root(), "campaigns")
    if not os.path.isdir(campaigns_root):
        return []
    return sorted(
        d
        for d in os.listdir(campaigns_root)
        if os.path.isdir(os.path.join(campaigns_root, d)) and not d.startswith("_")
    )


# ── Path functions (campaign-aware) ───────────────────────


def quest_log_path(cfg: dict) -> str:
    """Return the absolute path to the quest log file."""
    return os.path.join(active_campaign_dir(cfg), "quest_log.html")


def journal_path(cfg: dict) -> str:
    """Return the absolute path to the journal file."""
    return os.path.join(active_campaign_dir(cfg), "journal.html")


def sessions_dir(cfg: dict) -> str:
    """Return the absolute path to the sessions directory."""
    return ensure_dir(os.path.join(active_campaign_dir(cfg), "sessions"))


def shared_config_path(cfg: dict) -> str:
    """Return the path to shared_config.json in the active campaign dir."""
    return os.path.join(active_campaign_dir(cfg), "shared_config.json")


# ── Config I/O ────────────────────────────────────────────


def load_shared_config(cfg: dict) -> dict:
    """Load shared config from the active campaign's shared_config.json."""
    path = shared_config_path(cfg)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_shared_config(data: dict, cfg: dict) -> None:
    """Save shared config dict to the active campaign's shared_config.json."""
    path = shared_config_path(cfg)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_config() -> dict:
    """Load config from disk with layered merge: defaults -> shared -> personal."""
    cfg = dict(_DEFAULT_CONFIG)
    # Layer 1: personal config (to get active_campaign)
    path = config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            cfg.update(user_cfg)
        except (json.JSONDecodeError, OSError):
            pass
    # Layer 2: campaign shared config (only SHARED_CONFIG_KEYS)
    shared = load_shared_config(cfg)
    for k in SHARED_CONFIG_KEYS:
        if k in shared:
            cfg[k] = shared[k]

    # Initialize i18n from config language
    from . import i18n

    i18n.set_language(cfg.get("language", "en"))

    return cfg


def save_config(cfg: dict) -> None:
    """Save config dict, splitting shared keys into campaign's shared_config.json."""
    shared = {}
    personal = {}
    for k, v in cfg.items():
        if k in SHARED_CONFIG_KEYS:
            shared[k] = v
        else:
            personal[k] = v
    # Write personal config
    path = config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(personal, f, indent=2, ensure_ascii=False)
    # Write shared config to campaign dir
    save_shared_config(shared, cfg)


def ensure_dir(path: str) -> str:
    """Create directory if it doesn't exist, return the path."""
    os.makedirs(path, exist_ok=True)
    return path


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
    from .i18n import tr

    units = (
        tr("units.bytes"),
        tr("units.kilobytes"),
        tr("units.megabytes"),
        tr("units.gigabytes"),
    )
    for unit in units:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} {tr('units.terabytes')}"
