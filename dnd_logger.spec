# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for DnD Logger."""

import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None
IS_MAC = sys.platform == "darwin"

# Collect all Qt WebEngine data
webengine_datas, webengine_binaries, webengine_hiddenimports = collect_all(
    "PySide6.QtWebEngineWidgets"
)
webengine_core_datas, webengine_core_binaries, webengine_core_hiddenimports = collect_all(
    "PySide6.QtWebEngineCore"
)
edge_tts_datas, edge_tts_binaries, edge_tts_hiddenimports = collect_all("edge_tts")

# Speakeasy-generated mistralai uses star imports and importlib.import_module for
# lazy attribute access, neither of which PyInstaller's modulegraph follows.
# collect_submodules pulls every mistralai.* module name (no data files / metadata,
# so it avoids the optional-dep breakage that collect_all caused in v1.3.1).
mistralai_hiddenimports = collect_submodules("mistralai")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=webengine_binaries + webengine_core_binaries + edge_tts_binaries,
    datas=[
        ("assets/fonts", "assets/fonts"),
        ("assets/styles", "assets/styles"),
        ("assets/images", "assets/images"),
        ("assets/sounds", "assets/sounds"),
    ]
    + webengine_datas
    + webengine_core_datas
    + edge_tts_datas,
    hiddenimports=[
        "sounddevice",
        "soundfile",
        "numpy",
        "requests",
        "googleapiclient",
        "googleapiclient.discovery",
        "google.auth",
        "google.auth.transport.requests",
        "google.oauth2.credentials",
        "google_auth_oauthlib",
        "google_auth_oauthlib.flow",
        "google_auth_httplib2",
        "src.i18n.en",
        "src.i18n.fr",
        "src.i18n.de",
        "src.i18n.es",
        "src.i18n.it",
        "src.i18n.nl",
        "src.i18n.pt",
    ]
    + webengine_hiddenimports
    + webengine_core_hiddenimports
    + edge_tts_hiddenimports
    + mistralai_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["PyQt5", "PyQt6", "PySide2"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="DnD Logger",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=not IS_MAC,  # UPX corrupts macOS binaries
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/images/app/icon.icns" if IS_MAC else "assets/images/app/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=not IS_MAC,
    upx_exclude=[],
    name="DnD Logger",
)

if IS_MAC:
    # Version is injected into src/__init__.py by CI before the build
    sys.path.insert(0, SPECPATH)
    from src import __version__

    app = BUNDLE(
        coll,
        name="DnD Logger.app",
        icon="assets/images/app/icon.icns",
        bundle_identifier="com.dndlogger.app",
        version=__version__,
        info_plist={
            "CFBundleDisplayName": "DnD Logger",
            "CFBundleShortVersionString": __version__,
            "NSHighResolutionCapable": True,
            # Without this, macOS silently denies microphone access to the app
            "NSMicrophoneUsageDescription": "DnD Logger records your D&D sessions to transcribe them.",
        },
    )
