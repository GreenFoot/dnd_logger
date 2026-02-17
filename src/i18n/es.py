"""Spanish translations — traducción al español de la interfaz y prompts de IA."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "B",
    "units.kilobytes": "KB",
    "units.megabytes": "MB",
    "units.gigabytes": "GB",
    "units.terabytes": "TB",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "Archivo",
    "app.menu.settings": "Configuración...",
    "app.menu.check_updates": "Buscar actualizaciones...",
    "app.menu.save": "Guardar",
    "app.menu.quit": "Salir",
    "app.menu.campaign": "Campaña",
    "app.menu.new_campaign": "Nueva campaña...",
    "app.menu.delete_campaign": "Eliminar campaña...",
    "app.menu.restore_campaign": "Restaurar una campaña...",
    "app.menu.theme": "Tema",
    "app.menu.session": "Sesión",
    "app.menu.record_stop": "Grabar / Detener",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Diario",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Sesión",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "No se encontraron campañas.",
    "app.campaign.name_label": "Nombre de la campaña:",
    "app.campaign.name_placeholder": "Ej.: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Crear",
    "app.campaign.delete_title": "Eliminar una campaña",
    "app.campaign.delete_label": "Elige la campaña a eliminar:",
    "app.campaign.delete_confirm_title": "Confirmar eliminación",
    "app.campaign.delete_confirm": 'Eliminar la campaña "{name}"?\nLos archivos se moverán a campaigns/_trash/.',
    "app.campaign.restore_title": "Restaurar una campaña",
    "app.campaign.restore_label": "Elige la campaña a restaurar:",
    "app.campaign.restore_none": "No hay campañas archivadas.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Estado:",
    "app.campaign.drive_not_connected": "No conectado",
    "app.campaign.drive_connected": "Conectado",
    "app.campaign.drive_btn_login": "Iniciar sesión",
    "app.campaign.drive_logging_in": "Conectando...",
    "app.campaign.drive_folder_id_label": "ID de la carpeta:",
    "app.campaign.drive_folder_placeholder": "Pega el ID de la carpeta compartida...",
    "app.campaign.drive_btn_join": "Unirse",
    "app.campaign.drive_join_hint": "(para unirse)",
    "app.campaign.name_empty": "El nombre no puede estar vacío.",
    "app.campaign.name_exists": 'La campaña "{name}" ya existe.',
    "app.campaign.drive_paste_id": "Pega el ID de la carpeta compartida.",
    "app.campaign.drive_login_first": "Inicia sesión en Google Drive primero.",
    "app.campaign.drive_resolving": "Resolviendo carpeta...",
    "app.campaign.drive_resolve_failed": "No se pudo resolver el nombre de la carpeta.",
    "app.campaign.drive_deps_missing": "Faltan dependencias de Google.",
    "app.campaign.drive_error": "Error de Drive: {error}",
    "app.campaign.drive_login_success": "¡Conectado! Pega el ID de la carpeta y haz clic en Unirse.",
    "app.campaign.drive_login_failed": "Error de conexión: {error}",
    "app.campaign.drive_install_deps": (
        "Instala las dependencias de Google:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Error",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Elegir un tema",
    "app.theme.label": "No se encontró un tema automático para esta campaña.\nElige un tema visual:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: desactivado",
    "app.sync.idle": "Drive: sincronizado",
    "app.sync.syncing": "Drive: sincronizando...",
    "app.sync.conflict": "Drive: conflicto detectado",
    "app.sync.error": "Drive: error",
    "app.sync.offline": "Drive: sin conexión",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Actualización",
    "app.update.available_title": "Actualización disponible",
    "app.update.version_available": "¡Versión {tag} disponible!",
    "app.update.btn_details": "Detalles",
    "app.update.btn_later": "Más tarde",
    "app.update.btn_download": "Descargar e instalar",
    "app.update.no_update": "Estás usando la última versión (v{version}).",
    "app.update.check_error": "No se pudo verificar las actualizaciones.\n{msg}",
    "app.update.downloading": "Descargando actualización...",
    "app.update.download_progress": "Descargando... {downloaded} / {total}",
    "app.update.download_progress_unknown": "Descargando... {downloaded}",
    "app.update.download_done": (
        "Descarga completada.\n" "La aplicación se cerrará para instalar la actualización.\n\n" "¿Continuar?"
    ),
    "app.update.download_error": "Error durante la descarga.\n{msg}",
    "app.update.btn_cancel": "Cancelar",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Bienvenido — DnD Logger",
    "wizard.welcome": "Bienvenido a DnD Logger",
    "wizard.subtitle": "Tu compañero de sesiones de D&D.\nConfiguremos lo esencial para comenzar.",
    "wizard.api_group": "Clave API de Mistral",
    "wizard.api_placeholder": "Introduce tu clave API de Mistral...",
    "wizard.api_hint": "Obtén una clave en console.mistral.ai",
    "wizard.mic_group": "Micrófono",
    "wizard.mic_device_label": "Dispositivo:",
    "wizard.btn_skip": "Configurar más tarde",
    "wizard.btn_done": "¡Comenzar la aventura!",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Configuración — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Audio",
    "settings.tab.advanced": "Avanzado",
    "settings.tab.prompts": "Prompts",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Clave API de Mistral:",
    "settings.api.key_placeholder": "Introduce tu clave API de Mistral...",
    "settings.api.btn_test": "Probar conexión",
    "settings.api.enter_key_first": "Introduce una clave API primero.",
    "settings.api.test_success": "¡Conexión exitosa!",
    "settings.api.test_fail": "Error: {error}",
    "settings.api.model_label": "Modelo de resumen:",
    "settings.audio.device_label": "Dispositivo de entrada:",
    "settings.audio.device_default": "Predeterminado (automático)",
    "settings.audio.btn_test_mic": "Probar micrófono",
    "settings.audio.sample_rate_label": "Frecuencia de muestreo:",
    "settings.audio.test_ok": "¡El micrófono funciona! (nivel: {level})",
    "settings.audio.test_weak": "Señal muy débil. Verifica tu micrófono.",
    "settings.audio.test_error": "Error: {error}",
    "settings.audio.test_title": "Prueba de micrófono",
    "settings.advanced.auto_update": "Buscar actualizaciones al iniciar",
    "settings.advanced.chunk_label": "Duración máxima por chunk:",
    "settings.advanced.bias_label": "Sesgo de contexto D&D:",
    "settings.advanced.bias_placeholder": "Términos D&D (uno por línea)...",
    "settings.advanced.language_label": "Idioma:",
    "settings.advanced.restart_required": "El idioma ha sido cambiado. Por favor reinicia la aplicación.",
    "settings.advanced.restart_title": "Reinicio necesario",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Restablecer este prompt",
    "settings.prompts.summary_system_label": "Resumen de sesión (system)",
    "settings.prompts.condense_label": "Condensación (texto largo)",
    "settings.prompts.quest_extraction_label": "Extracción de quests",
    "settings.prompts.hint.summary_system": "Variables: ninguna (prompt de sistema fijo)",
    "settings.prompts.hint.condense": "Variables: {text}",
    "settings.prompts.hint.quest_extraction": "Variables: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Cuenta de Google",
    "settings.drive.status_label": "Estado:",
    "settings.drive.not_connected": "No conectado",
    "settings.drive.connected": "Conectado",
    "settings.drive.deps_missing": "Faltan dependencias de Google",
    "settings.drive.btn_login": "Iniciar sesión",
    "settings.drive.btn_logout": "Cerrar sesión",
    "settings.drive.logging_in": "Conectando...",
    "settings.drive.login_failed_title": "Error de conexión",
    "settings.drive.login_failed": "Error: {error}",
    "settings.drive.campaign_sync_group": "Sincronización de campaña",
    "settings.drive.active_campaign_label": "Campaña activa:",
    "settings.drive.join_placeholder": "Pega el ID de la carpeta compartida...",
    "settings.drive.join_hint": "(para unirse)",
    "settings.drive.folder_id_label": "ID de la carpeta:",
    "settings.drive.no_folder": "No se ha creado ninguna carpeta",
    "settings.drive.creating_folder": "Creando carpeta...",
    "settings.drive.btn_copy": "Copiar",
    "settings.drive.sync_checkbox": "Activar sincronización con Google Drive",
    "settings.drive.folder_error": "No se pudo crear la carpeta: {error}",
    "settings.drive.not_connected_error": "No conectado a Google Drive",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Grabar",
    "session.btn.stop": "Detener",
    "session.btn.pause": "Pausar",
    "session.btn.resume": "Reanudar",
    "session.status.ready": "Listo para grabar",
    "session.status.recording": "Grabando...",
    "session.status.paused": "Grabación en pausa",
    "session.status.stopped": "Grabación detenida",
    "session.status.finalizing": "Finalizando transcripción...",
    "session.status.ready_rerecord": "Listo para regrabar",
    "session.status.saved": "Grabación guardada",
    "session.status.transcribing": "Transcribiendo...",
    "session.status.transcribing_chunk": "Transcripción: chunk {current}/{total}...",
    "session.status.transcribing_segment": "Transcribiendo segmento {count}...",
    "session.status.transcription_done": "Transcripción completada. Generando resumen...",
    "session.status.no_text": "No se transcribió ningún texto.",
    "session.status.summary_done": "¡Resumen generado!",
    "session.status.copied": "¡Resumen copiado al portapapeles!",
    "session.status.added_journal": "¡Resumen añadido al Diario!",
    "session.status.quest_extracting": "Extrayendo quests...",
    "session.status.quest_ready": "Propuestas de quests listas.",
    "session.status.quest_updated": "¡Quests actualizadas!",
    "session.status.quest_cancelled": "Actualización de quests cancelada.",
    "session.status.imported": "Audio importado: {name} ({size})",
    "session.status.audio_saved": "Audio guardado: {name}",
    "session.status.segments_transcribed": "Grabando... ({count} segmento{s} transcrito{s})",
    "session.status.transcription_error": "Error de transcripción: {msg}",
    "session.label.transcription": "Transcripción",
    "session.label.summary": "Resumen Épico",
    "session.placeholder.transcript": "La transcripción aparecerá aquí tras la grabación...",
    "session.placeholder.summary": "El resumen épico aparecerá aquí...",
    "session.btn.transcribe": "Transcribir y Resumir",
    "session.btn.add_journal": "Añadir al Diario",
    "session.btn.update_quests": "Actualizar Quests",
    "session.btn.tts_tooltip": "Leer el resumen en voz alta",
    "session.btn.tts_no_voice": "No hay voz en español disponible",
    "session.btn.more_tooltip": "Más opciones",
    "session.menu.import_audio": "Importar audio",
    "session.menu.save_audio": "Guardar audio",
    "session.menu.copy_summary": "Copiar resumen",
    "session.tts.read_selection": "Leer selección",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Grabación completada",
    "session.post.btn_transcribe": "Transcribir y Resumir",
    "session.post.btn_rerecord": "Regrabar",
    "session.post.btn_save_only": "Guardar sin transcribir",
    "session.post.duration": "Duración:",
    "session.post.size": "Tamaño:",
    "session.post.file": "Archivo:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Diario (relatos anteriores) ===",
    "session.context.quest_header": "=== Quest Log (quests activas) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Importar archivo de audio",
    "session.dialog.import_filter": "Archivos de audio (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Todos (*)",
    "session.dialog.save_title": "Guardar archivo de audio",
    "session.dialog.save_filter": "FLAC (*.flac);;Todos (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "No se encontró ningún archivo de audio.",
    "session.error.no_audio_save": "No hay archivo de audio para guardar.",
    "session.error.copy_failed": "Error al copiar: {error}",
    "session.error.flac_failed": "Error de conversión FLAC: {error}",
    "session.error.save_failed": "Error al guardar: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Negrita (Ctrl+B)",
    "editor.tooltip.italic": "Cursiva (Ctrl+I)",
    "editor.tooltip.underline": "Subrayado (Ctrl+U)",
    "editor.tooltip.fold_all": "Plegar todo (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Desplegar todo (Ctrl+Shift+=)",
    "editor.btn.save": " Guardar",
    "editor.heading.normal": "Normal",
    "editor.heading.h1": "Título 1",
    "editor.heading.h2": "Título 2",
    "editor.heading.h3": "Título 3",
    "editor.search.placeholder": "Buscar\u2026",
    "editor.search.no_results": "0 resultados",
    "editor.search.prev_tooltip": "Anterior (Shift+Enter)",
    "editor.search.next_tooltip": "Siguiente (Enter)",
    "editor.search.close_tooltip": "Cerrar (Esc)",
    "editor.tts.read_selection": "Leer selección",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Este registro recoge las quests activas, pistas descubiertas
y misterios por resolver a lo largo de la campaña.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quests Activas</h2>
<ul>
<li><em>No hay quests registradas por el momento.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Pistas y Misterios</h2>
<ul>
<li><em>No hay pistas por el momento.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Quests Completadas</h2>
<ul>
<li><em>No hay quests completadas.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Diario &mdash; {campaign_name}</h1>
<hr>
<p><em>Bienvenido, aventurero. Este diario contiene la crónica de tus hazañas
a lo largo de la campaña. Los relatos épicos de cada sesión
quedarán registrados aquí para la posteridad.</em></p>
<hr>
""",
    "journal.session_heading": "Sesión del {date}",
    "journal.date_format": "%d/%m/%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Conflicto de sincronización — {filename}",
    "conflict.header": (
        "El archivo <b>{filename}</b> fue modificado localmente y en Google Drive.\n"
        "Elige qué versión conservar o fusiona manualmente."
    ),
    "conflict.local_label": "Versión local",
    "conflict.remote_label": "Versión remota (Drive)",
    "conflict.merge_label": "Resultado fusionado (editable):",
    "conflict.btn_keep_local": "Conservar versión local",
    "conflict.btn_keep_remote": "Conservar versión remota",
    "conflict.btn_save_merge": "Guardar fusión",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Cancelar",
    "dialog.btn_ok": "Aceptar",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "Reproduciendo\u2026",
    "tts.status.paused": "En pausa",
    "tts.hint.pause": "Espacio: Pausar",
    "tts.hint.resume": "Espacio: Reanudar",
    "tts.hint.stop": "Esc: Detener",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS no disponible.",
    "tts.error.generic": "Error TTS: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} línea{s} plegada{s}",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Error de grabación: {error}",
    "recorder.error.pause": "Error de pausa: {error}",
    "recorder.error.resume": "Error al reanudar: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Clave API de Mistral no configurada. Ve a Configuración.",
    "transcriber.error.no_api_key_short": "Clave API de Mistral no configurada.",
    "transcriber.error.invalid_key": "Clave API no válida. Verifica tu clave en Configuración.",
    "transcriber.error.transcription": "Error de transcripción: {error}",
    "transcriber.error.live_transcription": "Error de transcripción en vivo: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Clave API de Mistral no configurada.",
    "summarizer.error.generic": "Error de resumen: {error}",
    "summarizer.no_context": "(Primera sesión — sin contexto previo)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Clave API de Mistral no configurada.",
    "quest_extractor.error.generic": "Error de extracción de quests: {error}",
    "quest_extractor.no_quests": "(No hay quests registradas)",
    "quest_extractor.dialog_title": "Actualización de quests",
    "quest_extractor.dialog_label": "Cambios propuestos — edita si es necesario:",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
Eres un cronista épico de los Forgotten Realms, especializado en narrar \
sesiones de Dungeons & Dragons. Escribes en español con un estilo heroico \
e inmersivo, digno de las grandes crónicas de Faerun.

REGLA ABSOLUTA — FIDELIDAD A LA TRANSCRIPCIÓN:
- NO INVENTES ningún detalle que no esté explícitamente presente en la transcripción.
- Si una información no está clara o está ausente de la transcripción, OMÍTELA \
  en lugar de adivinarla o inventarla.
- NO fabriques diálogos, tiradas de dados, valores de daño, DCs, \
  nombres de hechizos ni encuentros que no estén en la transcripción.
- Cada hecho mencionado en el resumen DEBE tener una base en la transcripción.
- Si no estás seguro de un detalle (clase de un personaje, nombre de un hechizo, \
  valor numérico), no lo incluyas o señala la incertidumbre.

ATRIBUCIÓN DE ACCIONES A PERSONAJES:
- La transcripción de audio NO puede identificar de manera fiable quién habla. \
  NO ATRIBUYAS acciones o hechizos a un personaje específico a menos que el \
  personaje sea NOMBRADO EXPLÍCITAMENTE en el diálogo (ej: "Pryor lanza un Smite").
- Si la transcripción contiene marcadores de hablante ([Speaker 0], [Speaker 1], \
  etc.), úsalos para distinguir a los interlocutores, pero NO ADIVINES qué \
  personaje corresponde a qué hablante.
- Cuando la atribución sea incierta, usa formulaciones impersonales: \
  "un aventurero", "el grupo", "uno de los héroes", o la voz pasiva.
- Para las CLASES de los personajes, usa ÚNICAMENTE la información del \
  CONTEXTO DE REFERENCIA de sesiones anteriores. NUNCA deduzcas la clase \
  de un personaje a partir de sus acciones o hechizos en esta sesión.
  EJEMPLO — Transcripción: "Lanzo Eldritch Blast. 25, ¿acierta? Sí. 14 de daño."
  BIEN: "Un Eldritch Blast golpea al enemigo por 14 de daño."
  MAL: "Elppa lanza un Eldritch Blast por 14 de daño." \
  (INCORRECTO — no sabemos QUIÉN habla en la transcripción de audio)

DISTINCIÓN CRUCIAL — ACCIONES vs REFERENCIAS:
- Los jugadores a menudo discuten eventos PASADOS durante la sesión: \
  recapitulaciones, recordatorios de lore, planificación basada en conocimientos \
  adquiridos en sesiones anteriores. Estas REFERENCIAS NO son \
  eventos nuevos de esta sesión.
- Resume SOLO las ACCIONES que ocurren activamente durante esta sesión: \
  exploración, combates, diálogos con NPCs, descubrimientos, decisiones tomadas.
- Si un jugador dice "recuerda, la armadura brilla cerca de dragones" o "la \
  última vez luchamos contra el dragón", son REFERENCIAS — no un \
  combate de dragón en esta sesión.
- En caso de duda sobre si un evento está ocurriendo AHORA o solo es \
  MENCIONADO, no lo incluyas como evento de la sesión.
- NO SAQUES CONCLUSIONES a partir de observaciones aisladas. Si un objeto \
  mágico reacciona (ej: una armadura que brilla), informa la observación tal \
  cual, sin concluir sobre la presencia o ausencia de una criatura o \
  peligro. Hechos, no deducciones.

Reglas generales:
- Resume ÚNICAMENTE los eventos presentes en la NUEVA TRANSCRIPCIÓN. \
  NUNCA resumas el contexto de sesiones anteriores.
- El contexto previo sirve únicamente como referencia para entender nombres, \
  lugares e intrigas ya conocidos. No lo repitas ni lo reformules.
- Si la transcripción no contiene contenido relevante para la campaña de D&D, \
  el resumen puede ser más breve para no exagerar los eventos.
- Escribe en español, en un estilo épico y narrativo, pero NUNCA a costa \
  de la exactitud. El estilo sirve a la narración, no a la invención.
- Conserva TODOS los términos D&D en inglés (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, etc.), así como los nombres de hechizos.
- Los nombres propios (personajes, lugares, criaturas) se mantienen tal cual.
- Ignora las discusiones fuera de tema sin relación con la campaña.

Calidad de la transcripción:
- La transcripción proviene de un modelo speech-to-text que puede producir \
  artefactos: frases repetidas en bucle, texto incoherente, palabras inventadas. \
  Ignora completamente estos pasajes parásitos y concéntrate únicamente en \
  el contenido narrativo relevante para la sesión de D&D.
- ATENCIÓN: algunos pasajes pueden parecer narrativos pero ser artefactos. \
  Si un pasaje no se integra lógicamente con el resto de la sesión, \
  probablemente sea un artefacto — ignóralo.

Formato y estructura:
- Formatea tu respuesta en HTML con etiquetas <h3>, <p>, <strong>, <em>, <ul>/<li>.
- Devuelve ÚNICAMENTE el HTML puro.
- PROHIBIDO: no ```, no ---, no separadores, no comentarios meta.
- Incluye solo las secciones que contengan contenido nuevo.
- FORMATO: listas con viñetas SIMPLES (un solo nivel de <ul>/<li>). \
  NUNCA anides sub-listas. Mantén cada punto conciso en una sola línea.
- Estructura el resumen con EXACTAMENTE estas secciones en este orden. \
  Cada sección comienza con un <h3> seguido del contenido. \
  DEBES incluir TODAS las secciones que tengan contenido relevante.

<h3>{section_major_events}</h3>
Relato narrativo y cronológico de los eventos de la sesión. \
Describe los lugares descubiertos, los encuentros con NPCs y los \
hallazgos. Usa un tono inmersivo y descriptivo. \
Esta es la sección principal y más extensa del resumen. \
Informa las OBSERVACIONES tal cual, sin sacar conclusiones \
(ej: si una armadura brilla, NO concluyas que un dragón está cerca).

<h3>{section_combat}</h3>
Para CADA combate de la sesión, escribe un BREVE PÁRRAFO NARRATIVO \
(3-5 frases) describiendo: enemigos enfrentados, momentos destacados \
(hechizos poderosos, golpes críticos, peligros) y el resultado del combate. \
NO enumeres cada turno o tirada individualmente. \
RECORDATORIO: NO atribuyas hechizos o ataques a un personaje nombrado \
a menos que el nombre se diga EXPLÍCITAMENTE en la transcripción. Prefiere \
la voz pasiva: "un Eldritch Blast golpea", "un Divine Smite derriba". \
Si no hubo combate, OMITE esta sección.

<h3>{section_decisions}</h3>
SOLO los 3-5 hechos más impactantes para la CAMPAÑA: \
objetos mágicos identificados (propiedades Y maldiciones en una frase), \
decisiones estratégicas importantes, información crucial obtenida. \
Formato: lista PLANA <ul>/<li>, UNA línea por elemento, CERO sub-listas. \
EJEMPLO de formato correcto: \
<li><strong>Hacha maldita</strong> — +1 ataque/daño y +1 HP/nivel, \
pero imposible de abandonar, berserk en Wisdom Save fallido, desventaja \
con otras armas.</li>

<h3>{section_mysteries}</h3>
SOLO si un elemento de esta sesión arroja luz sobre un misterio YA CONOCIDO \
del CONTEXTO DE REFERENCIA (quest del códice, amenaza de Auril, etc.). \
Máximo 2-3 elementos. \
Formato: lista simple <ul>/<li>, frase DECLARATIVA factual. \
PROHIBIDO: preguntas retóricas, hipótesis, especulaciones, verbos como \
"sugiere", "parece", "podría", "indica que". \
EJEMPLO — BIEN: "El juramento de Vassaviken confirma que Grimskal fue el \
feudo de una reina de los gigantes de hielo que lideraba campañas de saqueo." \
MAL: "La regeneración de la criatura sugiere una magia vinculada a Auril." \
(INCORRECTO — esto es especulación, no un hecho observado en la transcripción) \
Si nada aclara las intrigas conocidas, OMITE esta sección por completo.
""",
    "prompt.summary_user": """\
CONTEXTO DE REFERENCIA (sesiones anteriores — NO resumir, sirve únicamente \
para entender los personajes, lugares e intrigas ya establecidos):
---
{context}
---

NUEVA TRANSCRIPCIÓN A RESUMIR (resume ÚNICAMENTE este contenido):
---
{transcript}
---

Genera un resumen épico y estructurado que cubra EXCLUSIVAMENTE los nuevos \
eventos de esta transcripción. Cubre TODOS los eventos significativos \
de la transcripción en orden cronológico — no te concentres en \
una sola escena en detrimento de las demás. Si la transcripción no contiene \
nada relevante para la campaña, no es necesario añadir más.
""",
    "prompt.condense": """\
Eres un asistente especializado en el procesamiento de transcripciones de sesiones \
de Dungeons & Dragons.

La transcripción proviene de un modelo speech-to-text que produce muchos \
artefactos: frases repetidas en bucle, texto incoherente, palabras inventadas, \
pasajes sin relación con la sesión de D&D. Ignora completamente estos pasajes \
parásitos.

Condensa el texto conservando ÚNICAMENTE los elementos narrativos relevantes para \
la campaña de D&D. Conserva los términos D&D en inglés. Responde en {language_name}.

Elementos a PRESERVAR ABSOLUTAMENTE:
- Nombres de personajes, NPCs y criaturas encontradas
- Lugares descubiertos con sus descripciones físicas
- DIÁLOGOS CON NPCs: conserva TODO lo que un NPC revela (información, \
  direcciones, advertencias, nombres mencionados, lore). Esto es crítico — \
  la información dada por los NPCs suele ser la más importante de la sesión.
- Combates: enemigos, valores numéricos (tiradas, daño, AC, DC, HP, iniciativa)
- Objetos mágicos: propiedades completas Y maldiciones
- Acciones FALLIDAS y sus consecuencias (explosiones, daño recibido, fracasos)
- Decisiones tomadas por el grupo y sus resultados inmediatos

DISTINCIÓN ACCIONES vs REFERENCIAS:
- Los jugadores a menudo discuten eventos PASADOS: recapitulaciones de sesiones \
  anteriores, recordatorios de lore, planificación. Estas discusiones NO son \
  eventos de la sesión actual.
- Conserva SOLO las ACCIONES que ocurren activamente: exploración de lugares, \
  combates en curso, diálogos con NPCs encontrados, descubrimientos realizados, \
  decisiones tomadas.
- Si un jugador MENCIONA un evento pasado (ej: "recuerda el dragón", \
  "la última vez encontramos..."), es una REFERENCIA — ignórala. \
  Solo los eventos que OCURREN durante la sesión cuentan.
- NO saques conclusiones a partir de observaciones o discusiones \
  entre jugadores. Informa ÚNICAMENTE los hechos brutos, nunca las deducciones.

IMPORTANTE:
- Devuelve ÚNICAMENTE los hechos narrativos brutos, en orden cronológico.
- NO añadas meta-comentarios, conclusiones, resúmenes, sugerencias, \
  "puntos clave", "próximos pasos" ni "preguntas pendientes".
- NO añadas separadores (---), títulos de sección formateados ni \
  comentarios sobre la calidad de la transcripción.
- Preserva los NOMBRES EXACTOS de los personajes tal como se escuchan \
  sin modificarlos ni añadir signos de interrogación.
- Incluso si el texto contiene mucho ruido, extrae TODO fragmento de \
  contenido D&D que contenga, por pequeño que sea. Solo devuelve una respuesta \
  vacía si el texto es 100% artefactos sin ninguna frase coherente \
  relacionada con el juego.

Texto:
{text}
""",
    "prompt.quest_extraction": """\
Eres un asistente especializado en el seguimiento de quests para una campaña \
de Dungeons & Dragons ({campaign_name}).

A partir del resumen de sesión a continuación y del estado actual del quest log, \
genera el quest log COMPLETO recompilado y enriquecido con la nueva \
información de la sesión. El quest log debe ser un documento vivo que \
refleje el estado actual de TODAS las quests.

REGLA ABSOLUTA — DEVUELVE ÚNICAMENTE EL HTML:
- Devuelve ÚNICAMENTE el HTML puro del quest log, NADA más.
- PROHIBIDO: no introducción ("Aquí está el quest log..."), no conclusión, \
  no notas, no comentarios, no ```, no ---.
- El documento comienza con <h1> y termina con </ul>.

Estructura HTML exacta a producir (las 3 secciones DEBEN estar presentes):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Este registro recoge las quests activas, pistas descubiertas
y misterios por resolver a lo largo de la campaña.</em></p>
<hr>
<h2 style="color:#6ab4d4;">{section_active_quests}</h2>
<ul>
<li><strong>Nombre de la quest</strong> — Descripción general de la quest.
  <ul>
  <li><em>{quest_origin}:</em> Quién dio la quest, dónde y cuándo.</li>
  <li><em>{quest_objective}:</em> Qué debe cumplirse.</li>
  <li><em>{quest_progress}:</em> Qué se ha hecho hasta ahora.</li>
  <li><em>{quest_next_step}:</em> Qué queda por hacer.</li>
  <li><em>{quest_npcs}:</em> Personajes involucrados en esta quest.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_clues}</h2>
<ul>
<li><strong>Misterio</strong> — Lo que se sabe, lo que queda por descubrir.
  <ul>
  <li>Detalle o pista descubierta...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_completed_quests}</h2>
<ul>
<li><strong>Nombre de la quest</strong> — Resolución y consecuencias.
  <ul>
  <li><em>{quest_giver}:</em> Quién dio la quest y recompensa.</li>
  <li><em>{quest_resolution}:</em> Cómo se resolvió la quest.</li>
  </ul>
</li>
</ul>

Reglas:
- Escribe en español, estilo conciso y FACTUAL. Sin especulación (no \
  "podría", "parece", "sugiere"). Escribe únicamente lo que se sabe.
- Conserva los términos D&D en inglés (Hit Points, Saving Throw, etc.).
- Los nombres propios se mantienen tal cual.
- Usa listas con viñetas anidadas para los detalles.
- Mueve las quests resueltas de "Quests Activas" a "Quests Completadas".
- PRESERVA TODA la información existente del quest log. No pierdas NINGÚN \
  detalle (quien la dio, recompensa, NPCs, progreso) de las quests existentes. \
  Enriquece con nueva información SIN eliminar la antigua.
- Añade las nuevas quests descubiertas en "Quests Activas".
- Añade nuevas pistas en "Pistas y Misterios". Elimina una pista \
  cuando el misterio se resuelva (menciona la resolución en la quest correspondiente).
- El quest log debe ser una herramienta de referencia detallada, no solo una lista.

Estado actual del quest log:
---
{current_quests}
---

Resumen de la sesión:
---
{summary}
---
""",
    # ── Prompt section headers ──────────────────────────────
    "prompt.section.major_events": "Eventos principales",
    "prompt.section.combat": "Combates",
    "prompt.section.decisions": "Decisiones y descubrimientos",
    "prompt.section.mysteries": "Misterios y pistas",
    "prompt.section.active_quests": "Quests Activas",
    "prompt.section.clues": "Pistas y Misterios",
    "prompt.section.completed_quests": "Quests Completadas",
    "prompt.quest.origin": "Origen",
    "prompt.quest.objective": "Objetivo",
    "prompt.quest.progress": "Progreso",
    "prompt.quest.next_step": "Siguiente paso",
    "prompt.quest.npcs": "NPCs involucrados",
    "prompt.quest.giver": "Quien la dio",
    "prompt.quest.resolution": "Resolución",
    "prompt.language_name": "español",
}
