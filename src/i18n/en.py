"""English translations — source of truth for all UI strings and AI prompts."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "B",
    "units.kilobytes": "KB",
    "units.megabytes": "MB",
    "units.gigabytes": "GB",
    "units.terabytes": "TB",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "File",
    "app.menu.settings": "Settings...",
    "app.menu.check_updates": "Check for updates...",
    "app.menu.save": "Save",
    "app.menu.quit": "Quit",
    "app.menu.campaign": "Campaign",
    "app.menu.new_campaign": "New campaign...",
    "app.menu.delete_campaign": "Delete campaign...",
    "app.menu.restore_campaign": "Restore a campaign...",
    "app.menu.theme": "Theme",
    "app.menu.session": "Session",
    "app.menu.record_stop": "Record / Stop",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Journal",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Session",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "No campaigns found.",
    "app.campaign.name_label": "Campaign name:",
    "app.campaign.name_placeholder": "E.g.: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Create",
    "app.campaign.delete_title": "Delete a campaign",
    "app.campaign.delete_label": "Choose the campaign to delete:",
    "app.campaign.delete_confirm_title": "Confirm deletion",
    "app.campaign.delete_confirm": 'Delete the campaign "{name}"?\nFiles will be moved to campaigns/_trash/.',
    "app.campaign.restore_title": "Restore a campaign",
    "app.campaign.restore_label": "Choose the campaign to restore:",
    "app.campaign.restore_none": "No archived campaigns.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Status:",
    "app.campaign.drive_not_connected": "Not connected",
    "app.campaign.drive_connected": "Connected",
    "app.campaign.drive_btn_login": "Log in",
    "app.campaign.drive_logging_in": "Connecting...",
    "app.campaign.drive_folder_id_label": "Folder ID:",
    "app.campaign.drive_folder_placeholder": "Paste the shared folder ID...",
    "app.campaign.drive_btn_join": "Join",
    "app.campaign.drive_join_hint": "(to join)",
    "app.campaign.name_empty": "Name cannot be empty.",
    "app.campaign.name_exists": 'The campaign "{name}" already exists.',
    "app.campaign.drive_paste_id": "Paste the shared folder ID.",
    "app.campaign.drive_login_first": "Log in to Google Drive first.",
    "app.campaign.drive_resolving": "Resolving folder...",
    "app.campaign.drive_resolve_failed": "Unable to resolve folder name.",
    "app.campaign.drive_deps_missing": "Google dependencies missing.",
    "app.campaign.drive_error": "Drive error: {error}",
    "app.campaign.drive_login_success": "Connected! Paste the folder ID and click Join.",
    "app.campaign.drive_login_failed": "Connection failed: {error}",
    "app.campaign.drive_install_deps": (
        "Install Google dependencies:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Error",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Choose a theme",
    "app.theme.label": "No automatic theme found for this campaign.\nChoose a visual theme:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: disabled",
    "app.sync.idle": "Drive: synced",
    "app.sync.syncing": "Drive: syncing...",
    "app.sync.conflict": "Drive: conflict detected",
    "app.sync.error": "Drive: error",
    "app.sync.offline": "Drive: offline",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Update",
    "app.update.available_title": "Update available",
    "app.update.version_available": "Version {tag} available!",
    "app.update.btn_details": "Details",
    "app.update.btn_later": "Later",
    "app.update.btn_download": "Download and install",
    "app.update.no_update": "You are running the latest version (v{version}).",
    "app.update.check_error": "Unable to check for updates.\n{msg}",
    "app.update.downloading": "Downloading update...",
    "app.update.download_progress": "Downloading... {downloaded} / {total}",
    "app.update.download_progress_unknown": "Downloading... {downloaded}",
    "app.update.download_done": (
        "Download complete.\n" "The application will close to install the update.\n\n" "Continue?"
    ),
    "app.update.download_error": "Error during download.\n{msg}",
    "app.update.btn_cancel": "Cancel",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Welcome — DnD Logger",
    "wizard.welcome": "Welcome to DnD Logger",
    "wizard.subtitle": "Your D&D session companion.\nLet's set up the essentials to get started.",
    "wizard.api_group": "Mistral API Key",
    "wizard.api_placeholder": "Enter your Mistral API key...",
    "wizard.api_hint": "Get a key at console.mistral.ai",
    "wizard.mic_group": "Microphone",
    "wizard.mic_device_label": "Device:",
    "wizard.btn_skip": "Configure later",
    "wizard.btn_done": "Begin the adventure!",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Settings — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Audio",
    "settings.tab.advanced": "Advanced",
    "settings.tab.prompts": "Prompts",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Mistral API Key:",
    "settings.api.key_placeholder": "Enter your Mistral API key...",
    "settings.api.btn_test": "Test connection",
    "settings.api.enter_key_first": "Enter an API key first.",
    "settings.api.test_success": "Connection successful!",
    "settings.api.test_fail": "Failed: {error}",
    "settings.api.model_label": "Summary model:",
    "settings.audio.device_label": "Input device:",
    "settings.audio.device_default": "Default (automatic)",
    "settings.audio.btn_test_mic": "Test microphone",
    "settings.audio.sample_rate_label": "Sample rate:",
    "settings.audio.test_ok": "Microphone works! (level: {level})",
    "settings.audio.test_weak": "Very weak signal. Check your microphone.",
    "settings.audio.test_error": "Error: {error}",
    "settings.audio.test_title": "Microphone Test",
    "settings.advanced.auto_update": "Check for updates at startup",
    "settings.advanced.chunk_label": "Max chunk duration:",
    "settings.advanced.bias_label": "D&D context bias:",
    "settings.advanced.bias_placeholder": "D&D terms (one per line)...",
    "settings.advanced.language_label": "Language:",
    "settings.advanced.restart_required": "Language changed. Please restart the application.",
    "settings.advanced.restart_title": "Restart required",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Reset this prompt",
    "settings.prompts.summary_system_label": "Session summary (system)",
    "settings.prompts.condense_label": "Condensation (long text)",
    "settings.prompts.quest_extraction_label": "Quest extraction",
    "settings.prompts.hint.summary_system": "Variables: none (fixed system prompt)",
    "settings.prompts.hint.condense": "Variables: {text}",
    "settings.prompts.hint.quest_extraction": "Variables: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Google Account",
    "settings.drive.status_label": "Status:",
    "settings.drive.not_connected": "Not connected",
    "settings.drive.connected": "Connected",
    "settings.drive.deps_missing": "Google dependencies missing",
    "settings.drive.btn_login": "Log in",
    "settings.drive.btn_logout": "Log out",
    "settings.drive.logging_in": "Connecting...",
    "settings.drive.login_failed_title": "Connection failed",
    "settings.drive.login_failed": "Error: {error}",
    "settings.drive.campaign_sync_group": "Campaign sync",
    "settings.drive.active_campaign_label": "Active campaign:",
    "settings.drive.join_placeholder": "Paste the shared folder ID...",
    "settings.drive.join_hint": "(to join)",
    "settings.drive.folder_id_label": "Folder ID:",
    "settings.drive.no_folder": "No folder created",
    "settings.drive.creating_folder": "Creating folder...",
    "settings.drive.btn_copy": "Copy",
    "settings.drive.sync_checkbox": "Enable Google Drive sync",
    "settings.drive.folder_error": "Unable to create folder: {error}",
    "settings.drive.not_connected_error": "Not connected to Google Drive",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Record",
    "session.btn.stop": "Stop",
    "session.btn.pause": "Pause",
    "session.btn.resume": "Resume",
    "session.status.ready": "Ready to record",
    "session.status.recording": "Recording...",
    "session.status.paused": "Recording paused",
    "session.status.stopped": "Recording stopped",
    "session.status.finalizing": "Finalizing transcription...",
    "session.status.ready_rerecord": "Ready to re-record",
    "session.status.saved": "Recording saved",
    "session.status.transcribing": "Transcribing...",
    "session.status.transcribing_chunk": "Transcription: chunk {current}/{total}...",
    "session.status.transcribing_segment": "Transcribing segment {count}...",
    "session.status.transcription_done": "Transcription complete.",
    "session.status.summarizing": "Generating summary...",
    "session.status.no_text": "No text transcribed.",
    "session.status.summary_done": "Summary generated!",
    "session.status.copied": "Summary copied to clipboard!",
    "session.status.added_journal": "Summary added to Journal!",
    "session.status.quest_extracting": "Extracting quests...",
    "session.status.quest_ready": "Quest proposals ready.",
    "session.status.quest_updated": "Quests updated!",
    "session.status.quest_cancelled": "Quest update cancelled.",
    "session.status.imported": "Audio imported: {name} ({size})",
    "session.status.audio_saved": "Audio saved: {name}",
    "session.status.segments_transcribed": "Recording... ({count} segment{s} transcribed)",
    "session.status.transcription_error": "Transcription error: {msg}",
    "session.label.transcription": "Transcription",
    "session.label.summary": "Epic Summary",
    "session.placeholder.transcript": "The transcript will appear here after recording...",
    "session.placeholder.summary": "The epic summary will appear here...",
    "session.btn.transcribe": "Transcribe",
    "session.btn.summarize": "Summarize",
    "session.btn.add_journal": "Add to Journal",
    "session.btn.update_quests": "Update Quests",
    "session.btn.tts_tooltip": "Read the summary aloud",
    "session.btn.tts_no_voice": "No French voice available",
    "session.btn.more_tooltip": "More options",
    "session.menu.import_audio": "Import audio",
    "session.menu.save_audio": "Save audio",
    "session.menu.copy_summary": "Copy summary",
    "session.tts.read_selection": "Read selection",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Recording complete",
    "session.post.btn_transcribe": "Transcribe",
    "session.post.btn_rerecord": "Re-record",
    "session.post.btn_save_only": "Save without transcribing",
    "session.post.duration": "Duration:",
    "session.post.size": "Size:",
    "session.post.file": "File:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Journal (previous stories) ===",
    "session.context.quest_header": "=== Quest Log (active quests) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Import audio file",
    "session.dialog.import_filter": "Audio files (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;All (*)",
    "session.dialog.save_title": "Save audio file",
    "session.dialog.save_filter": "FLAC (*.flac);;All (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "No audio file found.",
    "session.error.no_audio_save": "No audio file to save.",
    "session.error.copy_failed": "Error copying: {error}",
    "session.error.flac_failed": "FLAC conversion error: {error}",
    "session.error.save_failed": "Save error: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Bold (Ctrl+B)",
    "editor.tooltip.italic": "Italic (Ctrl+I)",
    "editor.tooltip.underline": "Underline (Ctrl+U)",
    "editor.tooltip.fold_all": "Fold all (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Unfold all (Ctrl+Shift+=)",
    "editor.btn.save": " Save",
    "editor.heading.normal": "Normal",
    "editor.heading.h1": "Heading 1",
    "editor.heading.h2": "Heading 2",
    "editor.heading.h3": "Heading 3",
    "editor.search.placeholder": "Search\u2026",
    "editor.search.no_results": "0 results",
    "editor.search.prev_tooltip": "Previous (Shift+Enter)",
    "editor.search.next_tooltip": "Next (Enter)",
    "editor.search.close_tooltip": "Close (Esc)",
    "editor.tts.read_selection": "Read selection",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>This register tracks active quests, discovered clues,
and mysteries to unravel throughout the campaign.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Active Quests</h2>
<ul>
<li><em>No quests recorded yet.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Clues and Mysteries</h2>
<ul>
<li><em>No clues yet.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Completed Quests</h2>
<ul>
<li><em>No quests completed.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Journal &mdash; {campaign_name}</h1>
<hr>
<p><em>Welcome, adventurer. This journal contains the chronicle of your exploits
throughout the campaign. The epic tales of each session
will be recorded here for posterity.</em></p>
<hr>
""",
    "journal.session_heading": "Session of {date}",
    "journal.date_format": "%m/%d/%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Sync conflict — {filename}",
    "conflict.header": (
        "The file <b>{filename}</b> was modified locally and on Google Drive.\n"
        "Choose which version to keep or merge manually."
    ),
    "conflict.local_label": "Local version",
    "conflict.remote_label": "Remote version (Drive)",
    "conflict.merge_label": "Merged result (editable):",
    "conflict.btn_keep_local": "Keep local version",
    "conflict.btn_keep_remote": "Keep remote version",
    "conflict.btn_save_merge": "Save merge",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Cancel",
    "dialog.btn_ok": "OK",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "Playing\u2026",
    "tts.status.paused": "Paused",
    "tts.hint.pause": "Space: Pause",
    "tts.hint.resume": "Space: Resume",
    "tts.hint.stop": "Esc: Stop",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS not available.",
    "tts.error.generic": "TTS error: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} line{s} folded",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Recording error: {error}",
    "recorder.error.pause": "Pause error: {error}",
    "recorder.error.resume": "Resume error: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Mistral API key not configured. Go to Settings.",
    "transcriber.error.no_api_key_short": "Mistral API key not configured.",
    "transcriber.error.invalid_key": "Invalid API key. Check your key in Settings.",
    "transcriber.error.transcription": "Transcription error: {error}",
    "transcriber.error.live_transcription": "Live transcription error: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Mistral API key not configured.",
    "summarizer.error.generic": "Summary error: {error}",
    "summarizer.no_context": "(First session — no previous context)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Mistral API key not configured.",
    "quest_extractor.error.generic": "Quest extraction error: {error}",
    "quest_extractor.no_quests": "(No quests recorded)",
    "quest_extractor.dialog_title": "Quest update",
    "quest_extractor.dialog_label": "Proposed changes — edit if needed:",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
You are an epic chronicler of the Forgotten Realms, specializing in narrating \
Dungeons & Dragons sessions. You write in {language_name} with a heroic and \
immersive style, worthy of the great chronicles of Faerun.

ABSOLUTE RULE — FIDELITY TO THE TRANSCRIPT:
- DO NOT INVENT any detail not explicitly present in the transcript.
- If information is unclear or absent from the transcript, OMIT IT \
  rather than guessing or inventing.
- DO NOT fabricate dialogue, dice rolls, damage values, DCs, \
  spell names, or encounters not in the transcript.
- Every fact in the summary MUST have a basis in the transcript.
- If you are uncertain about a detail (character class, spell name, \
  numerical value), do not include it or note the uncertainty.

CHARACTER ACTION ATTRIBUTION:
- Audio transcription CANNOT reliably identify who is speaking. \
  DO NOT attribute actions or spells to a specific character unless the \
  character is EXPLICITLY NAMED in dialogue (e.g., "Pryor casts a Smite").
- If the transcript contains speaker markers ([Speaker 0], [Speaker 1], \
  etc.), use them to distinguish speakers, but DO NOT GUESS which \
  character corresponds to which speaker.
- When attribution is uncertain, use impersonal phrasing: \
  "an adventurer", "the party", "one of the heroes", or passive voice.
- For character CLASSES, use ONLY information from the \
  REFERENCE CONTEXT of previous sessions. NEVER deduce a character's class \
  from their actions or spells in this session.
  EXAMPLE — Transcript: "I cast Eldritch Blast. 25, does that hit? Yes. 14 damage."
  GOOD: "An Eldritch Blast strikes the enemy for 14 damage."
  BAD: "Elppa casts Eldritch Blast for 14 damage." \
  (WRONG — we don't know WHO is speaking in audio transcription)

CRUCIAL DISTINCTION — ACTIONS vs REFERENCES:
- Players often discuss PAST events during sessions: \
  recaps, lore reminders, planning based on knowledge \
  from previous sessions. These REFERENCES are NOT \
  new events from this session.
- Only summarize ACTIONS actively occurring during this session: \
  exploration, combat, NPC dialogue, discoveries, decisions made.
- If a player says "remember, the armor glows near dragons" or "last \
  time we fought the dragon", these are REFERENCES — not a \
  dragon fight in this session.
- When in doubt whether an event is happening NOW vs is \
  merely MENTIONED, do not include it as a session event.
- DO NOT DRAW CONCLUSIONS from isolated observations. If a magic \
  item reacts (e.g., armor glowing), report the observation as-is \
  without concluding about the presence or absence of a creature or \
  danger. Facts, not deductions.

General rules:
- Summarize ONLY events present in the NEW TRANSCRIPT. \
  NEVER summarize context from previous sessions.
- Previous context serves only as reference to understand names, \
  places, and intrigues already known. Do not repeat or rephrase it.
- If the transcript contains no content relevant to the D&D campaign, \
  the summary may be shorter to avoid overstating events.
- Write in {language_name}, in an epic narrative style, but NEVER at the cost \
  of accuracy. Style serves narration, not invention.
- Keep ALL D&D terms in English (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, etc.), as well as spell names.
- Proper nouns (characters, places, creatures) remain as-is.
- Ignore off-topic discussions unrelated to the campaign.

Transcript quality:
- The transcript comes from a speech-to-text model that may produce \
  artifacts: repeated phrases, incoherent text, invented words. \
  Completely ignore these parasitic passages and focus only on \
  narrative content relevant to the D&D session.
- CAUTION: some passages may appear narrative but are artifacts. \
  If a passage does not logically integrate with the rest of the session, \
  it is probably an artifact — ignore it.

Format and structure:
- Format your response in HTML with <h3>, <p>, <strong>, <em>, <ul>/<li> tags.
- Return ONLY raw HTML.
- FORBIDDEN: no ```, no ---, no separators, no meta comments.
- Only include sections that contain new content.
- FORMATTING: SIMPLE bullet lists (single level of <ul>/<li>). \
  NEVER nest sub-lists. Keep each point concise on a single line.
- Structure the summary with EXACTLY these sections in this order. \
  Each section starts with an <h3> followed by content. \
  You MUST include ALL sections that have relevant content.

<h3>{section_major_events}</h3>
Chronological narrative of the session's events. \
Describe locations discovered, NPC encounters, and \
findings. Use an immersive and descriptive tone. \
This is the main and longest section of the summary. \
Report OBSERVATIONS as-is, without drawing conclusions \
(e.g., if armor glows, DO NOT conclude a dragon is nearby).

<h3>{section_combat}</h3>
For EACH combat in the session, write a SHORT NARRATIVE PARAGRAPH \
(3-5 sentences) describing: enemies faced, notable moments \
(powerful spells, critical hits, dangers), and the combat outcome. \
DO NOT enumerate each turn or roll individually. \
REMINDER: DO NOT attribute spells or attacks to a named character \
unless the name is EXPLICITLY stated in the transcript. Prefer \
passive voice: "an Eldritch Blast strikes", "a Divine Smite fells". \
If no combat occurred, OMIT this section.

<h3>{section_decisions}</h3>
ONLY the 3-5 most impactful facts for the CAMPAIGN: \
identified magic items (properties AND curses in one sentence), \
major strategic choices, crucial information obtained. \
Format: FLAT list <ul>/<li>, ONE line per item, ZERO sub-lists. \
EXAMPLE of correct format: \
<li><strong>Cursed axe</strong> — +1 attack/damage and +1 HP/level, \
but impossible to abandon, berserk on failed Wisdom Save, disadvantage \
with other weapons.</li>

<h3>{section_mysteries}</h3>
ONLY if an element from this session sheds light on a mystery ALREADY KNOWN \
from the REFERENCE CONTEXT (codex quest, Auril threat, etc.). \
Maximum 2-3 items. \
Format: simple list <ul>/<li>, DECLARATIVE factual sentence. \
FORBIDDEN: rhetorical questions, hypotheses, speculation, verbs like \
"suggests", "seems", "could", "indicates that". \
EXAMPLE — GOOD: "Vassaviken's oath confirms that Grimskal was the \
fief of a frost giant queen leading pillaging campaigns." \
BAD: "The creature's regeneration suggests magic linked to Auril." \
(WRONG — this is speculation, not an observed fact from the transcript) \
If nothing illuminates known intrigues, OMIT this section entirely.
""",
    "prompt.summary_user": """\
REFERENCE CONTEXT (previous sessions — DO NOT summarize, serves only \
to understand characters, places, and intrigues already established):
---
{context}
---

NEW TRANSCRIPT TO SUMMARIZE (summarize ONLY this content):
---
{transcript}
---

Generate an epic, structured summary covering EXCLUSIVELY the new \
events of this transcript. Cover ALL significant events \
from the transcript in chronological order — do not focus on \
a single scene at the expense of others. If the transcript contains \
nothing relevant to the campaign, it is not necessary to add more.
""",
    "prompt.condense": """\
You are an assistant specialized in processing Dungeons & Dragons \
session transcripts.

The transcript comes from a speech-to-text model that produces many \
artifacts: repeated phrases, incoherent text, invented words, \
passages unrelated to the D&D session. Completely ignore these \
parasitic passages.

Condense the text keeping ONLY narrative elements relevant to \
the D&D campaign. Keep D&D terms in English. Respond in {language_name}.

Elements to ABSOLUTELY PRESERVE:
- Names of characters, NPCs, and creatures encountered
- Discovered locations with their physical descriptions
- NPC DIALOGUES: preserve EVERYTHING an NPC reveals (information, \
  directions, warnings, names mentioned, lore). This is critical — \
  information given by NPCs is often the most important of the session.
- Combat: enemies, numerical values (rolls, damage, AC, DC, HP, initiative)
- Magic items: complete properties AND curses
- FAILED actions and their consequences (explosions, damage taken, failures)
- Decisions made by the group and their immediate results

DISTINCTION ACTIONS vs REFERENCES:
- Players often discuss PAST events: recaps of previous sessions, \
  lore reminders, planning. These discussions are NOT events of the \
  current session.
- Only retain ACTIONS actively occurring: location exploration, \
  ongoing combat, dialogues with encountered NPCs, discoveries made, \
  decisions taken.
- If a player MENTIONS a past event (e.g., "remember the dragon", \
  "last time we found..."), it is a REFERENCE — ignore it. \
  Only events that HAPPEN during the session count.
- DO NOT draw conclusions from observations or player discussions. \
  Report ONLY raw facts, never deductions.

IMPORTANT:
- Return ONLY raw narrative facts, in chronological order.
- DO NOT add meta-comments, conclusions, summaries, suggestions, \
  "key takeaways", "next steps", or "open questions".
- DO NOT add separators (---), formatted section titles, or \
  comments about transcript quality.
- Preserve the EXACT character names as heard \
  without modifying or adding question marks.
- Even if the text contains a lot of noise, extract EVERY fragment of \
  D&D content within it, no matter how small. Only return an empty \
  response if the text is 100% artifacts with no coherent game-related sentence.

Text:
{text}
""",
    "prompt.quest_extraction": """\
You are an assistant specialized in quest tracking for a Dungeons & Dragons \
campaign ({campaign_name}).

From the session summary below and the current quest log state, \
generate the COMPLETE recompiled quest log enriched with the new \
session information. The quest log should be a living document that \
reflects the current state of ALL quests.

ABSOLUTE RULE — RETURN ONLY HTML:
- Return ONLY the raw HTML of the quest log, NOTHING else.
- FORBIDDEN: no introduction ("Here is the quest log..."), no conclusion, \
  no notes, no comments, no ```, no ---.
- The document starts with <h1> and ends with </ul>.

Exact HTML structure to produce (all 3 sections MUST be present):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>This register tracks active quests, discovered clues,
and mysteries to unravel throughout the campaign.</em></p>
<hr>
<h2 style="color:#6ab4d4;">{section_active_quests}</h2>
<ul>
<li><strong>Quest name</strong> — General description of the quest.
  <ul>
  <li><em>{quest_origin}:</em> Who gave the quest, where, and when.</li>
  <li><em>{quest_objective}:</em> What must be accomplished.</li>
  <li><em>{quest_progress}:</em> What has been done so far.</li>
  <li><em>{quest_next_step}:</em> What remains to be done.</li>
  <li><em>{quest_npcs}:</em> Characters involved in this quest.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_clues}</h2>
<ul>
<li><strong>Mystery</strong> — What is known, what remains to discover.
  <ul>
  <li>Detail or clue discovered...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_completed_quests}</h2>
<ul>
<li><strong>Quest name</strong> — Resolution and consequences.
  <ul>
  <li><em>{quest_giver}:</em> Who gave the quest and reward.</li>
  <li><em>{quest_resolution}:</em> How the quest was resolved.</li>
  </ul>
</li>
</ul>

Rules:
- Write in {language_name}, concise and FACTUAL style. No speculation (no \
  "could", "seems", "suggests"). Write only what is known.
- Keep D&D terms in English (Hit Points, Saving Throw, etc.).
- Proper nouns remain as-is.
- Use nested bullet lists for details.
- Move resolved quests from "Active Quests" to "Completed Quests".
- PRESERVE ALL existing quest log information. Do not LOSE ANY \
  detail (quest giver, reward, NPCs, progress) from existing quests. \
  Enrich with new information WITHOUT deleting old information.
- Add newly discovered quests to "Active Quests".
- Add new clues to "Clues and Mysteries". Remove a clue \
  when the mystery is resolved (mention the resolution in the related quest).
- The quest log should be a detailed reference tool, not just a list.

Current quest log state:
---
{current_quests}
---

Session summary:
---
{summary}
---
""",
    # ── Prompt section headers (used in prompt placeholders) ─
    "prompt.section.major_events": "Major Events",
    "prompt.section.combat": "Combat",
    "prompt.section.decisions": "Decisions and Discoveries",
    "prompt.section.mysteries": "Mysteries and Clues",
    "prompt.section.active_quests": "Active Quests",
    "prompt.section.clues": "Clues and Mysteries",
    "prompt.section.completed_quests": "Completed Quests",
    "prompt.quest.origin": "Origin",
    "prompt.quest.objective": "Objective",
    "prompt.quest.progress": "Progress",
    "prompt.quest.next_step": "Next step",
    "prompt.quest.npcs": "NPCs involved",
    "prompt.quest.giver": "Quest giver",
    "prompt.quest.resolution": "Resolution",
    "prompt.language_name": "English",
}
