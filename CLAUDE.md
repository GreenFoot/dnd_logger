# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

D&D Logger is a PySide6 desktop app (Windows-only) for recording, transcribing, and summarizing D&D sessions. It uses the Mistral API for AI features and includes an embedded D&D Beyond browser, quest log, journal, and Google Drive sync.

## Commands

```bash
# Run the app (MUST use pythonw on Windows — python causes shell to kill app on focus loss)
pythonw main.py

# Install dependencies
pip install -r requirements.txt

# Lint
black --check --line-length 120 src/ main.py
isort --check --profile black src/ main.py
flake8 src/ main.py
pylint src/ main.py     # .pylintrc enables only a small subset of checks

# Build executable (--onedir required for QWebEngine)
pip install pyinstaller
pyinstaller dnd_logger.spec --noconfirm

# Build installer (requires Inno Setup)
iscc installer.iss
```

There are no tests in this project.

## Architecture

**Entry point:** `main.py` — sets up logging, exception hook, QApplication, launches `DndLoggerApp`.

**Main window (`src/app.py`):** QMainWindow with a QSplitter — embedded browser on the left, a QTabWidget on the right with Session, Quest Log, and Journal tabs. Manages campaign switching, theme loading, Drive sync engine lifecycle, TTS, and auto-update checks.

**Audio pipeline (`src/audio_recorder.py` → `src/transcriber.py` → `src/summarizer.py`):**
- Recording: sounddevice InputStream → callback queue → writer thread → WAV (constant memory)
- Transcription: WAV→FLAC conversion, chunking if >2.5h, Mistral Voxtral file-upload API
- Summarization: Mistral chat with epic fantasy style. Two-stage condensation if transcript >28k chars

**Quest extraction (`src/quest_extractor.py`):** AI extracts quests from summaries, shows inline diff preview before applying to quest log.

**Rich text editors (`src/rich_editor.py`, `src/quest_log.py`, `src/journal.py`):** `RichEditor` is the shared base class with toolbar, search (Ctrl+F), and section folding. `QuestLogWidget` and `JournalWidget` extend it with auto-save (2s debounce) and HTML persistence.

**Folding system (`src/fold_manager.py`, `src/fold_gutter.py`):** Detects heading/bullet fold regions, provides gutter toggle widget.

**Web panel (`src/web_panel.py`):** QWebEngineView with a named persistent profile (`ForcePersistentCookies`) for D&D Beyond login. Google OAuth is blocked in QWebEngine — only email/password login works.

**Google Drive sync (`src/drive_auth.py`, `src/drive_sync.py`, `src/sync_conflict_dialog.py`):** OAuth2 flow, poll-based sync engine (30s poll, 10s upload debounce), conflict resolution with side-by-side diff. Syncs `quest_log.html`, `journal.html`, `shared_config.json`. Credentials in `src/drive_credentials.py` (gitignored).

**Config (`src/utils.py`):** Two config files per campaign — `config.json` (personal, not synced) and `shared_config.json` (synced via Drive). `SHARED_CONFIG_KEYS` in utils.py defines which keys go where. `project_root()` returns repo root in dev, `%APPDATA%\DnDLogger` in frozen builds.

**i18n (`src/i18n/`):** Dict-based translations. `tr(key, **kwargs)` for lookup. English is always the base; other languages overlay. 7 languages (en/fr/de/es/it/nl/pt). D&D terms stay in English. Language can be switched live without restart.

**Theming:** 7 QSS themes in `assets/styles/` with metadata in `theme_meta.json`. Overlays: gold filigree corners (`src/filigree_overlay.py`), snow/particle effects (`src/snow_particles.py`).

**TTS (`src/tts_engine.py`, `src/tts_overlay.py`):** edge_tts for speech synthesis with animated overlay controls.

**Auto-update (`src/updater.py`):** Checks GitHub releases for newer versions, offers download.

## UI Framework

Uses **PySide6** (Qt for Python). Do NOT use PyQt6 imports. The spec file explicitly excludes PyQt5, PyQt6, and PySide2.

## Code Style

- **black** with line length 120
- **isort** with black profile
- **Docstrings:** Google format (Args/Returns/Raises)
- **pylint:** only a few checks enabled (see `.pylintrc`) — `missing-function-docstring`, `invalid-name`, `undefined-variable`, `used-before-assignment`, `no-member`, `attribute-defined-outside-init`
- Qt event overrides (`paintEvent`, `closeEvent`, `keyPressEvent`, etc.) are listed in pylint's `good-names` to allow camelCase

## Key Gotchas

- Must launch with `pythonw` not `python` on Windows
- QWebEngine requires `--onedir` PyInstaller mode (not `--onefile`)
- Google OAuth is blocked in QWebEngine — no workaround exists
- Version is injected into `src/__init__.py` by CI at build time (`__version__`)
- The `dist/` and `build/` directories contain PyInstaller output — ignore them when searching code
