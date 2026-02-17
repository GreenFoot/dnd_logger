# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for DnD Logger."""

import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all Qt WebEngine data
webengine_datas, webengine_binaries, webengine_hiddenimports = collect_all(
    "PySide6.QtWebEngineWidgets"
)
webengine_core_datas, webengine_core_binaries, webengine_core_hiddenimports = collect_all(
    "PySide6.QtWebEngineCore"
)

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=webengine_binaries + webengine_core_binaries,
    datas=[
        ("assets/fonts", "assets/fonts"),
        ("assets/styles", "assets/styles"),
        ("assets/images", "assets/images"),
    ]
    + webengine_datas
    + webengine_core_datas,
    hiddenimports=[
        "sounddevice",
        "soundfile",
        "mistralai",
        "pyttsx3",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "numpy",
        "googleapiclient",
        "googleapiclient.discovery",
        "google.auth",
        "google.auth.transport.requests",
        "google.oauth2.credentials",
        "google_auth_oauthlib",
        "google_auth_oauthlib.flow",
        "google_auth_httplib2",
    ]
    + webengine_hiddenimports
    + webengine_core_hiddenimports,
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
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/images/app/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="DnD Logger",
)
