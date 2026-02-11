# Icewind Dale -- D&D Session Logger

A PyQt6 desktop application for recording, transcribing, and summarizing Dungeons & Dragons sessions. Features an embedded D&D Beyond browser, a quest log, a journal, and an AI-powered transcription/summarization pipeline using the Mistral API.

The UI is in French. D&D-specific terms remain in English.

## Features

- **Audio recording** of game sessions (WAV, converted to FLAC for transcription)
- **AI transcription** via Mistral Voxtral with D&D-specific context bias
- **AI summarization** in epic French fantasy style, with context chaining for long sessions
- **Embedded D&D Beyond browser** with persistent login (cookies saved across sessions)
- **Quest log** -- rich text editor with auto-save
- **Journal** -- separate rich text editor for campaign notes
- **Text-to-speech** readback of summaries (French voice, pyttsx3)
- **Audio import** -- import existing audio files (FLAC, WAV, MP3, OGG, M4A) for transcription
- **Dark fantasy theme** (Icewind Dale aesthetic, Cinzel font, frost/aurora overlays)

## Project Structure

```
dnd_logger/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── icewind_dale.spec          # PyInstaller build spec
├── setup_appdata.py           # One-time script to migrate data to %APPDATA%
├── src/
│   ├── app.py                 # QMainWindow -- splitter layout, menus, settings
│   ├── audio_recorder.py      # sounddevice InputStream -> queue -> writer thread -> WAV
│   ├── transcriber.py         # Audio chunking (FLAC) + Mistral Voxtral API pipeline
│   ├── summarizer.py          # Mistral chat summarization (epic French fantasy style)
│   ├── session_tab.py         # Record -> transcribe -> summarize UI tab
│   ├── quest_log.py           # Rich text quest log with auto-save
│   ├── journal.py             # Rich text journal editor
│   ├── quest_extractor.py     # AI extraction of quests from summaries
│   ├── rich_editor.py         # Shared rich text editor base widget
│   ├── web_panel.py           # QWebEngineView with persistent D&D Beyond profile
│   ├── settings.py            # SettingsDialog + FirstRunWizard
│   ├── tts_engine.py          # pyttsx3 French voice TTS
│   ├── snow_particles.py      # Snow particle overlay effect
│   ├── frost_overlay.py       # Gold filigree / frost overlay
│   └── utils.py               # Paths, config I/O, helpers
└── assets/
    ├── fonts/                 # Cinzel font family (.ttf)
    ├── images/                # Icons, backgrounds, banners
    └── styles/
        └── icewind.qss        # Dark fantasy Qt stylesheet
```

## Requirements

- Python 3.11+
- Windows (uses pyttsx3 SAPI5 driver, QWebEngine, Windows-specific paths)

### Python Dependencies

```
PyQt6 >= 6.6.0
PyQt6-WebEngine >= 6.6.0
sounddevice >= 0.4.6
soundfile >= 0.12.1
mistralai >= 1.0.0
pyttsx3 >= 2.90
numpy
```

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (use pythonw on Windows to avoid shell killing the app)
pythonw main.py
```

> **Note:** You must use `pythonw` instead of `python` on Windows. Using `python` causes the shell parent process to kill the app when it loses focus.

### First Run

On first launch, a setup wizard will prompt for:
- Mistral API key (required for transcription and summarization)
- Audio input device selection

### D&D Beyond Login

The embedded browser uses a persistent QWebEngineProfile with `ForcePersistentCookies`, so your D&D Beyond login persists across sessions. **Google OAuth is not supported** in QWebEngine -- use email/password login instead.

## Data Storage

### In Development

All user data is stored in the project root directory:

```
dnd_logger/
├── config.json          # API key, audio settings, preferences
├── quest_log.html       # Quest log content (auto-saved)
├── journal.html         # Journal content (auto-saved)
├── icewind_dale.log     # Application log (rotating, 2 MB max, 3 backups)
├── sessions/            # Recorded audio and transcripts
│   └── session_YYYYMMDD_HHMMSS/
│       ├── recording.wav       # Raw audio recording
│       ├── full_audio.flac     # FLAC conversion (created during transcription)
│       ├── chunk_NNN.flac      # FLAC chunks (only if audio > 2.5h)
│       └── transcript.txt      # Transcription output
└── browser_data/        # QWebEngine profile (cookies, cache, local storage)
```

### As a Compiled Executable

User data is stored in `%APPDATA%\IcewindDaleLogger\` with the same structure as above. Bundled assets (fonts, images, stylesheets) remain inside the PyInstaller bundle.

To migrate existing data from a development setup to the exe data directory, run:

```bash
python setup_appdata.py            # skip files that already exist
python setup_appdata.py --force    # overwrite all files
```

This copies `config.json`, `quest_log.html`, `journal.html`, and `sessions/` to `%APPDATA%\IcewindDaleLogger\`.

## Building the Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the spec file (--onedir mode, required for QWebEngine)
pyinstaller icewind_dale.spec --noconfirm
```

The output is in `dist/Icewind Dale/`. The entry point is `Icewind Dale.exe`.

> **Important:** The `--onefile` mode is not compatible with QWebEngine. The spec file uses `--onedir` with `collect_all` for QtWebEngine data and binaries.

## Creating the Installer

The project includes an [Inno Setup](https://jrsoftware.org/isinfo.php) script to package the app as a standard Windows installer. The installer requires **no admin rights** -- it installs to `%LOCALAPPDATA%\Icewind Dale\`.

### Prerequisites

Download and install [Inno Setup](https://jrsoftware.org/isdl.php) (free).

### Building the installer

1. First build the exe with PyInstaller (see above)
2. Then compile the installer:

```bash
# From the Inno Setup GUI: open installer.iss and click Build > Compile
# Or from command line (if iscc is in PATH):
iscc installer.iss
```

The output is `installer_output/IcewindDale_Setup.exe`.

### What the installer does

- Installs the app to `%LOCALAPPDATA%\Icewind Dale\` (no admin rights needed)
- Creates a Start Menu entry with an uninstaller
- Optionally creates a desktop shortcut
- Offers to launch the app after installation
- French language UI

### Install locations summary

| What | Where |
|------|-------|
| App binaries | `%LOCALAPPDATA%\Icewind Dale\` |
| User data | `%APPDATA%\IcewindDaleLogger\` |

### Distributing

To distribute the app, share **one** of the following:

- **Installer (recommended):** `installer_output/IcewindDale_Setup.exe` -- single file, handles installation and shortcuts
- **Portable:** the entire `dist/Icewind Dale/` folder -- run `Icewind Dale.exe` directly, no installation needed

## Audio Pipeline

1. **Recording:** `sounddevice` InputStream captures audio via PortAudio callback into a queue, a writer thread writes to WAV in real time (constant memory usage)
2. **Chunking:** If the recording exceeds 2.5 hours (configurable), it is split into FLAC chunks with 10-second overlap
3. **Conversion:** WAV is converted to FLAC before upload (lossless, ~50-60% smaller)
4. **Transcription:** Each chunk is uploaded to the Mistral Voxtral API with D&D context bias and French language setting. Retries on rate limits (429)
5. **Summarization:** The transcript is sent to Mistral chat for summarization in epic French fantasy style. Transcripts exceeding 28k characters use two-stage summarization with context chaining
6. **Quest extraction:** Quests mentioned in the summary can be extracted and added to the quest log

## Configuration

Settings are stored in `config.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `api_key` | `""` | Mistral API key |
| `audio_device` | `null` | Audio input device index |
| `sample_rate` | `16000` | Recording sample rate (Hz) |
| `channels` | `1` | Recording channels (mono) |
| `chunk_duration_minutes` | `150` | Max chunk duration before splitting |
| `language` | `"fr"` | Transcription language |
| `context_bias` | *(D&D terms)* | Terms to bias transcription toward |
| `sessions_dir` | `"sessions"` | Sessions directory (relative or absolute) |
| `quest_log_path` | `"quest_log.html"` | Quest log file path |
| `journal_path` | `"journal.html"` | Journal file path |
