"""Nederlandse vertalingen — alle UI-teksten en AI-prompts."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "B",
    "units.kilobytes": "KB",
    "units.megabytes": "MB",
    "units.gigabytes": "GB",
    "units.terabytes": "TB",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "Bestand",
    "app.menu.settings": "Instellingen...",
    "app.menu.check_updates": "Controleren op updates...",
    "app.menu.save": "Opslaan",
    "app.menu.quit": "Afsluiten",
    "app.menu.campaign": "Campagne",
    "app.menu.new_campaign": "Nieuwe campagne...",
    "app.menu.delete_campaign": "Campagne verwijderen...",
    "app.menu.restore_campaign": "Campagne herstellen...",
    "app.menu.theme": "Thema",
    "app.menu.session": "Sessie",
    "app.menu.record_stop": "Opnemen / Stoppen",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Dagboek",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Sessie",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "Geen campagnes gevonden.",
    "app.campaign.name_label": "Campagnenaam:",
    "app.campaign.name_placeholder": "Bijv.: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Aanmaken",
    "app.campaign.delete_title": "Een campagne verwijderen",
    "app.campaign.delete_label": "Kies de campagne om te verwijderen:",
    "app.campaign.delete_confirm_title": "Verwijdering bevestigen",
    "app.campaign.delete_confirm": 'Campagne "{name}" verwijderen?\nBestanden worden verplaatst naar campaigns/_trash/.',
    "app.campaign.restore_title": "Een campagne herstellen",
    "app.campaign.restore_label": "Kies de campagne om te herstellen:",
    "app.campaign.restore_none": "Geen gearchiveerde campagnes.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Status:",
    "app.campaign.drive_not_connected": "Niet verbonden",
    "app.campaign.drive_connected": "Verbonden",
    "app.campaign.drive_btn_login": "Inloggen",
    "app.campaign.drive_logging_in": "Verbinden...",
    "app.campaign.drive_folder_id_label": "Map-ID:",
    "app.campaign.drive_folder_placeholder": "Plak het gedeelde map-ID...",
    "app.campaign.drive_btn_join": "Deelnemen",
    "app.campaign.drive_join_hint": "(om deel te nemen)",
    "app.campaign.name_empty": "Naam mag niet leeg zijn.",
    "app.campaign.name_exists": 'De campagne "{name}" bestaat al.',
    "app.campaign.drive_paste_id": "Plak het gedeelde map-ID.",
    "app.campaign.drive_login_first": "Log eerst in bij Google Drive.",
    "app.campaign.drive_resolving": "Map oplossen...",
    "app.campaign.drive_resolve_failed": "Kan mapnaam niet oplossen.",
    "app.campaign.drive_deps_missing": "Google-afhankelijkheden ontbreken.",
    "app.campaign.drive_error": "Drive-fout: {error}",
    "app.campaign.drive_login_success": "Verbonden! Plak het map-ID en klik op Deelnemen.",
    "app.campaign.drive_login_failed": "Verbinding mislukt: {error}",
    "app.campaign.drive_install_deps": (
        "Installeer Google-afhankelijkheden:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Fout",
    # ── app.py — theme keyword matching (comma-separated) ──
    "app.theme.kw.icewind_dale": "ijswind,vorst",
    "app.theme.kw.curse_of_strahd": "vloek",
    "app.theme.kw.descent_into_avernus": "hel,afdaling",
    "app.theme.kw.tomb_of_annihilation": "graf,vernietiging",
    "app.theme.kw.storm_kings_thunder": "storm,reus,donder",
    "app.theme.kw.waterdeep_dragon_heist": "drakenroof",
    "app.theme.kw.out_of_the_abyss": "afgrond,onderwereld",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Kies een thema",
    "app.theme.label": "Geen automatisch thema gevonden voor deze campagne.\nKies een visueel thema:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: uitgeschakeld",
    "app.sync.idle": "Drive: gesynchroniseerd",
    "app.sync.syncing": "Drive: synchroniseren...",
    "app.sync.conflict": "Drive: conflict gedetecteerd",
    "app.sync.error": "Drive: fout",
    "app.sync.offline": "Drive: offline",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Update",
    "app.update.available_title": "Update beschikbaar",
    "app.update.version_available": "Versie {tag} beschikbaar!",
    "app.update.btn_details": "Details",
    "app.update.btn_later": "Later",
    "app.update.btn_download": "Downloaden en installeren",
    "app.update.no_update": "U gebruikt de nieuwste versie (v{version}).",
    "app.update.check_error": "Kan niet controleren op updates.\n{msg}",
    "app.update.downloading": "Update downloaden...",
    "app.update.download_progress": "Downloaden... {downloaded} / {total}",
    "app.update.download_progress_unknown": "Downloaden... {downloaded}",
    "app.update.download_done": (
        "Download voltooid.\n" "De applicatie wordt gesloten om de update te installeren.\n\n" "Doorgaan?"
    ),
    "app.update.download_error": "Fout bij downloaden.\n{msg}",
    "app.update.btn_cancel": "Annuleren",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Welkom — DnD Logger",
    "wizard.welcome": "Welkom bij DnD Logger",
    "wizard.subtitle": "Uw D&D-sessiepartner.\nLaten we de basis instellen om te beginnen.",
    "wizard.api_group": "Mistral API-sleutel",
    "wizard.api_placeholder": "Voer uw Mistral API-sleutel in...",
    "wizard.api_hint": "Verkrijg een sleutel op console.mistral.ai",
    "wizard.mic_group": "Microfoon",
    "wizard.mic_device_label": "Apparaat:",
    "wizard.btn_skip": "Later instellen",
    "wizard.btn_done": "Begin het avontuur!",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Instellingen — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Audio",
    "settings.tab.advanced": "Geavanceerd",
    "settings.tab.prompts": "Prompts",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Mistral API-sleutel:",
    "settings.api.key_placeholder": "Voer uw Mistral API-sleutel in...",
    "settings.api.btn_test": "Verbinding testen",
    "settings.api.enter_key_first": "Voer eerst een API-sleutel in.",
    "settings.api.test_success": "Verbinding geslaagd!",
    "settings.api.test_fail": "Mislukt: {error}",
    "settings.api.model_label": "Samenvattingsmodel:",
    "settings.audio.device_label": "Invoerapparaat:",
    "settings.audio.device_default": "Standaard (automatisch)",
    "settings.audio.btn_test_mic": "Microfoon testen",
    "settings.audio.sample_rate_label": "Samplefrequentie:",
    "settings.audio.test_ok": "Microfoon werkt! (niveau: {level})",
    "settings.audio.test_weak": "Zeer zwak signaal. Controleer uw microfoon.",
    "settings.audio.test_error": "Fout: {error}",
    "settings.audio.test_title": "Microfoontest",
    "settings.advanced.auto_update": "Bij opstarten controleren op updates",
    "settings.advanced.chunk_label": "Maximale fragmentduur:",
    "settings.advanced.bias_label": "D&D-contextbias:",
    "settings.advanced.bias_placeholder": "D&D-termen (één per regel)...",
    "settings.advanced.language_label": "Taal:",
    "settings.advanced.restart_required": "Taal gewijzigd. Start de applicatie opnieuw op.",
    "settings.advanced.restart_title": "Herstart vereist",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Deze prompt resetten",
    "settings.prompts.summary_system_label": "Sessiesamenvatting (systeem)",
    "settings.prompts.condense_label": "Condensatie (lange tekst)",
    "settings.prompts.quest_extraction_label": "Quest-extractie",
    "settings.prompts.hint.summary_system": "Variabelen: geen (vast systeemprompt)",
    "settings.prompts.hint.condense": "Variabelen: {text}",
    "settings.prompts.hint.quest_extraction": "Variabelen: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Google-account",
    "settings.drive.status_label": "Status:",
    "settings.drive.not_connected": "Niet verbonden",
    "settings.drive.connected": "Verbonden",
    "settings.drive.deps_missing": "Google-afhankelijkheden ontbreken",
    "settings.drive.btn_login": "Inloggen",
    "settings.drive.btn_logout": "Uitloggen",
    "settings.drive.logging_in": "Verbinden...",
    "settings.drive.login_failed_title": "Verbinding mislukt",
    "settings.drive.login_failed": "Fout: {error}",
    "settings.drive.campaign_sync_group": "Campagnesynchronisatie",
    "settings.drive.active_campaign_label": "Actieve campagne:",
    "settings.drive.join_placeholder": "Plak het gedeelde map-ID...",
    "settings.drive.join_hint": "(om deel te nemen)",
    "settings.drive.folder_id_label": "Map-ID:",
    "settings.drive.no_folder": "Geen map aangemaakt",
    "settings.drive.creating_folder": "Map aanmaken...",
    "settings.drive.btn_copy": "Kopiëren",
    "settings.drive.sync_checkbox": "Google Drive-synchronisatie inschakelen",
    "settings.drive.folder_error": "Kan map niet aanmaken: {error}",
    "settings.drive.not_connected_error": "Niet verbonden met Google Drive",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Opnemen",
    "session.btn.stop": "Stoppen",
    "session.btn.pause": "Pauzeren",
    "session.btn.resume": "Hervatten",
    "session.status.ready": "Klaar om op te nemen",
    "session.status.recording": "Opname bezig...",
    "session.status.paused": "Opname gepauzeerd",
    "session.status.stopped": "Opname gestopt",
    "session.status.finalizing": "Transcriptie afronden...",
    "session.status.ready_rerecord": "Klaar om opnieuw op te nemen",
    "session.status.saved": "Opname opgeslagen",
    "session.status.transcribing": "Transcriberen...",
    "session.status.transcribing_chunk": "Transcriptie: fragment {current}/{total}...",
    "session.status.transcribing_segment": "Segment {count} transcriberen...",
    "session.status.transcription_done": "Transcriptie voltooid.",
    "session.status.summarizing": "Samenvatting genereren...",
    "session.status.no_text": "Geen tekst getranscribeerd.",
    "session.status.summary_done": "Samenvatting gegenereerd!",
    "session.status.copied": "Samenvatting gekopieerd naar klembord!",
    "session.status.added_journal": "Samenvatting toegevoegd aan Dagboek!",
    "session.status.quest_extracting": "Quests extraheren...",
    "session.status.quest_ready": "Questvoorstellen gereed.",
    "session.status.quest_updated": "Quests bijgewerkt!",
    "session.status.quest_cancelled": "Quest-update geannuleerd.",
    "session.status.imported": "Audio geïmporteerd: {name} ({size})",
    "session.status.audio_saved": "Audio opgeslagen: {name}",
    "session.status.segments_transcribed": "Opname bezig... ({count} segment{s} getranscribeerd)",
    "session.status.transcription_error": "Transcriptiefout: {msg}",
    "session.label.transcription": "Transcriptie",
    "session.label.summary": "Epische Samenvatting",
    "session.placeholder.transcript": "De transcriptie verschijnt hier na de opname...",
    "session.placeholder.summary": "De epische samenvatting verschijnt hier...",
    "session.btn.transcribe": "Transcriberen",
    "session.btn.summarize": "Samenvatten",
    "session.btn.add_journal": "Toevoegen aan Dagboek",
    "session.btn.update_quests": "Quests bijwerken",
    "session.btn.tts_tooltip": "De samenvatting voorlezen",
    "session.btn.tts_no_voice": "Geen Nederlandse stem beschikbaar",
    "session.btn.more_tooltip": "Meer opties",
    "session.menu.import_audio": "Audio importeren",
    "session.menu.save_audio": "Audio opslaan",
    "session.menu.copy_summary": "Samenvatting kopiëren",
    "session.tts.read_selection": "Selectie voorlezen",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Opname voltooid",
    "session.post.btn_transcribe": "Transcriberen",
    "session.post.btn_rerecord": "Opnieuw opnemen",
    "session.post.btn_save_only": "Opslaan zonder transcriptie",
    "session.post.duration": "Duur:",
    "session.post.size": "Grootte:",
    "session.post.file": "Bestand:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Dagboek (voorgaande verhalen) ===",
    "session.context.quest_header": "=== Quest Log (actieve quests) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Audiobestand importeren",
    "session.dialog.import_filter": "Audiobestanden (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Alle (*)",
    "session.dialog.save_title": "Audiobestand opslaan",
    "session.dialog.save_filter": "FLAC (*.flac);;Alle (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "Geen audiobestand gevonden.",
    "session.error.no_audio_save": "Geen audiobestand om op te slaan.",
    "session.error.copy_failed": "Fout bij kopiëren: {error}",
    "session.error.flac_failed": "FLAC-conversiefout: {error}",
    "session.error.save_failed": "Fout bij opslaan: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Vet (Ctrl+B)",
    "editor.tooltip.italic": "Cursief (Ctrl+I)",
    "editor.tooltip.underline": "Onderstrepen (Ctrl+U)",
    "editor.tooltip.fold_all": "Alles invouwen (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Alles uitvouwen (Ctrl+Shift+=)",
    "editor.btn.save": " Opslaan",
    "editor.heading.normal": "Normaal",
    "editor.heading.h1": "Kop 1",
    "editor.heading.h2": "Kop 2",
    "editor.heading.h3": "Kop 3",
    "editor.search.placeholder": "Zoeken\u2026",
    "editor.search.no_results": "0 resultaten",
    "editor.search.prev_tooltip": "Vorige (Shift+Enter)",
    "editor.search.next_tooltip": "Volgende (Enter)",
    "editor.search.close_tooltip": "Sluiten (Esc)",
    "editor.tts.read_selection": "Selectie voorlezen",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Dit register houdt actieve quests, ontdekte aanwijzingen
en mysteries bij die gedurende de campagne ontrafeld moeten worden.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Actieve Quests</h2>
<ul>
<li><em>Nog geen quests geregistreerd.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Aanwijzingen en Mysteries</h2>
<ul>
<li><em>Nog geen aanwijzingen.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Voltooide Quests</h2>
<ul>
<li><em>Geen quests voltooid.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Dagboek &mdash; {campaign_name}</h1>
<hr>
<p><em>Welkom, avonturier. Dit dagboek bevat de kroniek van uw avonturen
gedurende de campagne. De epische verhalen van elke sessie
worden hier voor het nageslacht vastgelegd.</em></p>
<hr>
""",
    "journal.session_heading": "Sessie van {date}",
    "journal.date_format": "%d/%m/%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Synchronisatieconflict — {filename}",
    "conflict.header": (
        "Het bestand <b>{filename}</b> is lokaal en op Google Drive gewijzigd.\n"
        "Kies welke versie u wilt behouden of voeg handmatig samen."
    ),
    "conflict.local_label": "Lokale versie",
    "conflict.remote_label": "Externe versie (Drive)",
    "conflict.merge_label": "Samengevoegd resultaat (bewerkbaar):",
    "conflict.btn_keep_local": "Lokale versie behouden",
    "conflict.btn_keep_remote": "Externe versie behouden",
    "conflict.btn_save_merge": "Samenvoeging opslaan",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Annuleren",
    "dialog.btn_ok": "OK",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "Afspelen\u2026",
    "tts.status.paused": "Gepauzeerd",
    "tts.hint.pause": "Spatie: Pauzeren",
    "tts.hint.resume": "Spatie: Hervatten",
    "tts.hint.stop": "Esc: Stoppen",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS niet beschikbaar.",
    "tts.error.generic": "TTS-fout: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} regel{s} ingevouwen",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Opnamefout: {error}",
    "recorder.error.pause": "Pauzeerfout: {error}",
    "recorder.error.resume": "Hervatfout: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Mistral API-sleutel niet geconfigureerd. Ga naar Instellingen.",
    "transcriber.error.no_api_key_short": "Mistral API-sleutel niet geconfigureerd.",
    "transcriber.error.invalid_key": "Ongeldige API-sleutel. Controleer uw sleutel in Instellingen.",
    "transcriber.error.transcription": "Transcriptiefout: {error}",
    "transcriber.error.live_transcription": "Live transcriptiefout: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Mistral API-sleutel niet geconfigureerd.",
    "summarizer.error.generic": "Samenvattingsfout: {error}",
    "summarizer.no_context": "(Eerste sessie — geen voorgaande context)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Mistral API-sleutel niet geconfigureerd.",
    "quest_extractor.error.generic": "Quest-extractiefout: {error}",
    "quest_extractor.no_quests": "(Geen quests geregistreerd)",
    "quest_extractor.dialog_title": "Quest-update",
    "quest_extractor.dialog_label": "Voorgestelde wijzigingen — bewerk indien nodig:",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
Je bent een epische kroniekschrijver van de Forgotten Realms, gespecialiseerd \
in het vertellen van Dungeons & Dragons-sessies. Je schrijft in het {language_name} \
met een heroïsche en meeslepende stijl, waardig aan de grote kronieken van Faerun.

ABSOLUTE REGEL — TROUW AAN HET TRANSCRIPT:
- VERZIN GEEN enkel detail dat niet expliciet in het transcript voorkomt.
- Als informatie onduidelijk of afwezig is in het transcript, LAAT HET WEG \
  in plaats van te raden of te verzinnen.
- VERZIN GEEN dialogen, dobbelsteenworpen, schadewaarden, DCs, \
  spreuknamen of ontmoetingen die niet in het transcript staan.
- Elk feit in de samenvatting MOET een basis hebben in het transcript.
- Als je onzeker bent over een detail (karakterklasse, spreuknaam, \
  numerieke waarde), neem het dan niet op of vermeld de onzekerheid.

TOEWIJZING VAN ACTIES AAN PERSONAGES:
- Audiotranscriptie kan NIET betrouwbaar identificeren wie er spreekt. \
  WIJS GEEN acties of spreuken toe aan een specifiek personage tenzij het \
  personage EXPLICIET BIJ NAAM wordt genoemd in de dialoog \
  (bijv. "Pryor cast een Smite").
- Als het transcript sprekersmarkeringen bevat ([Speaker 0], [Speaker 1], \
  enz.), gebruik ze om sprekers te onderscheiden, maar RAAD NIET welk \
  personage bij welke spreker hoort.
- Bij onzekere toewijzing, gebruik onpersoonlijke formuleringen: \
  "een avonturier", "de groep", "een van de helden", of de lijdende vorm.
- Gebruik voor personage-KLASSEN ALLEEN informatie uit de \
  REFERENTIECONTEXT van voorgaande sessies. Leid NOOIT de klasse van \
  een personage af uit hun acties of spreuken in deze sessie.
  VOORBEELD — Transcript: "Ik cast Eldritch Blast. 25, raakt dat? Ja. 14 schade."
  GOED: "Een Eldritch Blast treft de vijand voor 14 schade."
  FOUT: "Elppa cast Eldritch Blast voor 14 schade." \
  (FOUT — we weten niet WIE er spreekt bij audiotranscriptie)

CRUCIAAL ONDERSCHEID — ACTIES vs VERWIJZINGEN:
- Spelers bespreken vaak EERDERE gebeurtenissen tijdens sessies: \
  samenvattingen, lore-herinneringen, planning op basis van kennis \
  uit voorgaande sessies. Deze VERWIJZINGEN zijn GEEN \
  nieuwe gebeurtenissen uit deze sessie.
- Vat alleen ACTIES samen die actief plaatsvinden tijdens deze sessie: \
  verkenning, gevecht, NPC-dialogen, ontdekkingen, genomen beslissingen.
- Als een speler zegt "weet je nog, het harnas gloeit bij draken" of "vorige \
  keer vochten we tegen de draak", zijn dit VERWIJZINGEN — geen \
  drakengevecht in deze sessie.
- Bij twijfel of een gebeurtenis NU plaatsvindt of slechts \
  GENOEMD wordt, neem het niet op als sessiegebeurtenis.
- TREK GEEN CONCLUSIES uit losse waarnemingen. Als een magisch \
  voorwerp reageert (bijv. gloeiend harnas), rapporteer de waarneming \
  zoals ze is zonder te concluderen over de aan- of afwezigheid van een \
  wezen of gevaar. Feiten, geen afleidingen.

Algemene regels:
- Vat ALLEEN gebeurtenissen samen die in het NIEUWE TRANSCRIPT staan. \
  Vat NOOIT context uit voorgaande sessies samen.
- Voorgaande context dient alleen als referentie om namen, \
  plaatsen en intrigues die al bekend zijn te begrijpen. Herhaal of \
  herformuleer deze niet.
- Als het transcript geen inhoud bevat die relevant is voor de D&D-campagne, \
  mag de samenvatting korter zijn om gebeurtenissen niet te overdrijven.
- Schrijf in het {language_name}, in een epische verhalende stijl, maar NOOIT \
  ten koste van de nauwkeurigheid. Stijl dient het verhaal, niet de verzinning.
- Houd ALLE D&D-termen in het Engels (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, enz.), evenals spreuknamen.
- Eigennamen (personages, plaatsen, wezens) blijven ongewijzigd.
- Negeer off-topic discussies die niet gerelateerd zijn aan de campagne.

Transcriptkwaliteit:
- Het transcript komt van een spraak-naar-tekst-model dat artefacten kan \
  produceren: herhaalde zinnen, incoherente tekst, verzonnen woorden. \
  Negeer deze parasitaire passages volledig en concentreer je alleen op \
  verhalende inhoud die relevant is voor de D&D-sessie.
- LET OP: sommige passages kunnen verhalend lijken maar zijn artefacten. \
  Als een passage niet logisch integreert met de rest van de sessie, \
  is het waarschijnlijk een artefact — negeer het.

Opmaak en structuur:
- Maak je antwoord op in HTML met <h3>, <p>, <strong>, <em>, <ul>/<li> tags.
- Geef ALLEEN ruwe HTML terug.
- VERBODEN: geen ```, geen ---, geen scheidingstekens, geen metacommentaar.
- Neem alleen secties op die nieuwe inhoud bevatten.
- OPMAAK: EENVOUDIGE opsommingslijsten (één niveau van <ul>/<li>). \
  Maak NOOIT geneste sublijsten. Houd elk punt beknopt op één regel.
- Structureer de samenvatting met EXACT deze secties in deze volgorde. \
  Elke sectie begint met een <h3> gevolgd door inhoud. \
  Je MOET ALLE secties opnemen die relevante inhoud bevatten.

<h3>{section_major_events}</h3>
Chronologisch verhaal van de gebeurtenissen in de sessie. \
Beschrijf ontdekte locaties, NPC-ontmoetingen en \
bevindingen. Gebruik een meeslepende en beschrijvende toon. \
Dit is de belangrijkste en langste sectie van de samenvatting. \
Rapporteer WAARNEMINGEN zoals ze zijn, zonder conclusies te trekken \
(bijv. als een harnas gloeit, CONCLUDEER NIET dat een draak in de buurt is).

<h3>{section_combat}</h3>
Schrijf voor ELK gevecht in de sessie een KORT VERHALEND ALINEA \
(3-5 zinnen) met: tegenstanders, opmerkelijke momenten \
(krachtige spreuken, critical hits, gevaren), en de uitkomst van het gevecht. \
SOM NIET elke beurt of worp afzonderlijk op. \
HERINNERING: WIJS GEEN spreuken of aanvallen toe aan een genoemd personage \
tenzij de naam EXPLICIET in het transcript staat. Gebruik bij voorkeur \
de lijdende vorm: "een Eldritch Blast treft", "een Divine Smite velt". \
Als er geen gevecht plaatsvond, LAAT deze sectie WEG.

<h3>{section_decisions}</h3>
ALLEEN de 3-5 meest impactvolle feiten voor de CAMPAGNE: \
geïdentificeerde magische voorwerpen (eigenschappen EN vloeken in één zin), \
belangrijke strategische keuzes, cruciale verkregen informatie. \
Opmaak: PLATTE lijst <ul>/<li>, ÉÉN regel per item, NUL sublijsten. \
VOORBEELD van correct formaat: \
<li><strong>Vervloekte bijl</strong> — +1 aanval/schade en +1 HP/niveau, \
maar onmogelijk te verlaten, berserk bij mislukte Wisdom Save, nadeel \
met andere wapens.</li>

<h3>{section_mysteries}</h3>
ALLEEN als een element uit deze sessie licht werpt op een mysterie dat AL BEKEND is \
uit de REFERENTIECONTEXT (codex-quest, Auril-dreiging, enz.). \
Maximaal 2-3 items. \
Opmaak: eenvoudige lijst <ul>/<li>, STELLENDE feitelijke zin. \
VERBODEN: retorische vragen, hypothesen, speculatie, werkwoorden als \
"suggereert", "lijkt", "zou kunnen", "wijst erop dat". \
VOORBEELD — GOED: "Vassavikens eed bevestigt dat Grimskal het \
leengoed was van een ijsreuzenkoningin die plundertochten leidde." \
FOUT: "De regeneratie van het wezen suggereert magie verbonden met Auril." \
(FOUT — dit is speculatie, geen waargenomen feit uit het transcript) \
Als niets bekende intrigues verlicht, LAAT deze sectie geheel WEG.
""",
    "prompt.summary_user": """\
REFERENTIECONTEXT (voorgaande sessies — NIET samenvatten, dient alleen \
om personages, plaatsen en reeds vastgestelde intrigues te begrijpen):
---
{context}
---

NIEUW TRANSCRIPT OM SAMEN TE VATTEN (vat ALLEEN deze inhoud samen):
---
{transcript}
---

Genereer een epische, gestructureerde samenvatting die UITSLUITEND de nieuwe \
gebeurtenissen van dit transcript behandelt. Behandel ALLE significante \
gebeurtenissen uit het transcript in chronologische volgorde — focus niet op \
één enkele scène ten koste van andere. Als het transcript niets relevants \
voor de campagne bevat, is het niet nodig om meer toe te voegen.
""",
    "prompt.condense": """\
Je bent een assistent gespecialiseerd in het verwerken van Dungeons & Dragons-\
sessietranscripten.

Het transcript komt van een spraak-naar-tekst-model dat veel artefacten \
produceert: herhaalde zinnen, incoherente tekst, verzonnen woorden, \
passages die niet gerelateerd zijn aan de D&D-sessie. Negeer deze \
parasitaire passages volledig.

Condenseer de tekst en behoud ALLEEN verhalende elementen die relevant \
zijn voor de D&D-campagne. Houd D&D-termen in het Engels. Antwoord in het {language_name}.

Elementen om ABSOLUUT TE BEWAREN:
- Namen van personages, NPC's en ontmoete wezens
- Ontdekte locaties met hun fysieke beschrijvingen
- NPC-DIALOGEN: bewaar ALLES wat een NPC onthult (informatie, \
  aanwijzingen, waarschuwingen, genoemde namen, lore). Dit is cruciaal — \
  informatie gegeven door NPC's is vaak het belangrijkste van de sessie.
- Gevecht: vijanden, numerieke waarden (worpen, schade, AC, DC, HP, initiatief)
- Magische voorwerpen: volledige eigenschappen EN vloeken
- MISLUKTE acties en hun gevolgen (explosies, ontvangen schade, mislukkingen)
- Beslissingen genomen door de groep en hun directe resultaten

ONDERSCHEID ACTIES vs VERWIJZINGEN:
- Spelers bespreken vaak EERDERE gebeurtenissen: samenvattingen van \
  voorgaande sessies, lore-herinneringen, planning. Deze discussies \
  zijn GEEN gebeurtenissen van de huidige sessie.
- Behoud alleen ACTIES die actief plaatsvinden: verkenning van locaties, \
  lopend gevecht, dialogen met ontmoete NPC's, gedane ontdekkingen, \
  genomen beslissingen.
- Als een speler een eerdere gebeurtenis NOEMT (bijv. "weet je nog de draak", \
  "vorige keer vonden we..."), is het een VERWIJZING — negeer het. \
  Alleen gebeurtenissen die PLAATSVINDEN tijdens de sessie tellen.
- TREK GEEN conclusies uit waarnemingen of spelersdiscussies. \
  Rapporteer ALLEEN ruwe feiten, nooit afleidingen.

BELANGRIJK:
- Geef ALLEEN ruwe verhalende feiten terug, in chronologische volgorde.
- VOEG GEEN metacommentaar, conclusies, samenvattingen, suggesties, \
  "belangrijkste punten", "volgende stappen" of "openstaande vragen" toe.
- VOEG GEEN scheidingstekens (---), opgemaakte sectietitels of \
  opmerkingen over transcriptkwaliteit toe.
- Bewaar de EXACTE personagenamen zoals gehoord \
  zonder ze te wijzigen of vraagtekens toe te voegen.
- Zelfs als de tekst veel ruis bevat, extraheer ELK fragment van \
  D&D-inhoud erin, hoe klein ook. Geef alleen een leeg \
  antwoord als de tekst 100% artefacten is zonder een coherente spelgerelateerde zin.

Tekst:
{text}
""",
    "prompt.quest_extraction": """\
Je bent een assistent gespecialiseerd in het bijhouden van quests voor een \
Dungeons & Dragons-campagne ({campaign_name}).

Genereer op basis van de onderstaande sessiesamenvatting en de huidige staat \
van de quest log het VOLLEDIGE opnieuw samengestelde quest log verrijkt met \
de nieuwe sessie-informatie. De quest log moet een levend document zijn dat \
de huidige staat van ALLE quests weerspiegelt.

ABSOLUTE REGEL — GEEF ALLEEN HTML TERUG:
- Geef ALLEEN de ruwe HTML van de quest log terug, NIETS anders.
- VERBODEN: geen inleiding ("Hier is de quest log..."), geen conclusie, \
  geen notities, geen commentaar, geen ```, geen ---.
- Het document begint met <h1> en eindigt met </ul>.

Exacte HTML-structuur om te produceren (alle 3 secties MOETEN aanwezig zijn):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Dit register houdt actieve quests, ontdekte aanwijzingen
en mysteries bij die gedurende de campagne ontrafeld moeten worden.</em></p>
<hr>
<h2 style="color:#6ab4d4;">{section_active_quests}</h2>
<ul>
<li><strong>Questnaam</strong> — Algemene beschrijving van de quest.
  <ul>
  <li><em>{quest_origin}:</em> Wie de quest gaf, waar en wanneer.</li>
  <li><em>{quest_objective}:</em> Wat er bereikt moet worden.</li>
  <li><em>{quest_progress}:</em> Wat er tot nu toe gedaan is.</li>
  <li><em>{quest_next_step}:</em> Wat er nog gedaan moet worden.</li>
  <li><em>{quest_npcs}:</em> Personages betrokken bij deze quest.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_clues}</h2>
<ul>
<li><strong>Mysterie</strong> — Wat bekend is, wat nog ontdekt moet worden.
  <ul>
  <li>Ontdekt detail of aanwijzing...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_completed_quests}</h2>
<ul>
<li><strong>Questnaam</strong> — Afloop en gevolgen.
  <ul>
  <li><em>{quest_giver}:</em> Wie de quest gaf en de beloning.</li>
  <li><em>{quest_resolution}:</em> Hoe de quest is afgerond.</li>
  </ul>
</li>
</ul>

Regels:
- Schrijf in het {language_name}, beknopt en FEITELIJK. Geen speculatie (geen \
  "zou kunnen", "lijkt", "suggereert"). Schrijf alleen wat bekend is.
- Houd D&D-termen in het Engels (Hit Points, Saving Throw, enz.).
- Eigennamen blijven ongewijzigd.
- Gebruik geneste opsommingslijsten voor details.
- Verplaats afgeronde quests van "Actieve Quests" naar "Voltooide Quests".
- BEWAAR ALLE bestaande quest log-informatie. VERLIES GEEN ENKEL \
  detail (questgever, beloning, NPC's, voortgang) van bestaande quests. \
  Verrijk met nieuwe informatie ZONDER oude informatie te verwijderen.
- Voeg nieuw ontdekte quests toe aan "Actieve Quests".
- Voeg nieuwe aanwijzingen toe aan "Aanwijzingen en Mysteries". Verwijder \
  een aanwijzing wanneer het mysterie is opgelost (vermeld de oplossing \
  bij de gerelateerde quest).
- De quest log moet een gedetailleerd naslagwerk zijn, niet slechts een lijst.

Huidige staat van de quest log:
---
{current_quests}
---

Sessiesamenvatting:
---
{summary}
---
""",
    # ── Prompt section headers (used in prompt placeholders) ─
    "prompt.section.major_events": "Belangrijke Gebeurtenissen",
    "prompt.section.combat": "Gevecht",
    "prompt.section.decisions": "Beslissingen en Ontdekkingen",
    "prompt.section.mysteries": "Mysteries en Aanwijzingen",
    "prompt.section.active_quests": "Actieve Quests",
    "prompt.section.clues": "Aanwijzingen en Mysteries",
    "prompt.section.completed_quests": "Voltooide Quests",
    "prompt.quest.origin": "Oorsprong",
    "prompt.quest.objective": "Doelstelling",
    "prompt.quest.progress": "Voortgang",
    "prompt.quest.next_step": "Volgende stap",
    "prompt.quest.npcs": "Betrokken NPC's",
    "prompt.quest.giver": "Questgever",
    "prompt.quest.resolution": "Afloop",
    "prompt.language_name": "Nederlands",
}
