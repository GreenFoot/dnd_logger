"""German translations — Deutsche Ubersetzung aller UI-Texte und KI-Prompts."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "B",
    "units.kilobytes": "KB",
    "units.megabytes": "MB",
    "units.gigabytes": "GB",
    "units.terabytes": "TB",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "Datei",
    "app.menu.settings": "Einstellungen...",
    "app.menu.check_updates": "Nach Updates suchen...",
    "app.menu.save": "Speichern",
    "app.menu.quit": "Beenden",
    "app.menu.campaign": "Kampagne",
    "app.menu.new_campaign": "Neue Kampagne...",
    "app.menu.delete_campaign": "Kampagne loeschen...",
    "app.menu.restore_campaign": "Kampagne wiederherstellen...",
    "app.menu.theme": "Design",
    "app.menu.session": "Sitzung",
    "app.menu.record_stop": "Aufnahme / Stopp",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Tagebuch",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Sitzung",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "Keine Kampagnen gefunden.",
    "app.campaign.name_label": "Kampagnenname:",
    "app.campaign.name_placeholder": "Z.B.: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Erstellen",
    "app.campaign.delete_title": "Kampagne loeschen",
    "app.campaign.delete_label": "Kampagne zum Loeschen auswaehlen:",
    "app.campaign.delete_confirm_title": "Loeschung bestaetigen",
    "app.campaign.delete_confirm": 'Kampagne "{name}" loeschen?\nDateien werden nach campaigns/_trash/ verschoben.',
    "app.campaign.restore_title": "Kampagne wiederherstellen",
    "app.campaign.restore_label": "Kampagne zum Wiederherstellen auswaehlen:",
    "app.campaign.restore_none": "Keine archivierten Kampagnen.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Status:",
    "app.campaign.drive_not_connected": "Nicht verbunden",
    "app.campaign.drive_connected": "Verbunden",
    "app.campaign.drive_btn_login": "Anmelden",
    "app.campaign.drive_logging_in": "Verbindung wird hergestellt...",
    "app.campaign.drive_folder_id_label": "Ordner-ID:",
    "app.campaign.drive_folder_placeholder": "Freigegebene Ordner-ID einfuegen...",
    "app.campaign.drive_btn_join": "Beitreten",
    "app.campaign.drive_join_hint": "(zum Beitreten)",
    "app.campaign.name_empty": "Der Name darf nicht leer sein.",
    "app.campaign.name_exists": 'Die Kampagne "{name}" existiert bereits.',
    "app.campaign.drive_paste_id": "Freigegebene Ordner-ID einfuegen.",
    "app.campaign.drive_login_first": "Zuerst bei Google Drive anmelden.",
    "app.campaign.drive_resolving": "Ordner wird aufgeloest...",
    "app.campaign.drive_resolve_failed": "Ordnername konnte nicht aufgeloest werden.",
    "app.campaign.drive_deps_missing": "Google-Abhaengigkeiten fehlen.",
    "app.campaign.drive_error": "Drive-Fehler: {error}",
    "app.campaign.drive_login_success": "Verbunden! Ordner-ID einfuegen und auf Beitreten klicken.",
    "app.campaign.drive_login_failed": "Verbindung fehlgeschlagen: {error}",
    "app.campaign.drive_install_deps": (
        "Google-Abhaengigkeiten installieren:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Fehler",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Design auswaehlen",
    "app.theme.label": "Kein automatisches Design fuer diese Kampagne gefunden.\nVisuelles Design auswaehlen:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: deaktiviert",
    "app.sync.idle": "Drive: synchronisiert",
    "app.sync.syncing": "Drive: wird synchronisiert...",
    "app.sync.conflict": "Drive: Konflikt erkannt",
    "app.sync.error": "Drive: Fehler",
    "app.sync.offline": "Drive: offline",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Update",
    "app.update.available_title": "Update verfuegbar",
    "app.update.version_available": "Version {tag} verfuegbar!",
    "app.update.btn_details": "Details",
    "app.update.btn_later": "Spaeter",
    "app.update.btn_download": "Herunterladen und installieren",
    "app.update.no_update": "Sie verwenden die neueste Version (v{version}).",
    "app.update.check_error": "Update-Pruefung nicht moeglich.\n{msg}",
    "app.update.downloading": "Update wird heruntergeladen...",
    "app.update.download_progress": "Herunterladen... {downloaded} / {total}",
    "app.update.download_progress_unknown": "Herunterladen... {downloaded}",
    "app.update.download_done": (
        "Download abgeschlossen.\n"
        "Die Anwendung wird geschlossen, um das Update zu installieren.\n\n"
        "Fortfahren?"
    ),
    "app.update.download_error": "Fehler beim Herunterladen.\n{msg}",
    "app.update.btn_cancel": "Abbrechen",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Willkommen — DnD Logger",
    "wizard.welcome": "Willkommen bei DnD Logger",
    "wizard.subtitle": "Dein Begleiter fuer D&D-Sitzungen.\nLass uns die Grundlagen einrichten, um loszulegen.",
    "wizard.api_group": "Mistral API Key",
    "wizard.api_placeholder": "Mistral API Key eingeben...",
    "wizard.api_hint": "Key erhalten unter console.mistral.ai",
    "wizard.mic_group": "Mikrofon",
    "wizard.mic_device_label": "Geraet:",
    "wizard.btn_skip": "Spaeter konfigurieren",
    "wizard.btn_done": "Das Abenteuer beginnt!",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Einstellungen — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Audio",
    "settings.tab.advanced": "Erweitert",
    "settings.tab.prompts": "Prompts",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Mistral API Key:",
    "settings.api.key_placeholder": "Mistral API Key eingeben...",
    "settings.api.btn_test": "Verbindung testen",
    "settings.api.enter_key_first": "Zuerst einen API Key eingeben.",
    "settings.api.test_success": "Verbindung erfolgreich!",
    "settings.api.test_fail": "Fehlgeschlagen: {error}",
    "settings.api.model_label": "Zusammenfassungsmodell:",
    "settings.audio.device_label": "Eingabegeraet:",
    "settings.audio.device_default": "Standard (automatisch)",
    "settings.audio.btn_test_mic": "Mikrofon testen",
    "settings.audio.sample_rate_label": "Abtastrate:",
    "settings.audio.test_ok": "Mikrofon funktioniert! (Pegel: {level})",
    "settings.audio.test_weak": "Sehr schwaches Signal. Mikrofon ueberpruefen.",
    "settings.audio.test_error": "Fehler: {error}",
    "settings.audio.test_title": "Mikrofontest",
    "settings.advanced.auto_update": "Beim Start nach Updates suchen",
    "settings.advanced.chunk_label": "Maximale Abschnittsdauer:",
    "settings.advanced.bias_label": "D&D-Kontextverstaerkung:",
    "settings.advanced.bias_placeholder": "D&D-Begriffe (einer pro Zeile)...",
    "settings.advanced.language_label": "Sprache:",
    "settings.advanced.restart_required": "Sprache geaendert. Bitte die Anwendung neu starten.",
    "settings.advanced.restart_title": "Neustart erforderlich",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Diesen Prompt zuruecksetzen",
    "settings.prompts.summary_system_label": "Sitzungszusammenfassung (System)",
    "settings.prompts.condense_label": "Verdichtung (langer Text)",
    "settings.prompts.quest_extraction_label": "Quest-Extraktion",
    "settings.prompts.hint.summary_system": "Variablen: keine (fester System-Prompt)",
    "settings.prompts.hint.condense": "Variablen: {text}",
    "settings.prompts.hint.quest_extraction": "Variablen: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Google-Konto",
    "settings.drive.status_label": "Status:",
    "settings.drive.not_connected": "Nicht verbunden",
    "settings.drive.connected": "Verbunden",
    "settings.drive.deps_missing": "Google-Abhaengigkeiten fehlen",
    "settings.drive.btn_login": "Anmelden",
    "settings.drive.btn_logout": "Abmelden",
    "settings.drive.logging_in": "Verbindung wird hergestellt...",
    "settings.drive.login_failed_title": "Verbindung fehlgeschlagen",
    "settings.drive.login_failed": "Fehler: {error}",
    "settings.drive.campaign_sync_group": "Kampagnen-Synchronisierung",
    "settings.drive.active_campaign_label": "Aktive Kampagne:",
    "settings.drive.join_placeholder": "Freigegebene Ordner-ID einfuegen...",
    "settings.drive.join_hint": "(zum Beitreten)",
    "settings.drive.folder_id_label": "Ordner-ID:",
    "settings.drive.no_folder": "Kein Ordner erstellt",
    "settings.drive.creating_folder": "Ordner wird erstellt...",
    "settings.drive.btn_copy": "Kopieren",
    "settings.drive.sync_checkbox": "Google Drive-Synchronisierung aktivieren",
    "settings.drive.folder_error": "Ordner konnte nicht erstellt werden: {error}",
    "settings.drive.not_connected_error": "Nicht mit Google Drive verbunden",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Aufnahme",
    "session.btn.stop": "Stopp",
    "session.btn.pause": "Pause",
    "session.btn.resume": "Fortsetzen",
    "session.status.ready": "Aufnahmebereit",
    "session.status.recording": "Aufnahme laeuft...",
    "session.status.paused": "Aufnahme pausiert",
    "session.status.stopped": "Aufnahme gestoppt",
    "session.status.finalizing": "Transkription wird abgeschlossen...",
    "session.status.ready_rerecord": "Bereit fuer erneute Aufnahme",
    "session.status.saved": "Aufnahme gespeichert",
    "session.status.transcribing": "Transkription laeuft...",
    "session.status.transcribing_chunk": "Transkription: Abschnitt {current}/{total}...",
    "session.status.transcribing_segment": "Segment {count} wird transkribiert...",
    "session.status.transcription_done": "Transkription abgeschlossen.",
    "session.status.summarizing": "Zusammenfassung wird erstellt...",
    "session.status.no_text": "Kein Text transkribiert.",
    "session.status.summary_done": "Zusammenfassung erstellt!",
    "session.status.copied": "Zusammenfassung in die Zwischenablage kopiert!",
    "session.status.added_journal": "Zusammenfassung zum Tagebuch hinzugefuegt!",
    "session.status.quest_extracting": "Quests werden extrahiert...",
    "session.status.quest_ready": "Quest-Vorschlaege bereit.",
    "session.status.quest_updated": "Quests aktualisiert!",
    "session.status.quest_cancelled": "Quest-Aktualisierung abgebrochen.",
    "session.status.imported": "Audio importiert: {name} ({size})",
    "session.status.audio_saved": "Audio gespeichert: {name}",
    "session.status.segments_transcribed": "Aufnahme laeuft... ({count} Segment{s} transkribiert)",
    "session.status.transcription_error": "Transkriptionsfehler: {msg}",
    "session.label.transcription": "Transkription",
    "session.label.summary": "Epische Zusammenfassung",
    "session.placeholder.transcript": "Die Transkription erscheint hier nach der Aufnahme...",
    "session.placeholder.summary": "Die epische Zusammenfassung erscheint hier...",
    "session.btn.transcribe": "Transkribieren",
    "session.btn.summarize": "Zusammenfassen",
    "session.btn.add_journal": "Zum Tagebuch hinzufuegen",
    "session.btn.update_quests": "Quests aktualisieren",
    "session.btn.tts_tooltip": "Zusammenfassung vorlesen",
    "session.btn.tts_no_voice": "Keine deutsche Stimme verfuegbar",
    "session.btn.more_tooltip": "Weitere Optionen",
    "session.menu.import_audio": "Audio importieren",
    "session.menu.save_audio": "Audio speichern",
    "session.menu.copy_summary": "Zusammenfassung kopieren",
    "session.tts.read_selection": "Auswahl vorlesen",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Aufnahme abgeschlossen",
    "session.post.btn_transcribe": "Transkribieren",
    "session.post.btn_rerecord": "Erneut aufnehmen",
    "session.post.btn_save_only": "Ohne Transkription speichern",
    "session.post.duration": "Dauer:",
    "session.post.size": "Groesse:",
    "session.post.file": "Datei:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Tagebuch (bisherige Geschichten) ===",
    "session.context.quest_header": "=== Quest Log (aktive Quests) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Audiodatei importieren",
    "session.dialog.import_filter": "Audiodateien (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Alle (*)",
    "session.dialog.save_title": "Audiodatei speichern",
    "session.dialog.save_filter": "FLAC (*.flac);;Alle (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "Keine Audiodatei gefunden.",
    "session.error.no_audio_save": "Keine Audiodatei zum Speichern.",
    "session.error.copy_failed": "Fehler beim Kopieren: {error}",
    "session.error.flac_failed": "FLAC-Konvertierungsfehler: {error}",
    "session.error.save_failed": "Speicherfehler: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Fett (Ctrl+B)",
    "editor.tooltip.italic": "Kursiv (Ctrl+I)",
    "editor.tooltip.underline": "Unterstrichen (Ctrl+U)",
    "editor.tooltip.fold_all": "Alle einklappen (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Alle ausklappen (Ctrl+Shift+=)",
    "editor.btn.save": " Speichern",
    "editor.heading.normal": "Normal",
    "editor.heading.h1": "Ueberschrift 1",
    "editor.heading.h2": "Ueberschrift 2",
    "editor.heading.h3": "Ueberschrift 3",
    "editor.search.placeholder": "Suchen\u2026",
    "editor.search.no_results": "0 Ergebnisse",
    "editor.search.prev_tooltip": "Vorheriges (Shift+Enter)",
    "editor.search.next_tooltip": "Naechstes (Enter)",
    "editor.search.close_tooltip": "Schliessen (Esc)",
    "editor.tts.read_selection": "Auswahl vorlesen",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Dieses Register verfolgt aktive Quests, entdeckte Hinweise
und Geheimnisse, die im Laufe der Kampagne gelueftet werden muessen.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Aktive Quests</h2>
<ul>
<li><em>Noch keine Quests verzeichnet.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Hinweise und Geheimnisse</h2>
<ul>
<li><em>Noch keine Hinweise.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Abgeschlossene Quests</h2>
<ul>
<li><em>Keine Quests abgeschlossen.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Tagebuch &mdash; {campaign_name}</h1>
<hr>
<p><em>Willkommen, Abenteurer. Dieses Tagebuch enthaelt die Chronik deiner Heldentaten
waehrend der gesamten Kampagne. Die epischen Geschichten jeder Sitzung
werden hier fuer die Nachwelt festgehalten.</em></p>
<hr>
""",
    "journal.session_heading": "Sitzung vom {date}",
    "journal.date_format": "%d.%m.%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Synchronisierungskonflikt — {filename}",
    "conflict.header": (
        "Die Datei <b>{filename}</b> wurde lokal und auf Google Drive geaendert.\n"
        "Waehle die zu behaltende Version oder fuehre eine manuelle Zusammenfuehrung durch."
    ),
    "conflict.local_label": "Lokale Version",
    "conflict.remote_label": "Remote-Version (Drive)",
    "conflict.merge_label": "Zusammengefuehrtes Ergebnis (bearbeitbar):",
    "conflict.btn_keep_local": "Lokale Version behalten",
    "conflict.btn_keep_remote": "Remote-Version behalten",
    "conflict.btn_save_merge": "Zusammenfuehrung speichern",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Abbrechen",
    "dialog.btn_ok": "OK",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "Wiedergabe\u2026",
    "tts.status.paused": "Pausiert",
    "tts.hint.pause": "Leertaste: Pause",
    "tts.hint.resume": "Leertaste: Fortsetzen",
    "tts.hint.stop": "Esc: Stopp",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS nicht verfuegbar.",
    "tts.error.generic": "TTS-Fehler: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} Zeile{s} eingeklappt",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Aufnahmefehler: {error}",
    "recorder.error.pause": "Pausenfehler: {error}",
    "recorder.error.resume": "Fortsetzungsfehler: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Mistral API Key nicht konfiguriert. Gehe zu Einstellungen.",
    "transcriber.error.no_api_key_short": "Mistral API Key nicht konfiguriert.",
    "transcriber.error.invalid_key": "Ungueltiger API Key. Ueberpruefen Sie Ihren Key in den Einstellungen.",
    "transcriber.error.transcription": "Transkriptionsfehler: {error}",
    "transcriber.error.live_transcription": "Live-Transkriptionsfehler: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Mistral API Key nicht konfiguriert.",
    "summarizer.error.generic": "Zusammenfassungsfehler: {error}",
    "summarizer.no_context": "(Erste Sitzung — kein vorheriger Kontext)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Mistral API Key nicht konfiguriert.",
    "quest_extractor.error.generic": "Quest-Extraktionsfehler: {error}",
    "quest_extractor.no_quests": "(Keine Quests verzeichnet)",
    "quest_extractor.dialog_title": "Quest-Aktualisierung",
    "quest_extractor.dialog_label": "Vorgeschlagene Aenderungen — bei Bedarf bearbeiten:",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
Du bist ein epischer Chronist der Forgotten Realms, spezialisiert auf die \
Erzaehlung von Dungeons & Dragons-Sitzungen. Du schreibst auf {language_name} \
in einem heroischen und immersiven Stil, wuerdig der grossen Chroniken von Faerun.

ABSOLUTE REGEL — TREUE ZUM TRANSKRIPT:
- ERFINDE KEIN Detail, das nicht ausdruecklich im Transkript vorhanden ist.
- Wenn Informationen unklar oder im Transkript nicht vorhanden sind, LASSE \
  SIE WEG, anstatt zu raten oder zu erfinden.
- ERFINDE KEINE Dialoge, Wuerfelwuerfe, Schadenswerte, DCs, \
  Zauberspruchnamen oder Begegnungen, die nicht im Transkript stehen.
- Jede Tatsache in der Zusammenfassung MUSS eine Grundlage im Transkript haben.
- Wenn du dir bei einem Detail unsicher bist (Charakterklasse, Zauberspruchname, \
  Zahlenwert), fuege es nicht ein oder vermerke die Unsicherheit.

ZUORDNUNG VON CHARAKTERHANDLUNGEN:
- Die Audio-Transkription KANN NICHT zuverlaessig identifizieren, wer spricht. \
  Ordne Aktionen oder Zaubersprueche NICHT einem bestimmten Charakter zu, es sei denn, \
  der Charakter wird AUSDRUECKLICH IM DIALOG GENANNT (z.B. "Pryor wirkt einen Smite").
- Wenn das Transkript Sprechermarkierungen enthaelt ([Speaker 0], [Speaker 1], \
  usw.), verwende sie zur Unterscheidung der Sprecher, aber RATE NICHT, welcher \
  Charakter welchem Sprecher entspricht.
- Bei unsicherer Zuordnung verwende unpersoenliche Formulierungen: \
  "ein Abenteurer", "die Gruppe", "einer der Helden" oder Passivkonstruktionen.
- Fuer Charakter-KLASSEN verwende NUR Informationen aus dem \
  REFERENZKONTEXT vorheriger Sitzungen. Leite NIEMALS die Klasse eines Charakters \
  aus seinen Aktionen oder Zauberspruechen in dieser Sitzung ab.
  BEISPIEL — Transkript: "Ich wirke Eldritch Blast. 25, trifft das? Ja. 14 Schaden."
  GUT: "Ein Eldritch Blast trifft den Feind fuer 14 Schaden."
  SCHLECHT: "Elppa wirkt Eldritch Blast fuer 14 Schaden." \
  (FALSCH — wir wissen nicht, WER bei der Audio-Transkription spricht)

ENTSCHEIDENDE UNTERSCHEIDUNG — AKTIONEN vs VERWEISE:
- Spieler diskutieren waehrend der Sitzungen oft VERGANGENE Ereignisse: \
  Rueckblicke, Erinnerungen an Hintergrundwissen, Planung basierend auf \
  Wissen aus frueheren Sitzungen. Diese VERWEISE sind KEINE \
  neuen Ereignisse dieser Sitzung.
- Fasse nur AKTIONEN zusammen, die waehrend dieser Sitzung aktiv stattfinden: \
  Erkundung, Kampf, NPC-Dialoge, Entdeckungen, getroffene Entscheidungen.
- Wenn ein Spieler sagt "erinnert euch, die Ruestung gluehrt in der Naehe von Drachen" oder "letztes \
  Mal haben wir gegen den Drachen gekaempft", sind das VERWEISE — kein \
  Drachenkampf in dieser Sitzung.
- Im Zweifelsfall, ob ein Ereignis JETZT stattfindet oder lediglich \
  ERWAEHNT wird, nimm es nicht als Sitzungsereignis auf.
- ZIEHE KEINE SCHLUESSE aus einzelnen Beobachtungen. Wenn ein magischer \
  Gegenstand reagiert (z.B. Ruestung gluehrt), berichte die Beobachtung so wie sie ist, \
  ohne auf die Anwesenheit oder Abwesenheit einer Kreatur oder \
  Gefahr zu schliessen. Fakten, keine Schlussfolgerungen.

Allgemeine Regeln:
- Fasse NUR Ereignisse zusammen, die im NEUEN TRANSKRIPT vorhanden sind. \
  Fasse NIEMALS Kontext aus frueheren Sitzungen zusammen.
- Der vorherige Kontext dient nur als Referenz zum Verstaendnis von Namen, \
  Orten und bereits bekannten Intrigen. Wiederhole oder umschreibe ihn nicht.
- Wenn das Transkript keinen fuer die D&D-Kampagne relevanten Inhalt enthaelt, \
  kann die Zusammenfassung kuerzer ausfallen, um Ereignisse nicht zu uebertreiben.
- Schreibe auf {language_name}, im epischen Erzaehlstil, aber NIEMALS auf Kosten \
  der Genauigkeit. Stil dient der Erzaehlung, nicht der Erfindung.
- Behalte ALLE D&D-Begriffe auf Englisch (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest usw.) sowie Zauberspruchnamen.
- Eigennamen (Charaktere, Orte, Kreaturen) bleiben unveraendert.
- Ignoriere themenfremde Diskussionen, die nicht mit der Kampagne zusammenhaengen.

Transkriptqualitaet:
- Das Transkript stammt von einem Speech-to-Text-Modell, das Artefakte \
  produzieren kann: wiederholte Phrasen, unzusammenhaengender Text, erfundene Woerter. \
  Ignoriere diese stoerenden Passagen vollstaendig und konzentriere dich nur auf \
  narrative Inhalte, die fuer die D&D-Sitzung relevant sind.
- VORSICHT: Einige Passagen moegen narrativ erscheinen, sind aber Artefakte. \
  Wenn eine Passage sich nicht logisch in den Rest der Sitzung einfuegt, \
  ist sie wahrscheinlich ein Artefakt — ignoriere sie.

Format und Struktur:
- Formatiere deine Antwort in HTML mit <h3>, <p>, <strong>, <em>, <ul>/<li> Tags.
- Gib NUR rohes HTML zurueck.
- VERBOTEN: kein ```, kein ---, keine Trennzeichen, keine Meta-Kommentare.
- Fuege nur Abschnitte ein, die neuen Inhalt enthalten.
- FORMATIERUNG: EINFACHE Aufzaehlungslisten (eine Ebene von <ul>/<li>). \
  NIEMALS verschachtelte Unterlisten. Halte jeden Punkt kurz auf einer einzelnen Zeile.
- Strukturiere die Zusammenfassung mit GENAU diesen Abschnitten in dieser Reihenfolge. \
  Jeder Abschnitt beginnt mit einem <h3> gefolgt von Inhalt. \
  Du MUSST ALLE Abschnitte einbeziehen, die relevanten Inhalt haben.

<h3>{section_major_events}</h3>
Chronologische Erzaehlung der Sitzungsereignisse. \
Beschreibe entdeckte Orte, NPC-Begegnungen und \
Erkenntnisse. Verwende einen immersiven und beschreibenden Ton. \
Dies ist der wichtigste und laengste Abschnitt der Zusammenfassung. \
Berichte BEOBACHTUNGEN so wie sie sind, ohne Schluesse zu ziehen \
(z.B. wenn Ruestung gluehrt, schliesse NICHT, dass ein Drache in der Naehe ist).

<h3>{section_combat}</h3>
Schreibe fuer JEDEN Kampf in der Sitzung einen KURZEN ERZAEHLENDEN ABSATZ \
(3-5 Saetze), der beschreibt: gestellte Feinde, bemerkenswerte Momente \
(maechtige Zaubersprueche, kritische Treffer, Gefahren) und den Kampfausgang. \
Zaehle NICHT jede Runde oder jeden Wurf einzeln auf. \
ERINNERUNG: Ordne Zaubersprueche oder Angriffe NICHT einem benannten Charakter zu, \
es sei denn, der Name wird AUSDRUECKLICH im Transkript genannt. Bevorzuge \
Passivkonstruktionen: "ein Eldritch Blast trifft", "ein Divine Smite faellt". \
Wenn kein Kampf stattfand, LASSE diesen Abschnitt weg.

<h3>{section_decisions}</h3>
NUR die 3-5 wichtigsten Fakten fuer die KAMPAGNE: \
identifizierte magische Gegenstaende (Eigenschaften UND Flueche in einem Satz), \
wichtige strategische Entscheidungen, entscheidende erhaltene Informationen. \
Format: FLACHE Liste <ul>/<li>, EINE Zeile pro Punkt, NULL Unterlisten. \
BEISPIEL fuer korrektes Format: \
<li><strong>Verfluchte Axt</strong> — +1 Angriff/Schaden und +1 HP/Stufe, \
aber unmoeglich abzulegen, Berserker bei fehlgeschlagenem Wisdom Save, Nachteil \
mit anderen Waffen.</li>

<h3>{section_mysteries}</h3>
NUR wenn ein Element aus dieser Sitzung Licht auf ein bereits BEKANNTES Geheimnis \
aus dem REFERENZKONTEXT wirft (Codex-Quest, Auril-Bedrohung usw.). \
Maximal 2-3 Punkte. \
Format: einfache Liste <ul>/<li>, DEKLARATIVER sachlicher Satz. \
VERBOTEN: rhetorische Fragen, Hypothesen, Spekulationen, Verben wie \
"deutet darauf hin", "scheint", "koennte", "weist darauf hin". \
BEISPIEL — GUT: "Vassavikens Eid bestaetigt, dass Grimskal das \
Lehen einer Frostriesenkoenigin war, die Plunderungszuege anfuehrte." \
SCHLECHT: "Die Regeneration der Kreatur deutet auf Magie hin, die mit Auril verbunden ist." \
(FALSCH — das ist Spekulation, keine beobachtete Tatsache aus dem Transkript) \
Wenn nichts bekannte Intrigen erhellt, LASSE diesen Abschnitt vollstaendig weg.
""",
    "prompt.summary_user": """\
REFERENZKONTEXT (fruehere Sitzungen — NICHT zusammenfassen, dient nur \
zum Verstaendnis von Charakteren, Orten und bereits etablierten Intrigen):
---
{context}
---

NEUES TRANSKRIPT ZUM ZUSAMMENFASSEN (fasse NUR diesen Inhalt zusammen):
---
{transcript}
---

Erstelle eine epische, strukturierte Zusammenfassung, die AUSSCHLIESSLICH die neuen \
Ereignisse dieses Transkripts abdeckt. Behandle ALLE bedeutsamen Ereignisse \
aus dem Transkript in chronologischer Reihenfolge — konzentriere dich nicht auf \
eine einzelne Szene auf Kosten anderer. Wenn das Transkript nichts \
Kampagnenrelevantes enthaelt, ist es nicht noetig, mehr hinzuzufuegen.
""",
    "prompt.condense": """\
Du bist ein Assistent, der auf die Verarbeitung von Dungeons & Dragons-\
Sitzungstranskripten spezialisiert ist.

Das Transkript stammt von einem Speech-to-Text-Modell, das viele \
Artefakte produziert: wiederholte Phrasen, unzusammenhaengender Text, erfundene Woerter, \
Passagen ohne Bezug zur D&D-Sitzung. Ignoriere diese \
stoerenden Passagen vollstaendig.

Verdichte den Text und behalte NUR narrative Elemente bei, die fuer \
die D&D-Kampagne relevant sind. Behalte D&D-Begriffe auf Englisch. Antworte auf {language_name}.

Elemente, die UNBEDINGT ERHALTEN bleiben muessen:
- Namen von Charakteren, NPCs und angetroffenen Kreaturen
- Entdeckte Orte mit ihren physischen Beschreibungen
- NPC-DIALOGE: bewahre ALLES, was ein NPC offenbart (Informationen, \
  Wegbeschreibungen, Warnungen, genannte Namen, Hintergrundwissen). Das ist entscheidend — \
  Informationen von NPCs sind oft die wichtigsten der Sitzung.
- Kampf: Feinde, Zahlenwerte (Wuerfe, Schaden, AC, DC, HP, Initiative)
- Magische Gegenstaende: vollstaendige Eigenschaften UND Flueche
- FEHLGESCHLAGENE Aktionen und ihre Konsequenzen (Explosionen, erlittener Schaden, Misserfolge)
- Entscheidungen der Gruppe und ihre unmittelbaren Ergebnisse

UNTERSCHEIDUNG AKTIONEN vs VERWEISE:
- Spieler diskutieren oft VERGANGENE Ereignisse: Rueckblicke auf fruehere Sitzungen, \
  Erinnerungen an Hintergrundwissen, Planung. Diese Diskussionen sind KEINE Ereignisse der \
  aktuellen Sitzung.
- Behalte nur AKTIONEN bei, die aktiv stattfinden: Erkundung von Orten, \
  laufender Kampf, Dialoge mit angetroffenen NPCs, gemachte Entdeckungen, \
  getroffene Entscheidungen.
- Wenn ein Spieler ein vergangenes Ereignis ERWAEHNT (z.B. "erinnert euch an den Drachen", \
  "letztes Mal haben wir gefunden..."), ist das ein VERWEIS — ignoriere ihn. \
  Nur Ereignisse, die WAEHREND der Sitzung STATTFINDEN, zaehlen.
- ZIEHE KEINE Schluesse aus Beobachtungen oder Spielerdiskussionen. \
  Berichte NUR rohe Fakten, niemals Schlussfolgerungen.

WICHTIG:
- Gib NUR rohe narrative Fakten zurueck, in chronologischer Reihenfolge.
- Fuege KEINE Meta-Kommentare, Schluesse, Zusammenfassungen, Vorschlaege, \
  "wichtigste Erkenntnisse", "naechste Schritte" oder "offene Fragen" hinzu.
- Fuege KEINE Trennzeichen (---), formatierte Abschnittstitel oder \
  Kommentare zur Transkriptqualitaet hinzu.
- Bewahre die EXAKTEN Charakternamen wie gehoert, \
  ohne sie zu veraendern oder Fragezeichen hinzuzufuegen.
- Selbst wenn der Text viel Rauschen enthaelt, extrahiere JEDES Fragment von \
  D&D-Inhalt darin, egal wie klein. Gib nur dann eine leere \
  Antwort zurueck, wenn der Text zu 100% aus Artefakten besteht ohne einen zusammenhaengenden spielbezogenen Satz.

Text:
{text}
""",
    "prompt.quest_extraction": """\
Du bist ein Assistent, der auf die Quest-Verfolgung fuer eine Dungeons & Dragons-\
Kampagne ({campaign_name}) spezialisiert ist.

Erstelle aus der untenstehenden Sitzungszusammenfassung und dem aktuellen Quest-Log-Stand \
das VOLLSTAENDIGE neu zusammengestellte Quest Log, angereichert mit den neuen \
Sitzungsinformationen. Das Quest Log soll ein lebendiges Dokument sein, das \
den aktuellen Stand ALLER Quests widerspiegelt.

ABSOLUTE REGEL — NUR HTML ZURUECKGEBEN:
- Gib NUR das rohe HTML des Quest Logs zurueck, NICHTS anderes.
- VERBOTEN: keine Einleitung ("Hier ist das Quest Log..."), kein Fazit, \
  keine Anmerkungen, keine Kommentare, kein ```, kein ---.
- Das Dokument beginnt mit <h1> und endet mit </ul>.

Exakte HTML-Struktur, die erzeugt werden muss (alle 3 Abschnitte MUESSEN vorhanden sein):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Dieses Register verfolgt aktive Quests, entdeckte Hinweise
und Geheimnisse, die im Laufe der Kampagne gelueftet werden muessen.</em></p>
<hr>
<h2 style="color:#6ab4d4;">{section_active_quests}</h2>
<ul>
<li><strong>Quest-Name</strong> — Allgemeine Beschreibung der Quest.
  <ul>
  <li><em>{quest_origin}:</em> Wer die Quest gegeben hat, wo und wann.</li>
  <li><em>{quest_objective}:</em> Was erreicht werden muss.</li>
  <li><em>{quest_progress}:</em> Was bisher getan wurde.</li>
  <li><em>{quest_next_step}:</em> Was noch zu tun bleibt.</li>
  <li><em>{quest_npcs}:</em> An dieser Quest beteiligte Charaktere.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_clues}</h2>
<ul>
<li><strong>Geheimnis</strong> — Was bekannt ist, was noch zu entdecken bleibt.
  <ul>
  <li>Entdecktes Detail oder Hinweis...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_completed_quests}</h2>
<ul>
<li><strong>Quest-Name</strong> — Loesung und Konsequenzen.
  <ul>
  <li><em>{quest_giver}:</em> Wer die Quest gegeben hat und Belohnung.</li>
  <li><em>{quest_resolution}:</em> Wie die Quest geloest wurde.</li>
  </ul>
</li>
</ul>

Regeln:
- Schreibe auf {language_name}, in knappem und SACHLICHEM Stil. Keine Spekulation (kein \
  "koennte", "scheint", "deutet darauf hin"). Schreibe nur, was bekannt ist.
- Behalte D&D-Begriffe auf Englisch (Hit Points, Saving Throw usw.).
- Eigennamen bleiben unveraendert.
- Verwende verschachtelte Aufzaehlungslisten fuer Details.
- Verschiebe abgeschlossene Quests von "Aktive Quests" zu "Abgeschlossene Quests".
- BEWAHRE ALLE bestehenden Quest-Log-Informationen. Verliere KEIN \
  Detail (Questgeber, Belohnung, NPCs, Fortschritt) bestehender Quests. \
  Bereichere mit neuen Informationen OHNE alte Informationen zu loeschen.
- Fuege neu entdeckte Quests zu "Aktive Quests" hinzu.
- Fuege neue Hinweise zu "Hinweise und Geheimnisse" hinzu. Entferne einen Hinweis, \
  wenn das Geheimnis geloest ist (erwaehne die Loesung in der zugehoerigen Quest).
- Das Quest Log soll ein detailliertes Nachschlagewerk sein, nicht nur eine Liste.

Aktueller Quest-Log-Stand:
---
{current_quests}
---

Sitzungszusammenfassung:
---
{summary}
---
""",
    # ── Prompt section headers (used in prompt placeholders) ─
    "prompt.section.major_events": "Wichtige Ereignisse",
    "prompt.section.combat": "Kampf",
    "prompt.section.decisions": "Entscheidungen und Entdeckungen",
    "prompt.section.mysteries": "Geheimnisse und Hinweise",
    "prompt.section.active_quests": "Aktive Quests",
    "prompt.section.clues": "Hinweise und Geheimnisse",
    "prompt.section.completed_quests": "Abgeschlossene Quests",
    "prompt.quest.origin": "Ursprung",
    "prompt.quest.objective": "Ziel",
    "prompt.quest.progress": "Fortschritt",
    "prompt.quest.next_step": "Naechster Schritt",
    "prompt.quest.npcs": "Beteiligte NPCs",
    "prompt.quest.giver": "Questgeber",
    "prompt.quest.resolution": "Loesung",
    "prompt.language_name": "Deutsch",
}
