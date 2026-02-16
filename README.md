# D&D Logger

A PyQt6 desktop application for recording, transcribing, and summarizing Dungeons & Dragons sessions. Features an embedded D&D Beyond browser, a quest log, a journal, and an AI-powered transcription/summarization pipeline using the Mistral API.

The UI is in French. D&D-specific terms remain in English.

## Features

- **Audio recording** of game sessions with pause/resume (WAV, converted to FLAC for transcription)
- **AI transcription** via Mistral Voxtral with D&D-specific context bias and speaker diarization
- **AI summarization** in epic French fantasy style, with context chaining for long sessions
- **AI quest extraction** from session summaries with inline diff preview for review
- **Embedded D&D Beyond browser** with persistent login (cookies saved across sessions)
- **Quest log** -- rich text editor with auto-save, section folding, and search (Ctrl+F)
- **Journal** -- separate rich text editor for campaign notes with section folding and search
- **Google Drive sync** -- share quest log, journal, and campaign settings across players via a shared Google Drive folder
- **Text-to-speech** readback of summaries with animated overlay controls (play/pause/stop)
- **Audio import** -- import existing audio files (FLAC, WAV, MP3, OGG, M4A) for transcription
- **Dark fantasy theme** (Cinzel font, frost/aurora overlays)

## Project Structure

```
dnd_logger/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── installer.iss              # Inno Setup installer script
├── setup_appdata.py           # One-time script to migrate data to %APPDATA%
├── src/
│   ├── app.py                 # QMainWindow -- splitter layout, menus, sync engine init
│   ├── audio_recorder.py      # sounddevice InputStream -> queue -> writer thread -> WAV
│   ├── transcriber.py         # Audio chunking (FLAC) + Mistral Voxtral API pipeline
│   ├── summarizer.py          # Mistral chat summarization (epic French fantasy style)
│   ├── session_tab.py         # Record -> transcribe -> summarize UI tab
│   ├── quest_log.py           # Rich text quest log with auto-save
│   ├── journal.py             # Rich text journal editor
│   ├── quest_extractor.py     # AI quest extraction from summaries with diff preview
│   ├── rich_editor.py         # Shared rich text editor base (toolbar, search, folding)
│   ├── fold_manager.py        # Heading/bullet fold region detection and state
│   ├── fold_gutter.py         # Fold toggle gutter widget for editors
│   ├── diff_utils.py          # Shared inline diff highlighting utilities
│   ├── web_panel.py           # QWebEngineView with persistent D&D Beyond profile
│   ├── settings.py            # SettingsDialog + FirstRunWizard (API, Audio, Advanced, Drive)
│   ├── drive_credentials.py   # OAuth2 client config (gitignored, user-provided)
│   ├── drive_auth.py          # Google OAuth2 flow, token persistence
│   ├── drive_sync.py          # Google Drive sync engine (poll, upload, conflict detection)
│   ├── sync_conflict_dialog.py # Conflict resolution UI (local vs remote vs merge)
│   ├── tts_engine.py          # pyttsx3 French voice TTS
│   ├── tts_overlay.py         # Animated TTS playback overlay (play/pause/stop)
│   ├── snow_particles.py      # Snow particle overlay effect
│   ├── frost_overlay.py       # Gold filigree / frost overlay
│   └── utils.py               # Paths, config I/O (personal + shared split), helpers
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
google-api-python-client >= 2.100.0   # optional, for Google Drive sync
google-auth-httplib2 >= 0.1.1         # optional, for Google Drive sync
google-auth-oauthlib >= 1.1.0         # optional, for Google Drive sync
```

> **Note:** The Google API packages are only required if you want to use the Google Drive sync feature. The app works without them -- the Drive tab in settings will show a "dependencies missing" message.

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (use pythonw on Windows to avoid shell killing the app)
pythonw main.py
```

> **Note:** You must use `pythonw` instead of `python` on Windows. Using `python` causes the shell parent process to kill the app when it loses focus.

### First Run

On first launch:
1. A campaign creation dialog prompts for a campaign name (or to join one via Google Drive)
2. A setup wizard prompts for:
   - Mistral API key (required for transcription and summarization)
   - Audio input device selection

### D&D Beyond Login

The embedded browser uses a persistent QWebEngineProfile with `ForcePersistentCookies`, so your D&D Beyond login persists across sessions. **Google OAuth is not supported** in QWebEngine -- use email/password login instead.

## Data Storage

### In Development

All user data is stored in the project root directory:

```
dnd_logger/
├── config.json              # Personal settings (API key, audio, campaign config)
├── drive_token.json         # Google OAuth2 refresh token (gitignored)
├── dnd_logger.log           # Application log (rotating, 2 MB max, 3 backups)
├── campaigns/
│   ├── <campaign_name>/
│   │   ├── quest_log.html       # Quest log content (auto-saved, synced via Drive)
│   │   ├── journal.html         # Journal content (auto-saved, synced via Drive)
│   │   ├── shared_config.json   # Shared settings (synced via Drive)
│   │   ├── drive_sync_state.json # Sync state tracking
│   │   └── sessions/
│   │       └── session_YYYYMMDD_HHMMSS/
│   │           ├── recording.wav       # Raw audio recording
│   │           ├── full_audio.flac     # FLAC conversion
│   │           ├── chunk_NNN.flac      # FLAC chunks (only if audio > 2.5h)
│   │           └── transcript.txt      # Transcription output
│   └── _trash/                  # Deleted campaigns (restorable)
└── browser_data/                # QWebEngine profile (cookies, cache, local storage)
```

### As a Compiled Executable

User data is stored in `%APPDATA%\DnDLogger\` with the same structure as above. Bundled assets (fonts, images, stylesheets) remain inside the PyInstaller bundle.

To migrate existing data from a development setup to the exe data directory, run:

```bash
python setup_appdata.py            # skip files that already exist
python setup_appdata.py --force    # overwrite all files
```

This copies `config.json`, campaign data, and `sessions/` to `%APPDATA%\DnDLogger\`.

## Building the Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the spec file (--onedir mode, required for QWebEngine)
pyinstaller dnd_logger.spec --noconfirm
```

The output is in `dist/DnD Logger/`. The entry point is `DnD Logger.exe`.

> **Important:** The `--onefile` mode is not compatible with QWebEngine. The spec file uses `--onedir` with `collect_all` for QtWebEngine data and binaries.

## Creating the Installer

The project includes an [Inno Setup](https://jrsoftware.org/isinfo.php) script to package the app as a standard Windows installer. The installer requires **no admin rights**.

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

The output is `installer_output/DnDLogger_Setup.exe`.

### What the installer does

- Installs the app to `%LOCALAPPDATA%\DnD Logger\` (no admin rights needed)
- Creates a Start Menu entry with an uninstaller
- Optionally creates a desktop shortcut
- Offers to launch the app after installation
- French language UI

### Install locations summary

| What | Where |
|------|-------|
| App binaries | `%LOCALAPPDATA%\DnD Logger\` |
| User data | `%APPDATA%\DnDLogger\` |

### Distributing

To distribute the app, share **one** of the following:

- **Installer (recommended):** `installer_output/DnDLogger_Setup.exe` -- single file, handles installation and shortcuts
- **Portable:** the entire `dist/DnD Logger/` folder -- run `DnD Logger.exe` directly, no installation needed

## Audio Pipeline

1. **Recording:** `sounddevice` InputStream captures audio via PortAudio callback into a queue, a writer thread writes to WAV in real time (constant memory usage)
2. **Chunking:** If the recording exceeds 2.5 hours (configurable), it is split into FLAC chunks with 10-second overlap
3. **Conversion:** WAV is converted to FLAC before upload (lossless, ~50-60% smaller)
4. **Transcription:** Each chunk is uploaded to the Mistral Voxtral API with D&D context bias and French language setting. Retries on rate limits (429)
5. **Summarization:** The transcript is sent to Mistral chat for summarization in epic French fantasy style. Transcripts exceeding 28k characters use two-stage summarization with context chaining
6. **Quest extraction:** Quests mentioned in the summary can be extracted and added to the quest log

## Configuration

Settings are split across two files:

### `config.json` -- Personal settings (not synced)

| Key | Default | Description |
|-----|---------|-------------|
| `api_key` | `""` | Mistral API key |
| `audio_device` | `null` | Audio input device index |
| `sample_rate` | `16000` | Recording sample rate (Hz) |
| `channels` | `1` | Recording channels (mono) |
| `last_browser_url` | `"https://www.dndbeyond.com"` | Last visited URL in embedded browser |
| `active_campaign` | `""` | Currently active campaign name |
| `campaigns` | `{}` | Per-campaign config (Drive sync enabled, folder ID) |

### `shared_config.json` -- Shared settings (synced via Drive)

| Key | Default | Description |
|-----|---------|-------------|
| `chunk_duration_minutes` | `60` | Max chunk duration before splitting |
| `transcription_model` | `"voxtral-mini-latest"` | Mistral transcription model |
| `summary_model` | `"mistral-large-latest"` | Mistral summarization model |
| `language` | `"fr"` | Transcription language |
| `diarize` | `false` | Enable speaker diarization |
| `context_bias` | *(D&D terms)* | Terms to bias transcription toward |

> On first run, shared keys are automatically migrated from `config.json` to `shared_config.json`. If `shared_config.json` is missing, all settings are read from `config.json` as a fallback.

## Google Drive Sync

The app can sync the quest log, journal, and shared campaign settings across multiple players via a shared Google Drive folder.

### Setup (one-time, for the developer)

1. Go to [Google Cloud Console](https://console.cloud.google.com) and create a project
2. Enable the **Google Drive API**
3. Create **OAuth 2.0 credentials** with application type "Desktop app"
4. Paste the `client_id` and `client_secret` into `src/drive_credentials.py`
5. Add test users (< 100) or publish to production

### Usage

1. Open **Settings > Google Drive** and click "Se connecter" -- a browser window opens for Google login
2. Check **"Activer la synchronisation"** -- this creates a Drive folder for the active campaign
3. Share the campaign folder ID (shown in settings, copyable) with other players
4. Other players use "Rejoindre via Google Drive" when creating a new campaign and paste the folder ID

### How it works

- **Upload**: After a local save, the file is uploaded to Drive after a 10-second debounce
- **Download**: Every 30 seconds, the app polls Drive for changes and downloads updated files
- **Conflicts**: If both local and remote changed since the last sync, a conflict resolution dialog appears with side-by-side comparison and a merged editor
- **Files synced**: `quest_log.html`, `journal.html`, `shared_config.json`
- **Status**: A status label in the bottom-right shows the current sync state (idle/syncing/conflict/error/offline)
