"""French translations — preserves original French UI and AI prompts."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "o",
    "units.kilobytes": "Ko",
    "units.megabytes": "Mo",
    "units.gigabytes": "Go",
    "units.terabytes": "To",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "Fichier",
    "app.menu.settings": "Paramètres...",
    "app.menu.check_updates": "Vérifier les mises à jour...",
    "app.menu.save": "Sauvegarder",
    "app.menu.quit": "Quitter",
    "app.menu.campaign": "Campagne",
    "app.menu.new_campaign": "Nouvelle campagne...",
    "app.menu.delete_campaign": "Supprimer la campagne...",
    "app.menu.restore_campaign": "Restaurer une campagne...",
    "app.menu.theme": "Thème",
    "app.menu.session": "Session",
    "app.menu.record_stop": "Enregistrer / Arrêter",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Journal",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Session",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "Aucune campagne trouvée.",
    "app.campaign.name_label": "Nom de la campagne:",
    "app.campaign.name_placeholder": "Ex: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Créer",
    "app.campaign.delete_title": "Supprimer une campagne",
    "app.campaign.delete_label": "Choisissez la campagne à supprimer :",
    "app.campaign.delete_confirm_title": "Confirmer la suppression",
    "app.campaign.delete_confirm": 'Supprimer la campagne "{name}" ?\nLes fichiers seront déplacés dans campaigns/_trash/.',
    "app.campaign.restore_title": "Restaurer une campagne",
    "app.campaign.restore_label": "Choisissez la campagne à restaurer :",
    "app.campaign.restore_none": "Aucune campagne archivée.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Statut:",
    "app.campaign.drive_not_connected": "Non connecté",
    "app.campaign.drive_connected": "Connecté",
    "app.campaign.drive_btn_login": "Se connecter",
    "app.campaign.drive_logging_in": "Connexion en cours...",
    "app.campaign.drive_folder_id_label": "ID du dossier:",
    "app.campaign.drive_folder_placeholder": "Coller l'ID du dossier partagé...",
    "app.campaign.drive_btn_join": "Rejoindre",
    "app.campaign.drive_join_hint": "(pour rejoindre)",
    "app.campaign.name_empty": "Le nom ne peut pas être vide.",
    "app.campaign.name_exists": 'La campagne "{name}" existe déjà.',
    "app.campaign.drive_paste_id": "Collez l'ID du dossier partagé.",
    "app.campaign.drive_login_first": "Connectez-vous d'abord à Google Drive.",
    "app.campaign.drive_resolving": "Résolution du dossier...",
    "app.campaign.drive_resolve_failed": "Impossible de résoudre le nom du dossier.",
    "app.campaign.drive_deps_missing": "Dépendances Google manquantes.",
    "app.campaign.drive_error": "Erreur Drive: {error}",
    "app.campaign.drive_login_success": "Connecté ! Collez l'ID du dossier et cliquez Rejoindre.",
    "app.campaign.drive_login_failed": "Échec de connexion: {error}",
    "app.campaign.drive_install_deps": (
        "Installez les dépendances Google:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Erreur",
    # ── app.py — theme keyword matching (comma-separated) ──
    "app.theme.kw.icewind_dale": "givre",
    "app.theme.kw.curse_of_strahd": "",
    "app.theme.kw.descent_into_avernus": "averné,enfer",
    "app.theme.kw.tomb_of_annihilation": "tombeau",
    "app.theme.kw.storm_kings_thunder": "géant",
    "app.theme.kw.waterdeep_dragon_heist": "eauprofonde",
    "app.theme.kw.out_of_the_abyss": "abîme,outreterre",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Choisir un thème",
    "app.theme.label": "Aucun thème automatique trouvé pour cette campagne.\nChoisissez un thème visuel:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: désactivé",
    "app.sync.idle": "Drive: synchronisé",
    "app.sync.syncing": "Drive: synchronisation...",
    "app.sync.conflict": "Drive: conflit détecté",
    "app.sync.error": "Drive: erreur",
    "app.sync.offline": "Drive: hors ligne",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Mise à jour",
    "app.update.available_title": "Mise à jour disponible",
    "app.update.version_available": "Version {tag} disponible !",
    "app.update.btn_details": "Détails",
    "app.update.btn_later": "Plus tard",
    "app.update.btn_download": "Télécharger et installer",
    "app.update.no_update": "Vous utilisez la dernière version (v{version}).",
    "app.update.check_error": "Impossible de vérifier les mises à jour.\n{msg}",
    "app.update.downloading": "Téléchargement de la mise à jour...",
    "app.update.download_progress": "Téléchargement... {downloaded} / {total}",
    "app.update.download_progress_unknown": "Téléchargement... {downloaded}",
    "app.update.download_done": (
        "Téléchargement terminé.\n" "L'application va se fermer pour installer la mise à jour.\n\n" "Continuer ?"
    ),
    "app.update.download_error": "Erreur lors du téléchargement.\n{msg}",
    "app.update.btn_cancel": "Annuler",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Bienvenue — DnD Logger",
    "wizard.welcome": "Bienvenue dans DnD Logger",
    "wizard.subtitle": "Votre compagnon de session D&D.\nConfigurons les éléments essentiels pour commencer.",
    "wizard.api_group": "Clé API Mistral",
    "wizard.api_placeholder": "Entrez votre clé API Mistral...",
    "wizard.api_hint": "Obtenez une clé sur console.mistral.ai",
    "wizard.mic_group": "Microphone",
    "wizard.mic_device_label": "Périphérique:",
    "wizard.btn_skip": "Configurer plus tard",
    "wizard.btn_done": "Commencer l'aventure !",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Paramètres — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Audio",
    "settings.tab.advanced": "Avancé",
    "settings.tab.prompts": "Prompts",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Clé API Mistral:",
    "settings.api.key_placeholder": "Entrez votre cle API Mistral...",
    "settings.api.btn_test": "Tester la connexion",
    "settings.api.enter_key_first": "Entrez une clé API d'abord.",
    "settings.api.test_success": "Connexion réussie !",
    "settings.api.test_fail": "Échec: {error}",
    "settings.api.model_label": "Modèle de résumé:",
    "settings.audio.device_label": "Périphérique d'entrée:",
    "settings.audio.device_default": "Défaut (automatique)",
    "settings.audio.btn_test_mic": "Tester le microphone",
    "settings.audio.sample_rate_label": "Fréquence d'échantillonnage:",
    "settings.audio.test_ok": "Microphone fonctionne ! (niveau: {level})",
    "settings.audio.test_weak": "Signal très faible. Vérifiez votre microphone.",
    "settings.audio.test_error": "Erreur: {error}",
    "settings.audio.test_title": "Test Microphone",
    "settings.advanced.auto_update": "Vérifier les mises à jour au démarrage",
    "settings.advanced.chunk_label": "Durée max par chunk:",
    "settings.advanced.bias_label": "Biais de contexte D&D:",
    "settings.advanced.bias_placeholder": "Termes D&D (un par ligne)...",
    "settings.advanced.language_label": "Langue:",
    "settings.advanced.restart_required": "La langue a été modifiée. Veuillez redémarrer l'application.",
    "settings.advanced.restart_title": "Redémarrage nécessaire",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Réinitialiser ce prompt",
    "settings.prompts.summary_system_label": "Résumé de session (system)",
    "settings.prompts.condense_label": "Condensation (texte long)",
    "settings.prompts.quest_extraction_label": "Extraction de quêtes",
    "settings.prompts.hint.summary_system": "Variables: aucune (prompt système fixe)",
    "settings.prompts.hint.condense": "Variables: {text}",
    "settings.prompts.hint.quest_extraction": "Variables: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Compte Google",
    "settings.drive.status_label": "Statut:",
    "settings.drive.not_connected": "Non connecté",
    "settings.drive.connected": "Connecté",
    "settings.drive.deps_missing": "Dépendances Google manquantes",
    "settings.drive.btn_login": "Se connecter",
    "settings.drive.btn_logout": "Se déconnecter",
    "settings.drive.logging_in": "Connexion en cours...",
    "settings.drive.login_failed_title": "Échec de connexion",
    "settings.drive.login_failed": "Erreur: {error}",
    "settings.drive.campaign_sync_group": "Synchronisation de campagne",
    "settings.drive.active_campaign_label": "Campagne active:",
    "settings.drive.join_placeholder": "Coller l'ID du dossier partagé...",
    "settings.drive.join_hint": "(pour rejoindre)",
    "settings.drive.folder_id_label": "ID du dossier:",
    "settings.drive.no_folder": "Aucun dossier créé",
    "settings.drive.creating_folder": "Création du dossier...",
    "settings.drive.btn_copy": "Copier",
    "settings.drive.sync_checkbox": "Activer la synchronisation Google Drive",
    "settings.drive.folder_error": "Impossible de créer le dossier: {error}",
    "settings.drive.not_connected_error": "Non connecté à Google Drive",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Enregistrer",
    "session.btn.stop": "Arrêter",
    "session.btn.pause": "Pause",
    "session.btn.resume": "Reprendre",
    "session.status.ready": "Prêt à enregistrer",
    "session.status.recording": "Enregistrement en cours...",
    "session.status.paused": "Enregistrement en pause",
    "session.status.stopped": "Enregistrement terminé",
    "session.status.finalizing": "Finalisation de la transcription...",
    "session.status.ready_rerecord": "Prêt à re-enregistrer",
    "session.status.saved": "Enregistrement sauvegardé",
    "session.status.transcribing": "Transcription en cours...",
    "session.status.transcribing_chunk": "Transcription: chunk {current}/{total}...",
    "session.status.transcribing_segment": "Transcription du segment {count}...",
    "session.status.transcription_done": "Transcription terminée.",
    "session.status.summarizing": "Génération du résumé...",
    "session.status.no_text": "Aucun texte transcrit.",
    "session.status.summary_done": "Resumé généré !",
    "session.status.copied": "Resumé copié dans le presse-papiers !",
    "session.status.added_journal": "Resumé ajouté au Journal !",
    "session.status.quest_extracting": "Extraction des quêtes en cours...",
    "session.status.quest_ready": "Propositions de quêtes prêtes.",
    "session.status.quest_updated": "Quêtes mises a jour !",
    "session.status.quest_cancelled": "Mise a jour des quêtes annulée.",
    "session.status.imported": "Audio importé: {name} ({size})",
    "session.status.audio_saved": "Audio sauvegardé: {name}",
    "session.status.segments_transcribed": "Enregistrement... ({count} segment{s} transcrit{s})",
    "session.status.transcription_error": "Erreur transcription: {msg}",
    "session.label.transcription": "Transcription",
    "session.label.summary": "Resumé Épique",
    "session.placeholder.transcript": "La transcription apparaitra ici après l'enregistrement...",
    "session.placeholder.summary": "Le resumé épique apparaitra ici...",
    "session.btn.transcribe": "Transcrire",
    "session.btn.summarize": "Résumer",
    "session.btn.add_journal": "Ajouter au Journal",
    "session.btn.update_quests": "Mettre à jour les Quêtes",
    "session.btn.tts_tooltip": "Lire le resumé à voix haute",
    "session.btn.tts_no_voice": "Aucune voix française disponible",
    "session.btn.more_tooltip": "Plus d'options",
    "session.menu.import_audio": "Importer un audio",
    "session.menu.save_audio": "Sauvegarder l'audio",
    "session.menu.copy_summary": "Copier le resumé",
    "session.tts.read_selection": "Lire la sélection",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Enregistrement terminé",
    "session.post.btn_transcribe": "Transcrire",
    "session.post.btn_rerecord": "Re-enregistrer",
    "session.post.btn_save_only": "Sauvegarder sans transcrire",
    "session.post.duration": "Durée:",
    "session.post.size": "Taille:",
    "session.post.file": "Fichier:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Journal (récits précédents) ===",
    "session.context.quest_header": "=== Quest Log (quêtes actives) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Importer un fichier audio",
    "session.dialog.import_filter": "Fichiers audio (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Tous (*)",
    "session.dialog.save_title": "Sauvegarder le fichier audio",
    "session.dialog.save_filter": "FLAC (*.flac);;Tous (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "Aucun fichier audio trouvé.",
    "session.error.no_audio_save": "Aucun fichier audio à sauvegarder.",
    "session.error.copy_failed": "Erreur lors de la copie: {error}",
    "session.error.flac_failed": "Erreur de conversion FLAC: {error}",
    "session.error.save_failed": "Erreur de sauvegarde: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Gras (Ctrl+B)",
    "editor.tooltip.italic": "Italique (Ctrl+I)",
    "editor.tooltip.underline": "Souligner (Ctrl+U)",
    "editor.tooltip.fold_all": "Replier tout (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Déplier tout (Ctrl+Shift+=)",
    "editor.btn.save": " Sauvegarder",
    "editor.heading.normal": "Normal",
    "editor.heading.h1": "Titre 1",
    "editor.heading.h2": "Titre 2",
    "editor.heading.h3": "Titre 3",
    "editor.search.placeholder": "Rechercher\u2026",
    "editor.search.no_results": "0 résultat",
    "editor.search.prev_tooltip": "Précédent (Shift+Enter)",
    "editor.search.next_tooltip": "Suivant (Enter)",
    "editor.search.close_tooltip": "Fermer (Échap)",
    "editor.tts.read_selection": "Lire la selection",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères à élucider au cours de la campagne.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quêtes Actives</h2>
<ul>
<li><em>Aucune quête enregistrée pour le moment.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Indices et Mystères</h2>
<ul>
<li><em>Aucun indice pour le moment.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Quêtes Terminées</h2>
<ul>
<li><em>Aucune quête terminée.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Journal &mdash; {campaign_name}</h1>
<hr>
<p><em>Bienvenue, aventurier. Ce journal contient la chronique de vos exploits
au cours de la campagne. Les récits épiques de chaque session
seront consignés ici pour la postérité.</em></p>
<hr>
""",
    "journal.session_heading": "Session du {date}",
    "journal.date_format": "%d/%m/%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Conflit de synchronisation — {filename}",
    "conflict.header": (
        "Le fichier <b>{filename}</b> a été modifié localement et sur Google Drive.\n"
        "Choisissez quelle version garder ou fusionnez manuellement."
    ),
    "conflict.local_label": "Version locale",
    "conflict.remote_label": "Version distante (Drive)",
    "conflict.merge_label": "Résultat fusionné (modifiable):",
    "conflict.btn_keep_local": "Garder la version locale",
    "conflict.btn_keep_remote": "Garder la version distante",
    "conflict.btn_save_merge": "Sauvegarder la fusion",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Annuler",
    "dialog.btn_ok": "OK",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "Lecture en cours\u2026",
    "tts.status.paused": "En pause",
    "tts.hint.pause": "Espace : Pause",
    "tts.hint.resume": "Espace : Reprendre",
    "tts.hint.stop": "\u00c9chap : Arr\u00eater",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS non disponible.",
    "tts.error.generic": "Erreur TTS: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} ligne{s} repliée{s}",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Erreur d'enregistrement: {error}",
    "recorder.error.pause": "Erreur de pause: {error}",
    "recorder.error.resume": "Erreur de reprise: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Clé API Mistral non configurée. Allez dans Paramètres.",
    "transcriber.error.no_api_key_short": "Clé API Mistral non configurée.",
    "transcriber.error.invalid_key": "Clé API invalide. Verifiez votre clé dans les Paramètres.",
    "transcriber.error.transcription": "Erreur de transcription: {error}",
    "transcriber.error.live_transcription": "Erreur de transcription live: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Clé API Mistral non configurée.",
    "summarizer.error.generic": "Erreur de résumé: {error}",
    "summarizer.no_context": "(Première session — pas de contexte précédent)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Clé API Mistral non configurée.",
    "quest_extractor.error.generic": "Erreur d'extraction de quêtes: {error}",
    "quest_extractor.no_quests": "(Aucune quête enregistrée)",
    "quest_extractor.dialog_title": "Mise à jour des quêtes",
    "quest_extractor.dialog_label": "Changements proposés — modifiez si nécessaire:",
    # ── updater.py ─────────────────────────────────────────
    "updater.error.no_installer": "Aucun installateur trouvé dans cette release.",
    "updater.error.network": "Erreur réseau : {reason}",
    # ── drive_sync.py ─────────────────────────────────────
    "drive.error.init": "Erreur d'initialisation Drive: {error}",
    "drive.error.session_expired": "Session Drive expirée. Reconnectez-vous dans les paramètres.",
    "drive.error.upload": "Erreur d'upload ({filename}): {error}",
    "drive.error.download": "Erreur de téléchargement ({filename}): {error}",
    # ── web_panel.py ──────────────────────────────────────
    "browser.tooltip.back": "Retour",
    "browser.tooltip.forward": "Suivant",
    "browser.tooltip.refresh": "Rafraichir",
    "browser.tooltip.home": "Accueil D&D Beyond",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
Tu es un chroniqueur épique des Royaumes Oubliés, specialisé dans la narration \
de sessions de Dungeons & Dragons. Tu écris en français avec un style héroïque \
et immersif, digne des grandes chroniques de Faerun.

RÈGLE ABSOLUE — FIDÉLITÉ À LA TRANSCRIPTION:
- N'INVENTE AUCUN détail qui n'est pas explicitement présent dans la transcription.
- Si une information n'est pas claire ou absente de la transcription, OMETS-LA \
  plutôt que de la deviner ou de l'inventer.
- Ne fabrique PAS de dialogue, de jets de dés, de valeurs de dégâts, de DC, \
  de noms de sorts, ou de rencontres qui ne sont pas dans la transcription.
- Chaque fait mentionné dans le résumé DOIT avoir une base dans la transcription.
- Si tu n'es pas certain d'un détail (classe d'un personnage, nom d'un sort, \
  valeur numérique), ne l'inclus pas ou signale l'incertitude.

ATTRIBUTION DES ACTIONS AUX PERSONNAGES:
- La transcription audio ne permet PAS d'identifier de manière fiable qui parle. \
  N'ATTRIBUE PAS d'actions ou de sorts à un personnage spécifique sauf si le \
  personnage est NOMMÉ EXPLICITEMENT dans le dialogue (ex: "Pryor lance un Smite").
- Si la transcription contient des marqueurs de locuteur ([Speaker 0], [Speaker 1], \
  etc.), utilise-les pour distinguer les interlocuteurs, mais NE DEVINE PAS quel \
  personnage correspond à quel locuteur.
- Quand l'attribution est incertaine, utilise des formulations impersonnelles : \
  "un aventurier", "le groupe", "l'un des héros", ou la voix passive.
- Pour les CLASSES des personnages, utilise UNIQUEMENT les informations du \
  CONTEXTE DE RÉFÉRENCE des sessions précédentes. Ne déduis JAMAIS la classe \
  d'un personnage à partir de ses actions ou sorts dans cette session.
  EXEMPLE — Transcription: "Je lance Eldritch Blast. 25, ça touche? Oui. 14 dégâts."
  BON: "Un Eldritch Blast frappe l'ennemi pour 14 dégâts."
  MAUVAIS: "Elppa lance un Eldritch Blast pour 14 dégâts." \
  (FAUX — on ne sait pas QUI parle dans la transcription audio)

DISTINCTION CRUCIALE — ACTIONS vs RÉFÉRENCES:
- Les joueurs discutent souvent d'évènements PASSÉS pendant la session : \
  récapitulatifs, rappels de lore, planification basée sur des connaissances \
  acquises lors de sessions précédentes. Ces RÉFÉRENCES ne sont PAS des \
  évènements nouveaux de cette session.
- Ne résume QUE les ACTIONS qui se déroulent activement pendant cette session : \
  exploration, combats, dialogues avec des PNJ, découvertes, décisions prises.
- Si un joueur dit "rappelle-toi, l'armure brille près des dragons" ou "la \
  dernière fois on a combattu le dragon", ce sont des RÉFÉRENCES — pas un \
  combat de dragon dans cette session.
- En cas de doute sur le fait qu'un évènement se produit MAINTENANT vs est \
  simplement MENTIONNÉ, ne l'inclus pas comme évènement de la session.
- NE TIRE PAS DE CONCLUSIONS à partir d'observations isolées. Si un objet \
  magique réagit (ex: une armure qui brille), rapporte l'observation telle \
  quelle, sans conclure sur la présence ou l'absence d'une créature ou d'un \
  danger. Les faits, pas les déductions.

Règles générales:
- Résume UNIQUEMENT les évènements présents dans la NOUVELLE TRANSCRIPTION. \
  Ne résume JAMAIS le contexte des sessions précédentes.
- Le contexte précédent sert uniquement de référence pour comprendre les noms, \
  lieux et intrigues déjà connus. Ne le répète pas, ne le reformule pas.
- Si la transcription ne contient aucun contenu pertinent à la campagne D&D, \
  le résumé peut être plus court pour ne pas exagérer les évènements.
- Écris en français, dans un style épique et narratif, mais JAMAIS au prix \
  de l'exactitude. Le style sert la narration, pas l'invention.
- Conserve TOUS les termes D&D en anglais (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, etc.), ainsi que les noms des sorts.
- Les noms propres (personnages, lieux, créatures) restent tels quels.
- Ignore les discussions hors-sujet sans lien avec la campagne.

Qualité de la transcription:
- La transcription provient d'un modèle speech-to-text qui peut produire des \
  artefacts : phrases répétées en boucle, texte incohérent, mots inventés. \
  Ignore complètement ces passages parasites et concentre-toi uniquement sur \
  le contenu narratif pertinent à la session D&D.
- ATTENTION : certains passages peuvent sembler narratifs mais être des artefacts. \
  Si un passage ne s'intègre pas logiquement avec le reste de la session, \
  c'est probablement un artefact — ignore-le.

Format et structure:
- Formate ta réponse en HTML avec des balises <h3>, <p>, <strong>, <em>, <ul>/<li>.
- Retourne UNIQUEMENT le HTML brut.
- INTERDIT: pas de ```, pas de ---, pas de séparateurs, pas de commentaires méta.
- N'inclus que les sections qui contiennent du contenu nouveau.
- MISE EN FORME : listes à puces SIMPLES (un seul niveau de <ul>/<li>). \
  N'imbrique JAMAIS de sous-listes. Garde chaque point concis sur une seule ligne.
- Structure le résumé avec EXACTEMENT ces sections dans cet ordre. \
  Chaque section commence par un <h3> suivi du contenu. \
  Tu DOIS inclure TOUTES les sections qui ont du contenu pertinent.

<h3>Évènements majeurs</h3>
Récit narratif et chronologique des évènements de la session. \
Décris les lieux découverts, les rencontres avec les PNJ, et les \
découvertes. Utilise un ton immersif et descriptif. \
C'est la section principale et la plus longue du résumé. \
Rapporte les OBSERVATIONS telles quelles, sans en tirer de conclusions \
(ex: si une armure brille, ne conclus PAS qu'un dragon est proche).

<h3>Combats</h3>
Pour CHAQUE combat de la session, écris un COURT PARAGRAPHE NARRATIF \
(3-5 phrases) décrivant : les ennemis affrontés, les moments marquants \
(sorts puissants, coups critiques, dangers), et l'issue du combat. \
N'énumère PAS chaque tour ou jet individuellement. \
RAPPEL: n'attribue PAS les sorts ou attaques à un personnage nommé \
sauf si le nom est EXPLICITEMENT dit dans la transcription. Préfère \
la voix passive : "un Eldritch Blast frappe", "un Divine Smite terrasse". \
Si aucun combat n'a eu lieu, OMETS cette section.

<h3>Décisions et découvertes</h3>
SEULEMENT les 3-5 faits les plus impactants pour la CAMPAGNE : \
objets magiques identifiés (propriétés ET malédictions en une phrase), \
choix stratégiques majeurs, informations cruciales obtenues. \
Format: liste PLATE <ul>/<li>, UNE ligne par élément, ZÉRO sous-liste. \
EXEMPLE de format correct: \
<li><strong>Hache maudite</strong> — +1 attaque/dégâts et +1 PV/niveau, \
mais impossible à abandonner, berserk sur Wisdom Save raté, désavantage \
avec d'autres armes.</li>

<h3>Mystères et indices</h3>
SEULEMENT si un élément de cette session éclaire un mystère DÉJÀ CONNU \
du CONTEXTE DE RÉFÉRENCE (quête du codex, menace d'Auril, etc.). \
Maximum 2-3 éléments. \
Format: liste simple <ul>/<li>, phrase DÉCLARATIVE factuelle. \
INTERDIT: questions rhétoriques, hypothèses, spéculations, verbes comme \
"suggère", "semble", "pourrait", "indique que". \
EXEMPLE — BON: "Le serment de Vassaviken confirme que Grimskal fut le \
fief d'une reine des géants des glaces menant des campagnes de pillage." \
MAUVAIS: "La régénération de la créature suggère une magie liée à Auril." \
(FAUX — c'est une spéculation, pas un fait observé dans la transcription) \
Si rien n'éclaire les intrigues connues, OMETS cette section entièrement.
""",
    "prompt.summary_user": """\
CONTEXTE DE RÉFÉRENCE (sessions précédentes — NE PAS résumer, sert uniquement \
à comprendre les personnages, lieux et intrigues déjà établis):
---
{context}
---

NOUVELLE TRANSCRIPTION À RÉSUMER (résume UNIQUEMENT ce contenu-ci):
---
{transcript}
---

Génère un résumé épique et structuré portant EXCLUSIVEMENT sur les nouveaux \
évènements de cette transcription. Couvre TOUS les évènements significatifs \
de la transcription dans l'ordre chronologique — ne te concentre pas sur \
une seule scène au détriment des autres. Si la transcription ne contient \
rien de pertinent à la campagne, il n'est pas nécessaire d'en ajouter plus.
""",
    "prompt.condense": """\
Tu es un assistant spécialisé dans le traitement de transcriptions de sessions \
de Dungeons & Dragons.

La transcription provient d'un modèle speech-to-text qui produit de nombreux \
artefacts : phrases répétées en boucle, texte incohérent, mots inventés, \
passages sans rapport avec la session D&D. Ignore complètement ces passages \
parasites.

Condense le texte en gardant UNIQUEMENT les éléments narratifs pertinents à \
la campagne D&D. Conserve les termes D&D en anglais. Réponds en français.

Éléments à PRÉSERVER ABSOLUMENT:
- Noms des personnages, PNJ et créatures rencontrées
- Lieux découverts avec leurs descriptions physiques
- DIALOGUES AVEC LES PNJ : conserve TOUT ce qu'un PNJ révèle (informations, \
  directions, avertissements, noms mentionnés, lore). C'est critique — les \
  informations données par les PNJ sont souvent les plus importantes de la session.
- Combats : ennemis, valeurs numériques (jets, dégâts, AC, DC, HP, initiative)
- Objets magiques : propriétés complètes ET malédictions
- Actions RATÉES et leurs conséquences (explosions, dégâts subis, échecs)
- Décisions prises par le groupe et leurs résultats immédiats

DISTINCTION ACTIONS vs RÉFÉRENCES:
- Les joueurs discutent souvent d'évènements PASSÉS : récapitulatifs de sessions \
  précédentes, rappels de lore, planification. Ces discussions ne sont PAS des \
  évènements de la session en cours.
- Ne retiens QUE les ACTIONS qui se déroulent activement : exploration de lieux, \
  combats en cours, dialogues avec des PNJ rencontrés, découvertes faites, \
  décisions prises.
- Si un joueur MENTIONNE un évènement passé (ex: "rappelle-toi le dragon", \
  "la dernière fois on a trouvé..."), c'est une RÉFÉRENCE — ignore-la. \
  Seuls les évènements qui SE PRODUISENT pendant la session comptent.
- Ne tire PAS de conclusions à partir d'observations ou de discussions \
  entre joueurs. Rapporte UNIQUEMENT les faits bruts, jamais les déductions.

IMPORTANT:
- Retourne UNIQUEMENT les faits narratifs bruts, dans l'ordre chronologique.
- N'ajoute PAS de méta-commentaires, conclusions, résumés, suggestions, \
  "points clés à retenir", "prochaines étapes" ou "questions en suspens".
- N'ajoute PAS de séparateurs (---), de titres de section formatés, ni de \
  commentaires sur la qualité de la transcription.
- Préserve les NOMS EXACTS des personnages tels qu'entendus \
  sans les modifier ni ajouter de points d'interrogation.
- Même si le texte contient beaucoup de bruit, extrais TOUT fragment de \
  contenu D&D qui s'y trouve, aussi petit soit-il. Ne retourne une réponse \
  vide que si le texte est à 100% des artefacts sans aucune phrase cohérente \
  liée au jeu.

Texte:
{text}
""",
    "prompt.quest_extraction": """\
Tu es un assistant spécialisé dans le suivi de quêtes pour une campagne \
Dungeons & Dragons ({campaign_name}).

À partir du résumé de session ci-dessous et de l'état actuel du quest log, \
génère le quest log COMPLET recompilé et enrichi avec les nouvelles \
informations de la session. Le quest log doit être un document vivant qui \
reflète l'état actuel de TOUTES les quêtes.

RÈGLE ABSOLUE — RETOURNE UNIQUEMENT LE HTML:
- Retourne UNIQUEMENT le HTML brut du quest log, RIEN d'autre.
- INTERDIT: pas d'introduction ("Voici le quest log..."), pas de conclusion, \
  pas de notes, pas de commentaires, pas de ```, pas de ---.
- Le document commence par <h1> et finit par </ul>.

Structure HTML exacte à produire (les 3 sections DOIVENT être présentes):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Ce registre recense les quêtes actives, indices découverts
et mystères à élucider au cours de la campagne.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quêtes Actives</h2>
<ul>
<li><strong>Nom de la quête</strong> — Description générale de la quête.
  <ul>
  <li><em>Origine:</em> Qui a donné la quête, où et quand.</li>
  <li><em>Objectif:</em> Ce qui doit être accompli.</li>
  <li><em>Progression:</em> Ce qui a été fait jusqu'ici.</li>
  <li><em>Prochaine étape:</em> Ce qu'il reste à faire.</li>
  <li><em>PNJ impliqués:</em> Personnages liés à cette quête.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">Indices et Mystères</h2>
<ul>
<li><strong>Mystère</strong> — Ce qu'on sait, ce qui reste à découvrir.
  <ul>
  <li>Détail ou indice découvert...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">Quêtes Terminées</h2>
<ul>
<li><strong>Nom de la quête</strong> — Résolution et conséquences.
  <ul>
  <li><em>Mandataire:</em> Qui a donné la quête et récompense.</li>
  <li><em>Résolution:</em> Comment la quête a été résolue.</li>
  </ul>
</li>
</ul>

Règles:
- Écris en français, style concis et FACTUEL. Pas de spéculation (pas de \
  "pourrait", "semble", "suggère"). Écris uniquement ce qui est connu.
- Conserve les termes D&D en anglais (Hit Points, Saving Throw, etc.).
- Les noms propres restent tels quels.
- Utilise des listes à puces imbriquées pour les détails.
- Déplace les quêtes résolues de "Quêtes Actives" vers "Quêtes Terminées".
- PRÉSERVE TOUTES les informations existantes du quest log. Ne perds AUCUN \
  détail (mandataire, récompense, PNJ, progression) des quêtes existantes. \
  Enrichis avec les nouvelles informations SANS supprimer les anciennes.
- Ajoute les nouvelles quêtes découvertes dans "Quêtes Actives".
- Ajoute les nouveaux indices dans "Indices et Mystères". Retire un indice \
  quand le mystère est résolu (mentionne la résolution dans la quête concernée).
- Le quest log doit être un outil de référence détaillé, pas juste une liste.

État actuel du quest log:
---
{current_quests}
---

Résumé de la session:
---
{summary}
---
""",
    # ── Prompt section headers ──────────────────────────────
    "prompt.section.major_events": "Évènements majeurs",
    "prompt.section.combat": "Combats",
    "prompt.section.decisions": "Décisions et découvertes",
    "prompt.section.mysteries": "Mystères et indices",
    "prompt.section.active_quests": "Quêtes Actives",
    "prompt.section.clues": "Indices et Mystères",
    "prompt.section.completed_quests": "Quêtes Terminées",
    "prompt.quest.origin": "Origine",
    "prompt.quest.objective": "Objectif",
    "prompt.quest.progress": "Progression",
    "prompt.quest.next_step": "Prochaine étape",
    "prompt.quest.npcs": "PNJ impliqués",
    "prompt.quest.giver": "Mandataire",
    "prompt.quest.resolution": "Résolution",
    "prompt.language_name": "français",
}
