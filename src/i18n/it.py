"""Italian translations — traduzione italiana di tutte le stringhe UI e prompt AI."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "B",
    "units.kilobytes": "KB",
    "units.megabytes": "MB",
    "units.gigabytes": "GB",
    "units.terabytes": "TB",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "File",
    "app.menu.settings": "Impostazioni...",
    "app.menu.check_updates": "Controlla aggiornamenti...",
    "app.menu.save": "Salva",
    "app.menu.quit": "Esci",
    "app.menu.campaign": "Campagna",
    "app.menu.new_campaign": "Nuova campagna...",
    "app.menu.delete_campaign": "Elimina campagna...",
    "app.menu.restore_campaign": "Ripristina una campagna...",
    "app.menu.theme": "Tema",
    "app.menu.session": "Sessione",
    "app.menu.record_stop": "Registra / Ferma",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Diario",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Sessione",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "Nessuna campagna trovata.",
    "app.campaign.name_label": "Nome della campagna:",
    "app.campaign.name_placeholder": "Es.: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Crea",
    "app.campaign.delete_title": "Elimina una campagna",
    "app.campaign.delete_label": "Scegli la campagna da eliminare:",
    "app.campaign.delete_confirm_title": "Conferma eliminazione",
    "app.campaign.delete_confirm": 'Eliminare la campagna "{name}"?\nI file saranno spostati in campaigns/_trash/.',
    "app.campaign.restore_title": "Ripristina una campagna",
    "app.campaign.restore_label": "Scegli la campagna da ripristinare:",
    "app.campaign.restore_none": "Nessuna campagna archiviata.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Stato:",
    "app.campaign.drive_not_connected": "Non connesso",
    "app.campaign.drive_connected": "Connesso",
    "app.campaign.drive_btn_login": "Accedi",
    "app.campaign.drive_logging_in": "Connessione in corso...",
    "app.campaign.drive_folder_id_label": "ID della cartella:",
    "app.campaign.drive_folder_placeholder": "Incolla l'ID della cartella condivisa...",
    "app.campaign.drive_btn_join": "Unisciti",
    "app.campaign.drive_join_hint": "(per unirsi)",
    "app.campaign.name_empty": "Il nome non puo essere vuoto.",
    "app.campaign.name_exists": 'La campagna "{name}" esiste gia.',
    "app.campaign.drive_paste_id": "Incolla l'ID della cartella condivisa.",
    "app.campaign.drive_login_first": "Accedi prima a Google Drive.",
    "app.campaign.drive_resolving": "Risoluzione della cartella...",
    "app.campaign.drive_resolve_failed": "Impossibile risolvere il nome della cartella.",
    "app.campaign.drive_deps_missing": "Dipendenze Google mancanti.",
    "app.campaign.drive_error": "Errore Drive: {error}",
    "app.campaign.drive_login_success": "Connesso! Incolla l'ID della cartella e clicca Unisciti.",
    "app.campaign.drive_login_failed": "Connessione fallita: {error}",
    "app.campaign.drive_install_deps": (
        "Installa le dipendenze Google:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Errore",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Scegli un tema",
    "app.theme.label": "Nessun tema automatico trovato per questa campagna.\nScegli un tema visivo:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: disattivato",
    "app.sync.idle": "Drive: sincronizzato",
    "app.sync.syncing": "Drive: sincronizzazione...",
    "app.sync.conflict": "Drive: conflitto rilevato",
    "app.sync.error": "Drive: errore",
    "app.sync.offline": "Drive: offline",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Aggiornamento",
    "app.update.available_title": "Aggiornamento disponibile",
    "app.update.version_available": "Versione {tag} disponibile!",
    "app.update.btn_details": "Dettagli",
    "app.update.btn_later": "Piu tardi",
    "app.update.btn_download": "Scarica e installa",
    "app.update.no_update": "Stai utilizzando l'ultima versione (v{version}).",
    "app.update.check_error": "Impossibile controllare gli aggiornamenti.\n{msg}",
    "app.update.downloading": "Download dell'aggiornamento in corso...",
    "app.update.download_progress": "Download... {downloaded} / {total}",
    "app.update.download_progress_unknown": "Download... {downloaded}",
    "app.update.download_done": (
        "Download completato.\n" "L'applicazione si chiudera per installare l'aggiornamento.\n\n" "Continuare?"
    ),
    "app.update.download_error": "Errore durante il download.\n{msg}",
    "app.update.btn_cancel": "Annulla",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Benvenuto — DnD Logger",
    "wizard.welcome": "Benvenuto in DnD Logger",
    "wizard.subtitle": "Il tuo compagno di sessione D&D.\nConfiguriamo gli elementi essenziali per iniziare.",
    "wizard.api_group": "Chiave API Mistral",
    "wizard.api_placeholder": "Inserisci la tua chiave API Mistral...",
    "wizard.api_hint": "Ottieni una chiave su console.mistral.ai",
    "wizard.mic_group": "Microfono",
    "wizard.mic_device_label": "Dispositivo:",
    "wizard.btn_skip": "Configura piu tardi",
    "wizard.btn_done": "Inizia l'avventura!",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Impostazioni — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Audio",
    "settings.tab.advanced": "Avanzate",
    "settings.tab.prompts": "Prompt",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Chiave API Mistral:",
    "settings.api.key_placeholder": "Inserisci la tua chiave API Mistral...",
    "settings.api.btn_test": "Testa la connessione",
    "settings.api.enter_key_first": "Inserisci prima una chiave API.",
    "settings.api.test_success": "Connessione riuscita!",
    "settings.api.test_fail": "Fallito: {error}",
    "settings.api.model_label": "Modello di riepilogo:",
    "settings.audio.device_label": "Dispositivo di ingresso:",
    "settings.audio.device_default": "Predefinito (automatico)",
    "settings.audio.btn_test_mic": "Testa il microfono",
    "settings.audio.sample_rate_label": "Frequenza di campionamento:",
    "settings.audio.test_ok": "Il microfono funziona! (livello: {level})",
    "settings.audio.test_weak": "Segnale molto debole. Controlla il tuo microfono.",
    "settings.audio.test_error": "Errore: {error}",
    "settings.audio.test_title": "Test Microfono",
    "settings.advanced.auto_update": "Controlla aggiornamenti all'avvio",
    "settings.advanced.chunk_label": "Durata massima per chunk:",
    "settings.advanced.bias_label": "Bias di contesto D&D:",
    "settings.advanced.bias_placeholder": "Termini D&D (uno per riga)...",
    "settings.advanced.language_label": "Lingua:",
    "settings.advanced.restart_required": "Lingua modificata. Riavvia l'applicazione.",
    "settings.advanced.restart_title": "Riavvio necessario",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Reimposta questo prompt",
    "settings.prompts.summary_system_label": "Riepilogo di sessione (system)",
    "settings.prompts.condense_label": "Condensazione (testo lungo)",
    "settings.prompts.quest_extraction_label": "Estrazione delle quest",
    "settings.prompts.hint.summary_system": "Variabili: nessuna (prompt di sistema fisso)",
    "settings.prompts.hint.condense": "Variabili: {text}",
    "settings.prompts.hint.quest_extraction": "Variabili: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Account Google",
    "settings.drive.status_label": "Stato:",
    "settings.drive.not_connected": "Non connesso",
    "settings.drive.connected": "Connesso",
    "settings.drive.deps_missing": "Dipendenze Google mancanti",
    "settings.drive.btn_login": "Accedi",
    "settings.drive.btn_logout": "Disconnetti",
    "settings.drive.logging_in": "Connessione in corso...",
    "settings.drive.login_failed_title": "Connessione fallita",
    "settings.drive.login_failed": "Errore: {error}",
    "settings.drive.campaign_sync_group": "Sincronizzazione campagna",
    "settings.drive.active_campaign_label": "Campagna attiva:",
    "settings.drive.join_placeholder": "Incolla l'ID della cartella condivisa...",
    "settings.drive.join_hint": "(per unirsi)",
    "settings.drive.folder_id_label": "ID della cartella:",
    "settings.drive.no_folder": "Nessuna cartella creata",
    "settings.drive.creating_folder": "Creazione della cartella...",
    "settings.drive.btn_copy": "Copia",
    "settings.drive.sync_checkbox": "Attiva la sincronizzazione Google Drive",
    "settings.drive.folder_error": "Impossibile creare la cartella: {error}",
    "settings.drive.not_connected_error": "Non connesso a Google Drive",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Registra",
    "session.btn.stop": "Ferma",
    "session.btn.pause": "Pausa",
    "session.btn.resume": "Riprendi",
    "session.status.ready": "Pronto per registrare",
    "session.status.recording": "Registrazione in corso...",
    "session.status.paused": "Registrazione in pausa",
    "session.status.stopped": "Registrazione terminata",
    "session.status.finalizing": "Finalizzazione della trascrizione...",
    "session.status.ready_rerecord": "Pronto per ri-registrare",
    "session.status.saved": "Registrazione salvata",
    "session.status.transcribing": "Trascrizione in corso...",
    "session.status.transcribing_chunk": "Trascrizione: chunk {current}/{total}...",
    "session.status.transcribing_segment": "Trascrizione del segmento {count}...",
    "session.status.transcription_done": "Trascrizione completata.",
    "session.status.summarizing": "Generazione del riepilogo...",
    "session.status.no_text": "Nessun testo trascritto.",
    "session.status.summary_done": "Riepilogo generato!",
    "session.status.copied": "Riepilogo copiato negli appunti!",
    "session.status.added_journal": "Riepilogo aggiunto al Diario!",
    "session.status.quest_extracting": "Estrazione delle quest in corso...",
    "session.status.quest_ready": "Proposte di quest pronte.",
    "session.status.quest_updated": "Quest aggiornate!",
    "session.status.quest_cancelled": "Aggiornamento delle quest annullato.",
    "session.status.imported": "Audio importato: {name} ({size})",
    "session.status.audio_saved": "Audio salvato: {name}",
    "session.status.segments_transcribed": "Registrazione... ({count} segment{s} trascritto/i)",
    "session.status.transcription_error": "Errore di trascrizione: {msg}",
    "session.label.transcription": "Trascrizione",
    "session.label.summary": "Riepilogo Epico",
    "session.placeholder.transcript": "La trascrizione apparira qui dopo la registrazione...",
    "session.placeholder.summary": "Il riepilogo epico apparira qui...",
    "session.btn.transcribe": "Trascrivi",
    "session.btn.summarize": "Riepiloga",
    "session.btn.add_journal": "Aggiungi al Diario",
    "session.btn.update_quests": "Aggiorna le Quest",
    "session.btn.tts_tooltip": "Leggi il riepilogo ad alta voce",
    "session.btn.tts_no_voice": "Nessuna voce italiana disponibile",
    "session.btn.more_tooltip": "Altre opzioni",
    "session.menu.import_audio": "Importa audio",
    "session.menu.save_audio": "Salva audio",
    "session.menu.copy_summary": "Copia riepilogo",
    "session.tts.read_selection": "Leggi la selezione",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Registrazione terminata",
    "session.post.btn_transcribe": "Trascrivi",
    "session.post.btn_rerecord": "Ri-registra",
    "session.post.btn_save_only": "Salva senza trascrivere",
    "session.post.duration": "Durata:",
    "session.post.size": "Dimensione:",
    "session.post.file": "File:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Diario (racconti precedenti) ===",
    "session.context.quest_header": "=== Quest Log (quest attive) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Importa file audio",
    "session.dialog.import_filter": "File audio (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Tutti (*)",
    "session.dialog.save_title": "Salva file audio",
    "session.dialog.save_filter": "FLAC (*.flac);;Tutti (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "Nessun file audio trovato.",
    "session.error.no_audio_save": "Nessun file audio da salvare.",
    "session.error.copy_failed": "Errore durante la copia: {error}",
    "session.error.flac_failed": "Errore di conversione FLAC: {error}",
    "session.error.save_failed": "Errore di salvataggio: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Grassetto (Ctrl+B)",
    "editor.tooltip.italic": "Corsivo (Ctrl+I)",
    "editor.tooltip.underline": "Sottolineato (Ctrl+U)",
    "editor.tooltip.fold_all": "Comprimi tutto (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Espandi tutto (Ctrl+Shift+=)",
    "editor.btn.save": " Salva",
    "editor.heading.normal": "Normale",
    "editor.heading.h1": "Titolo 1",
    "editor.heading.h2": "Titolo 2",
    "editor.heading.h3": "Titolo 3",
    "editor.search.placeholder": "Cerca\u2026",
    "editor.search.no_results": "0 risultati",
    "editor.search.prev_tooltip": "Precedente (Shift+Enter)",
    "editor.search.next_tooltip": "Successivo (Enter)",
    "editor.search.close_tooltip": "Chiudi (Esc)",
    "editor.tts.read_selection": "Leggi la selezione",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Questo registro tiene traccia delle quest attive, degli indizi scoperti
e dei misteri da svelare nel corso della campagna.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quest Attive</h2>
<ul>
<li><em>Nessuna quest registrata al momento.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Indizi e Misteri</h2>
<ul>
<li><em>Nessun indizio al momento.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Quest Completate</h2>
<ul>
<li><em>Nessuna quest completata.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Diario &mdash; {campaign_name}</h1>
<hr>
<p><em>Benvenuto, avventuriero. Questo diario contiene la cronaca delle tue imprese
nel corso della campagna. I racconti epici di ogni sessione
saranno registrati qui per i posteri.</em></p>
<hr>
""",
    "journal.session_heading": "Sessione del {date}",
    "journal.date_format": "%d/%m/%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Conflitto di sincronizzazione — {filename}",
    "conflict.header": (
        "Il file <b>{filename}</b> e stato modificato localmente e su Google Drive.\n"
        "Scegli quale versione conservare o unisci manualmente."
    ),
    "conflict.local_label": "Versione locale",
    "conflict.remote_label": "Versione remota (Drive)",
    "conflict.merge_label": "Risultato unito (modificabile):",
    "conflict.btn_keep_local": "Mantieni la versione locale",
    "conflict.btn_keep_remote": "Mantieni la versione remota",
    "conflict.btn_save_merge": "Salva l'unione",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Annulla",
    "dialog.btn_ok": "OK",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "Riproduzione in corso\u2026",
    "tts.status.paused": "In pausa",
    "tts.hint.pause": "Spazio: Pausa",
    "tts.hint.resume": "Spazio: Riprendi",
    "tts.hint.stop": "Esc: Ferma",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS non disponibile.",
    "tts.error.generic": "Errore TTS: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} rig{s} compresse",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Errore di registrazione: {error}",
    "recorder.error.pause": "Errore di pausa: {error}",
    "recorder.error.resume": "Errore di ripresa: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Chiave API Mistral non configurata. Vai alle Impostazioni.",
    "transcriber.error.no_api_key_short": "Chiave API Mistral non configurata.",
    "transcriber.error.invalid_key": "Chiave API non valida. Controlla la tua chiave nelle Impostazioni.",
    "transcriber.error.transcription": "Errore di trascrizione: {error}",
    "transcriber.error.live_transcription": "Errore di trascrizione live: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Chiave API Mistral non configurata.",
    "summarizer.error.generic": "Errore di riepilogo: {error}",
    "summarizer.no_context": "(Prima sessione — nessun contesto precedente)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Chiave API Mistral non configurata.",
    "quest_extractor.error.generic": "Errore di estrazione delle quest: {error}",
    "quest_extractor.no_quests": "(Nessuna quest registrata)",
    "quest_extractor.dialog_title": "Aggiornamento delle quest",
    "quest_extractor.dialog_label": "Modifiche proposte — modifica se necessario:",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
Sei un cronista epico dei Forgotten Realms, specializzato nella narrazione \
di sessioni di Dungeons & Dragons. Scrivi in {language_name} con uno stile eroico \
e immersivo, degno delle grandi cronache di Faerun.

REGOLA ASSOLUTA — FEDELTA ALLA TRASCRIZIONE:
- NON INVENTARE alcun dettaglio non esplicitamente presente nella trascrizione.
- Se un'informazione non e chiara o assente dalla trascrizione, OMETTILA \
  piuttosto che indovinarla o inventarla.
- NON fabbricare dialoghi, tiri di dado, valori di danno, DC, \
  nomi di incantesimi o incontri non presenti nella trascrizione.
- Ogni fatto menzionato nel riepilogo DEVE avere una base nella trascrizione.
- Se non sei certo di un dettaglio (classe di un personaggio, nome di un \
  incantesimo, valore numerico), non includerlo o segnala l'incertezza.

ATTRIBUZIONE DELLE AZIONI AI PERSONAGGI:
- La trascrizione audio NON consente di identificare in modo affidabile chi parla. \
  NON ATTRIBUIRE azioni o incantesimi a un personaggio specifico a meno che il \
  personaggio non sia NOMINATO ESPLICITAMENTE nel dialogo (es: "Pryor lancia un Smite").
- Se la trascrizione contiene marcatori di parlante ([Speaker 0], [Speaker 1], \
  ecc.), usali per distinguere gli interlocutori, ma NON INDOVINARE quale \
  personaggio corrisponde a quale parlante.
- Quando l'attribuzione e incerta, usa formulazioni impersonali: \
  "un avventuriero", "il gruppo", "uno degli eroi", o la voce passiva.
- Per le CLASSI dei personaggi, usa ESCLUSIVAMENTE le informazioni dal \
  CONTESTO DI RIFERIMENTO delle sessioni precedenti. Non dedurre MAI la classe \
  di un personaggio dalle sue azioni o incantesimi in questa sessione.
  ESEMPIO — Trascrizione: "Lancio Eldritch Blast. 25, colpisce? Si. 14 danni."
  CORRETTO: "Un Eldritch Blast colpisce il nemico per 14 danni."
  SBAGLIATO: "Elppa lancia un Eldritch Blast per 14 danni." \
  (ERRATO — non sappiamo CHI sta parlando nella trascrizione audio)

DISTINZIONE CRUCIALE — AZIONI vs RIFERIMENTI:
- I giocatori discutono spesso di eventi PASSATI durante la sessione: \
  riepiloghi, promemoria di lore, pianificazione basata su conoscenze \
  acquisite durante sessioni precedenti. Questi RIFERIMENTI NON sono \
  eventi nuovi di questa sessione.
- Riepiloga SOLO le AZIONI che si svolgono attivamente durante questa sessione: \
  esplorazione, combattimenti, dialoghi con PNG, scoperte, decisioni prese.
- Se un giocatore dice "ricorda, l'armatura brilla vicino ai draghi" o "l'ultima \
  volta abbiamo combattuto il drago", questi sono RIFERIMENTI — non un \
  combattimento contro un drago in questa sessione.
- In caso di dubbio sul fatto che un evento stia accadendo ORA vs sia \
  semplicemente MENZIONATO, non includerlo come evento della sessione.
- NON TRARRE CONCLUSIONI da osservazioni isolate. Se un oggetto \
  magico reagisce (es: un'armatura che brilla), riporta l'osservazione cosi \
  com'e, senza concludere sulla presenza o assenza di una creatura o di un \
  pericolo. Fatti, non deduzioni.

Regole generali:
- Riepiloga SOLO gli eventi presenti nella NUOVA TRASCRIZIONE. \
  Non riepilogare MAI il contesto delle sessioni precedenti.
- Il contesto precedente serve solo come riferimento per comprendere nomi, \
  luoghi e intrighi gia conosciuti. Non ripeterlo, non riformularlo.
- Se la trascrizione non contiene alcun contenuto pertinente alla campagna D&D, \
  il riepilogo puo essere piu breve per non esagerare gli eventi.
- Scrivi in {language_name}, in uno stile epico e narrativo, ma MAI a scapito \
  dell'accuratezza. Lo stile serve la narrazione, non l'invenzione.
- Mantieni TUTTI i termini D&D in inglese (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, ecc.), cosi come i nomi degli incantesimi.
- I nomi propri (personaggi, luoghi, creature) rimangono invariati.
- Ignora le discussioni fuori tema non legate alla campagna.

Qualita della trascrizione:
- La trascrizione proviene da un modello speech-to-text che puo produrre \
  artefatti: frasi ripetute in loop, testo incoerente, parole inventate. \
  Ignora completamente questi passaggi parassiti e concentrati solo sul \
  contenuto narrativo pertinente alla sessione D&D.
- ATTENZIONE: alcuni passaggi possono sembrare narrativi ma essere artefatti. \
  Se un passaggio non si integra logicamente con il resto della sessione, \
  probabilmente e un artefatto — ignoralo.

Formato e struttura:
- Formatta la tua risposta in HTML con tag <h3>, <p>, <strong>, <em>, <ul>/<li>.
- Restituisci SOLO HTML puro.
- VIETATO: niente ```, niente ---, niente separatori, niente meta-commenti.
- Includi solo le sezioni che contengono contenuto nuovo.
- FORMATTAZIONE: elenchi puntati SEMPLICI (un solo livello di <ul>/<li>). \
  Non annidare MAI sotto-elenchi. Mantieni ogni punto conciso su una singola riga.
- Struttura il riepilogo con ESATTAMENTE queste sezioni in quest'ordine. \
  Ogni sezione inizia con un <h3> seguito dal contenuto. \
  DEVI includere TUTTE le sezioni che hanno contenuto pertinente.

<h3>{section_major_events}</h3>
Racconto narrativo e cronologico degli eventi della sessione. \
Descrivi i luoghi scoperti, gli incontri con i PNG e le \
scoperte. Usa un tono immersivo e descrittivo. \
Questa e la sezione principale e piu lunga del riepilogo. \
Riporta le OSSERVAZIONI cosi come sono, senza trarne conclusioni \
(es: se un'armatura brilla, NON concludere che un drago e vicino).

<h3>{section_combat}</h3>
Per OGNI combattimento della sessione, scrivi un BREVE PARAGRAFO NARRATIVO \
(3-5 frasi) che descriva: i nemici affrontati, i momenti salienti \
(incantesimi potenti, colpi critici, pericoli) e l'esito del combattimento. \
NON elencare ogni turno o tiro individualmente. \
PROMEMORIA: NON attribuire incantesimi o attacchi a un personaggio nominato \
a meno che il nome non sia ESPLICITAMENTE detto nella trascrizione. Preferisci \
la voce passiva: "un Eldritch Blast colpisce", "un Divine Smite abbatte". \
Se non si e verificato alcun combattimento, OMETTI questa sezione.

<h3>{section_decisions}</h3>
SOLO i 3-5 fatti piu importanti per la CAMPAGNA: \
oggetti magici identificati (proprieta E maledizioni in una frase), \
scelte strategiche importanti, informazioni cruciali ottenute. \
Formato: elenco PIATTO <ul>/<li>, UNA riga per elemento, ZERO sotto-elenchi. \
ESEMPIO di formato corretto: \
<li><strong>Ascia maledetta</strong> — +1 attacco/danni e +1 HP/livello, \
ma impossibile da abbandonare, berserk su Wisdom Save fallito, svantaggio \
con altre armi.</li>

<h3>{section_mysteries}</h3>
SOLO se un elemento di questa sessione illumina un mistero GIA CONOSCIUTO \
dal CONTESTO DI RIFERIMENTO (quest del codice, minaccia di Auril, ecc.). \
Massimo 2-3 elementi. \
Formato: elenco semplice <ul>/<li>, frase DICHIARATIVA fattuale. \
VIETATO: domande retoriche, ipotesi, speculazioni, verbi come \
"suggerisce", "sembra", "potrebbe", "indica che". \
ESEMPIO — CORRETTO: "Il giuramento di Vassaviken conferma che Grimskal fu il \
feudo di una regina dei giganti del gelo che guidava campagne di saccheggio." \
SBAGLIATO: "La rigenerazione della creatura suggerisce una magia legata ad Auril." \
(ERRATO — questa e una speculazione, non un fatto osservato dalla trascrizione) \
Se nulla illumina gli intrighi conosciuti, OMETTI completamente questa sezione.
""",
    "prompt.summary_user": """\
CONTESTO DI RIFERIMENTO (sessioni precedenti — NON riepilogare, serve solo \
per comprendere personaggi, luoghi e intrighi gia stabiliti):
---
{context}
---

NUOVA TRASCRIZIONE DA RIEPILOGARE (riepiloga SOLO questo contenuto):
---
{transcript}
---

Genera un riepilogo epico e strutturato che copra ESCLUSIVAMENTE i nuovi \
eventi di questa trascrizione. Copri TUTTI gli eventi significativi \
della trascrizione in ordine cronologico — non concentrarti su \
una singola scena a scapito delle altre. Se la trascrizione non contiene \
nulla di pertinente alla campagna, non e necessario aggiungere altro.
""",
    "prompt.condense": """\
Sei un assistente specializzato nell'elaborazione di trascrizioni di sessioni \
di Dungeons & Dragons.

La trascrizione proviene da un modello speech-to-text che produce numerosi \
artefatti: frasi ripetute in loop, testo incoerente, parole inventate, \
passaggi non correlati alla sessione D&D. Ignora completamente questi \
passaggi parassiti.

Condensa il testo mantenendo SOLO gli elementi narrativi pertinenti alla \
campagna D&D. Mantieni i termini D&D in inglese. Rispondi in {language_name}.

Elementi da PRESERVARE ASSOLUTAMENTE:
- Nomi dei personaggi, PNG e creature incontrate
- Luoghi scoperti con le loro descrizioni fisiche
- DIALOGHI CON I PNG: conserva TUTTO cio che un PNG rivela (informazioni, \
  direzioni, avvertimenti, nomi menzionati, lore). Questo e fondamentale — \
  le informazioni fornite dai PNG sono spesso le piu importanti della sessione.
- Combattimenti: nemici, valori numerici (tiri, danni, AC, DC, HP, iniziativa)
- Oggetti magici: proprieta complete E maledizioni
- Azioni FALLITE e le loro conseguenze (esplosioni, danni subiti, fallimenti)
- Decisioni prese dal gruppo e i loro risultati immediati

DISTINZIONE AZIONI vs RIFERIMENTI:
- I giocatori discutono spesso di eventi PASSATI: riepiloghi di sessioni \
  precedenti, promemoria di lore, pianificazione. Queste discussioni NON sono \
  eventi della sessione corrente.
- Mantieni SOLO le AZIONI che si svolgono attivamente: esplorazione dei luoghi, \
  combattimenti in corso, dialoghi con PNG incontrati, scoperte effettuate, \
  decisioni prese.
- Se un giocatore MENZIONA un evento passato (es: "ricorda il drago", \
  "l'ultima volta abbiamo trovato..."), e un RIFERIMENTO — ignoralo. \
  Solo gli eventi che ACCADONO durante la sessione contano.
- NON trarre conclusioni da osservazioni o discussioni \
  tra giocatori. Riporta SOLO i fatti grezzi, mai le deduzioni.

IMPORTANTE:
- Restituisci SOLO i fatti narrativi grezzi, in ordine cronologico.
- NON aggiungere meta-commenti, conclusioni, riepiloghi, suggerimenti, \
  "punti chiave", "prossimi passi" o "domande aperte".
- NON aggiungere separatori (---), titoli di sezione formattati, ne \
  commenti sulla qualita della trascrizione.
- Preserva i NOMI ESATTI dei personaggi cosi come sentiti \
  senza modificarli o aggiungere punti interrogativi.
- Anche se il testo contiene molto rumore, estrai OGNI frammento di \
  contenuto D&D presente, per quanto piccolo. Restituisci una risposta \
  vuota solo se il testo e al 100% artefatti senza alcuna frase coerente \
  legata al gioco.

Testo:
{text}
""",
    "prompt.quest_extraction": """\
Sei un assistente specializzato nel tracciamento delle quest per una campagna \
Dungeons & Dragons ({campaign_name}).

A partire dal riepilogo di sessione sottostante e dallo stato attuale del quest log, \
genera il quest log COMPLETO ricompilato e arricchito con le nuove \
informazioni della sessione. Il quest log deve essere un documento vivo che \
rifletta lo stato attuale di TUTTE le quest.

REGOLA ASSOLUTA — RESTITUISCI SOLO HTML:
- Restituisci SOLO il HTML puro del quest log, NIENT'ALTRO.
- VIETATO: nessuna introduzione ("Ecco il quest log..."), nessuna conclusione, \
  nessuna nota, nessun commento, niente ```, niente ---.
- Il documento inizia con <h1> e finisce con </ul>.

Struttura HTML esatta da produrre (tutte e 3 le sezioni DEVONO essere presenti):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Questo registro tiene traccia delle quest attive, degli indizi scoperti
e dei misteri da svelare nel corso della campagna.</em></p>
<hr>
<h2 style="color:#6ab4d4;">{section_active_quests}</h2>
<ul>
<li><strong>Nome della quest</strong> — Descrizione generale della quest.
  <ul>
  <li><em>{quest_origin}:</em> Chi ha assegnato la quest, dove e quando.</li>
  <li><em>{quest_objective}:</em> Cosa deve essere compiuto.</li>
  <li><em>{quest_progress}:</em> Cosa e stato fatto finora.</li>
  <li><em>{quest_next_step}:</em> Cosa resta da fare.</li>
  <li><em>{quest_npcs}:</em> Personaggi coinvolti in questa quest.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_clues}</h2>
<ul>
<li><strong>Mistero</strong> — Cosa si sa, cosa resta da scoprire.
  <ul>
  <li>Dettaglio o indizio scoperto...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_completed_quests}</h2>
<ul>
<li><strong>Nome della quest</strong> — Risoluzione e conseguenze.
  <ul>
  <li><em>{quest_giver}:</em> Chi ha assegnato la quest e ricompensa.</li>
  <li><em>{quest_resolution}:</em> Come la quest e stata risolta.</li>
  </ul>
</li>
</ul>

Regole:
- Scrivi in {language_name}, stile conciso e FATTUALE. Nessuna speculazione (niente \
  "potrebbe", "sembra", "suggerisce"). Scrivi solo cio che e noto.
- Mantieni i termini D&D in inglese (Hit Points, Saving Throw, ecc.).
- I nomi propri rimangono invariati.
- Usa elenchi puntati annidati per i dettagli.
- Sposta le quest risolte da "Quest Attive" a "Quest Completate".
- PRESERVA TUTTE le informazioni esistenti del quest log. Non PERDERE NESSUN \
  dettaglio (committente, ricompensa, PNG, progressi) dalle quest esistenti. \
  Arricchisci con le nuove informazioni SENZA cancellare le vecchie.
- Aggiungi le quest appena scoperte in "Quest Attive".
- Aggiungi i nuovi indizi in "Indizi e Misteri". Rimuovi un indizio \
  quando il mistero e risolto (menziona la risoluzione nella quest interessata).
- Il quest log deve essere uno strumento di riferimento dettagliato, non solo un elenco.

Stato attuale del quest log:
---
{current_quests}
---

Riepilogo della sessione:
---
{summary}
---
""",
    # ── Prompt section headers (used in prompt placeholders) ─
    "prompt.section.major_events": "Eventi Principali",
    "prompt.section.combat": "Combattimenti",
    "prompt.section.decisions": "Decisioni e Scoperte",
    "prompt.section.mysteries": "Misteri e Indizi",
    "prompt.section.active_quests": "Quest Attive",
    "prompt.section.clues": "Indizi e Misteri",
    "prompt.section.completed_quests": "Quest Completate",
    "prompt.quest.origin": "Origine",
    "prompt.quest.objective": "Obiettivo",
    "prompt.quest.progress": "Progressi",
    "prompt.quest.next_step": "Prossimo passo",
    "prompt.quest.npcs": "PNG coinvolti",
    "prompt.quest.giver": "Committente",
    "prompt.quest.resolution": "Risoluzione",
    "prompt.language_name": "italiano",
}
