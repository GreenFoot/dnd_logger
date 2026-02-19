"""Traduções em português — todas as strings da interface e prompts de IA."""

STRINGS: dict[str, str] = {
    # ── utils.py ────────────────────────────────────────────
    "units.bytes": "B",
    "units.kilobytes": "KB",
    "units.megabytes": "MB",
    "units.gigabytes": "GB",
    "units.terabytes": "TB",
    # ── app.py — menus ──────────────────────────────────────
    "app.menu.file": "Ficheiro",
    "app.menu.settings": "Definições...",
    "app.menu.check_updates": "Verificar atualizações...",
    "app.menu.save": "Guardar",
    "app.menu.quit": "Sair",
    "app.menu.campaign": "Campanha",
    "app.menu.new_campaign": "Nova campanha...",
    "app.menu.delete_campaign": "Eliminar campanha...",
    "app.menu.restore_campaign": "Restaurar uma campanha...",
    "app.menu.theme": "Tema",
    "app.menu.session": "Sessão",
    "app.menu.record_stop": "Gravar / Parar",
    # ── app.py — tab titles ──────────────────────────────────
    "app.tab.journal": "Diário",
    "app.tab.quest_log": "Quest Log",
    "app.tab.session": "Sessão",
    # ── app.py — campaign dialogs ───────────────────────────
    "app.campaign.no_campaigns": "Nenhuma campanha encontrada.",
    "app.campaign.name_label": "Nome da campanha:",
    "app.campaign.name_placeholder": "Ex.: Icewind Dale, Curse of Strahd...",
    "app.campaign.btn_create": "Criar",
    "app.campaign.delete_title": "Eliminar uma campanha",
    "app.campaign.delete_label": "Escolha a campanha a eliminar:",
    "app.campaign.delete_confirm_title": "Confirmar eliminação",
    "app.campaign.delete_confirm": 'Eliminar a campanha "{name}"?\nOs ficheiros serão movidos para campaigns/_trash/.',
    "app.campaign.restore_title": "Restaurar uma campanha",
    "app.campaign.restore_label": "Escolha a campanha a restaurar:",
    "app.campaign.restore_none": "Nenhuma campanha arquivada.",
    # ── app.py — campaign creation dialog (Drive) ───────────
    "app.campaign.drive_group": "Google Drive",
    "app.campaign.drive_status_label": "Estado:",
    "app.campaign.drive_not_connected": "Não ligado",
    "app.campaign.drive_connected": "Ligado",
    "app.campaign.drive_btn_login": "Iniciar sessão",
    "app.campaign.drive_logging_in": "A ligar...",
    "app.campaign.drive_folder_id_label": "ID da pasta:",
    "app.campaign.drive_folder_placeholder": "Cole o ID da pasta partilhada...",
    "app.campaign.drive_btn_join": "Juntar-se",
    "app.campaign.drive_join_hint": "(para se juntar)",
    "app.campaign.name_empty": "O nome não pode estar vazio.",
    "app.campaign.name_exists": 'A campanha "{name}" já existe.',
    "app.campaign.drive_paste_id": "Cole o ID da pasta partilhada.",
    "app.campaign.drive_login_first": "Inicie sessão no Google Drive primeiro.",
    "app.campaign.drive_resolving": "A resolver a pasta...",
    "app.campaign.drive_resolve_failed": "Não foi possível resolver o nome da pasta.",
    "app.campaign.drive_deps_missing": "Dependências Google em falta.",
    "app.campaign.drive_error": "Erro Drive: {error}",
    "app.campaign.drive_login_success": "Ligado! Cole o ID da pasta e clique em Juntar-se.",
    "app.campaign.drive_login_failed": "Ligação falhou: {error}",
    "app.campaign.drive_install_deps": (
        "Instale as dependências Google:\n"
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    ),
    "app.campaign.error_title": "Erro",
    # ── app.py — theme picker ───────────────────────────────
    "app.theme.title": "Escolher um tema",
    "app.theme.label": "Nenhum tema automático encontrado para esta campanha.\nEscolha um tema visual:",
    # ── app.py — sync status ────────────────────────────────
    "app.sync.disabled": "Drive: desativado",
    "app.sync.idle": "Drive: sincronizado",
    "app.sync.syncing": "Drive: a sincronizar...",
    "app.sync.conflict": "Drive: conflito detetado",
    "app.sync.error": "Drive: erro",
    "app.sync.offline": "Drive: offline",
    # ── app.py — updater ────────────────────────────────────
    "app.update.title": "Atualização",
    "app.update.available_title": "Atualização disponível",
    "app.update.version_available": "Versão {tag} disponível!",
    "app.update.btn_details": "Detalhes",
    "app.update.btn_later": "Mais tarde",
    "app.update.btn_download": "Transferir e instalar",
    "app.update.no_update": "Está a executar a versão mais recente (v{version}).",
    "app.update.check_error": "Não foi possível verificar atualizações.\n{msg}",
    "app.update.downloading": "A transferir atualização...",
    "app.update.download_progress": "A transferir... {downloaded} / {total}",
    "app.update.download_progress_unknown": "A transferir... {downloaded}",
    "app.update.download_done": (
        "Transferência concluída.\n"
        "A aplicação será encerrada para instalar a atualização.\n\n"
        "Continuar?"
    ),
    "app.update.download_error": "Erro durante a transferência.\n{msg}",
    "app.update.btn_cancel": "Cancelar",
    # ── app.py — first run wizard ───────────────────────────
    "wizard.title": "Bem-vindo — DnD Logger",
    "wizard.welcome": "Bem-vindo ao DnD Logger",
    "wizard.subtitle": "O seu companheiro de sessões de D&D.\nVamos configurar o essencial para começar.",
    "wizard.api_group": "Chave API Mistral",
    "wizard.api_placeholder": "Introduza a sua chave API Mistral...",
    "wizard.api_hint": "Obtenha uma chave em console.mistral.ai",
    "wizard.mic_group": "Microfone",
    "wizard.mic_device_label": "Dispositivo:",
    "wizard.btn_skip": "Configurar mais tarde",
    "wizard.btn_done": "Começar a aventura!",
    # ── settings.py ─────────────────────────────────────────
    "settings.title": "Definições — DnD Logger",
    "settings.tab.api": "API",
    "settings.tab.audio": "Áudio",
    "settings.tab.advanced": "Avançado",
    "settings.tab.prompts": "Prompts",
    "settings.tab.drive": "Google Drive",
    "settings.api.key_label": "Chave API Mistral:",
    "settings.api.key_placeholder": "Introduza a sua chave API Mistral...",
    "settings.api.btn_test": "Testar ligação",
    "settings.api.enter_key_first": "Introduza primeiro uma chave API.",
    "settings.api.test_success": "Ligação bem-sucedida!",
    "settings.api.test_fail": "Falhou: {error}",
    "settings.api.model_label": "Modelo de resumo:",
    "settings.audio.device_label": "Dispositivo de entrada:",
    "settings.audio.device_default": "Predefinido (automático)",
    "settings.audio.btn_test_mic": "Testar microfone",
    "settings.audio.sample_rate_label": "Taxa de amostragem:",
    "settings.audio.test_ok": "O microfone funciona! (nível: {level})",
    "settings.audio.test_weak": "Sinal muito fraco. Verifique o seu microfone.",
    "settings.audio.test_error": "Erro: {error}",
    "settings.audio.test_title": "Teste de microfone",
    "settings.advanced.auto_update": "Verificar atualizações ao iniciar",
    "settings.advanced.chunk_label": "Duração máxima do segmento:",
    "settings.advanced.bias_label": "Contexto D&D (bias):",
    "settings.advanced.bias_placeholder": "Termos D&D (um por linha)...",
    "settings.advanced.language_label": "Idioma:",
    "settings.advanced.restart_required": "Idioma alterado. Por favor, reinicie a aplicação.",
    "settings.advanced.restart_title": "Reinício necessário",
    "settings.prompts.prompt_label": "Prompt:",
    "settings.prompts.btn_reset": "Repor este prompt",
    "settings.prompts.summary_system_label": "Resumo da sessão (sistema)",
    "settings.prompts.condense_label": "Condensação (texto longo)",
    "settings.prompts.quest_extraction_label": "Extração de quests",
    "settings.prompts.hint.summary_system": "Variáveis: nenhuma (prompt de sistema fixo)",
    "settings.prompts.hint.condense": "Variáveis: {text}",
    "settings.prompts.hint.quest_extraction": "Variáveis: {campaign_name}, {current_quests}, {summary}",
    "settings.drive.account_group": "Conta Google",
    "settings.drive.status_label": "Estado:",
    "settings.drive.not_connected": "Não ligado",
    "settings.drive.connected": "Ligado",
    "settings.drive.deps_missing": "Dependências Google em falta",
    "settings.drive.btn_login": "Iniciar sessão",
    "settings.drive.btn_logout": "Terminar sessão",
    "settings.drive.logging_in": "A ligar...",
    "settings.drive.login_failed_title": "Ligação falhou",
    "settings.drive.login_failed": "Erro: {error}",
    "settings.drive.campaign_sync_group": "Sincronização de campanha",
    "settings.drive.active_campaign_label": "Campanha ativa:",
    "settings.drive.join_placeholder": "Cole o ID da pasta partilhada...",
    "settings.drive.join_hint": "(para se juntar)",
    "settings.drive.folder_id_label": "ID da pasta:",
    "settings.drive.no_folder": "Nenhuma pasta criada",
    "settings.drive.creating_folder": "A criar pasta...",
    "settings.drive.btn_copy": "Copiar",
    "settings.drive.sync_checkbox": "Ativar sincronização Google Drive",
    "settings.drive.folder_error": "Não foi possível criar a pasta: {error}",
    "settings.drive.not_connected_error": "Não ligado ao Google Drive",
    # ── session_tab.py ──────────────────────────────────────
    "session.btn.record": "Gravar",
    "session.btn.stop": "Parar",
    "session.btn.pause": "Pausar",
    "session.btn.resume": "Retomar",
    "session.status.ready": "Pronto para gravar",
    "session.status.recording": "A gravar...",
    "session.status.paused": "Gravação em pausa",
    "session.status.stopped": "Gravação parada",
    "session.status.finalizing": "A finalizar transcrição...",
    "session.status.ready_rerecord": "Pronto para regravar",
    "session.status.saved": "Gravação guardada",
    "session.status.transcribing": "A transcrever...",
    "session.status.transcribing_chunk": "Transcrição: segmento {current}/{total}...",
    "session.status.transcribing_segment": "A transcrever segmento {count}...",
    "session.status.transcription_done": "Transcrição concluída.",
    "session.status.summarizing": "A gerar resumo...",
    "session.status.no_text": "Nenhum texto transcrito.",
    "session.status.summary_done": "Resumo gerado!",
    "session.status.copied": "Resumo copiado para a área de transferência!",
    "session.status.added_journal": "Resumo adicionado ao Diário!",
    "session.status.quest_extracting": "A extrair quests...",
    "session.status.quest_ready": "Propostas de quests prontas.",
    "session.status.quest_updated": "Quests atualizadas!",
    "session.status.quest_cancelled": "Atualização de quests cancelada.",
    "session.status.imported": "Áudio importado: {name} ({size})",
    "session.status.audio_saved": "Áudio guardado: {name}",
    "session.status.segments_transcribed": "A gravar... ({count} segmento{s} transcrito{s})",
    "session.status.transcription_error": "Erro de transcrição: {msg}",
    "session.label.transcription": "Transcrição",
    "session.label.summary": "Resumo Épico",
    "session.placeholder.transcript": "A transcrição aparecerá aqui após a gravação...",
    "session.placeholder.summary": "O resumo épico aparecerá aqui...",
    "session.btn.transcribe": "Transcrever",
    "session.btn.summarize": "Resumir",
    "session.btn.add_journal": "Adicionar ao Diário",
    "session.btn.update_quests": "Atualizar Quests",
    "session.btn.tts_tooltip": "Ler o resumo em voz alta",
    "session.btn.tts_no_voice": "Nenhuma voz portuguesa disponível",
    "session.btn.more_tooltip": "Mais opções",
    "session.menu.import_audio": "Importar áudio",
    "session.menu.save_audio": "Guardar áudio",
    "session.menu.copy_summary": "Copiar resumo",
    "session.tts.read_selection": "Ler seleção",
    # ── session_tab.py — PostRecordingDialog ────────────────
    "session.post.title": "Gravação concluída",
    "session.post.btn_transcribe": "Transcrever",
    "session.post.btn_rerecord": "Regravar",
    "session.post.btn_save_only": "Guardar sem transcrever",
    "session.post.duration": "Duração:",
    "session.post.size": "Tamanho:",
    "session.post.file": "Ficheiro:",
    # ── session_tab.py — context headers (sent to AI) ────────
    "session.context.journal_header": "=== Diário (histórias anteriores) ===",
    "session.context.quest_header": "=== Quest Log (quests ativas) ===",
    # ── session_tab.py — file dialogs ───────────────────────
    "session.dialog.import_title": "Importar ficheiro de áudio",
    "session.dialog.import_filter": "Ficheiros de áudio (*.wav *.mp3 *.flac *.ogg *.m4a *.wma);;Todos (*)",
    "session.dialog.save_title": "Guardar ficheiro de áudio",
    "session.dialog.save_filter": "FLAC (*.flac);;Todos (*)",
    # ── session_tab.py — errors ─────────────────────────────
    "session.error.no_audio": "Nenhum ficheiro de áudio encontrado.",
    "session.error.no_audio_save": "Nenhum ficheiro de áudio para guardar.",
    "session.error.copy_failed": "Erro ao copiar: {error}",
    "session.error.flac_failed": "Erro de conversão FLAC: {error}",
    "session.error.save_failed": "Erro ao guardar: {error}",
    # ── rich_editor.py ──────────────────────────────────────
    "editor.tooltip.bold": "Negrito (Ctrl+B)",
    "editor.tooltip.italic": "Itálico (Ctrl+I)",
    "editor.tooltip.underline": "Sublinhado (Ctrl+U)",
    "editor.tooltip.fold_all": "Recolher tudo (Ctrl+Shift+-)",
    "editor.tooltip.unfold_all": "Expandir tudo (Ctrl+Shift+=)",
    "editor.btn.save": " Guardar",
    "editor.heading.normal": "Normal",
    "editor.heading.h1": "Título 1",
    "editor.heading.h2": "Título 2",
    "editor.heading.h3": "Título 3",
    "editor.search.placeholder": "Pesquisar\u2026",
    "editor.search.no_results": "0 resultados",
    "editor.search.prev_tooltip": "Anterior (Shift+Enter)",
    "editor.search.next_tooltip": "Seguinte (Enter)",
    "editor.search.close_tooltip": "Fechar (Esc)",
    "editor.tts.read_selection": "Ler seleção",
    # ── quest_log.py ────────────────────────────────────────
    "quest_log.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Este registo acompanha as quests ativas, pistas descobertas
e mistérios a desvendar ao longo da campanha.</em></p>
<hr>
<h2 style="color:#6ab4d4;">Quests Ativas</h2>
<ul>
<li><em>Nenhuma quest registada ainda.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Pistas e Mistérios</h2>
<ul>
<li><em>Nenhuma pista ainda.</em></li>
</ul>
<h2 style="color:#6ab4d4;">Quests Concluídas</h2>
<ul>
<li><em>Nenhuma quest concluída.</em></li>
</ul>
""",
    # ── journal.py ──────────────────────────────────────────
    "journal.default_html": """\
<h1 style="color:#d4af37; text-align:center;">Diário &mdash; {campaign_name}</h1>
<hr>
<p><em>Bem-vindo, aventureiro. Este diário contém a crónica das suas façanhas
ao longo da campanha. Os relatos épicos de cada sessão
serão aqui registados para a posteridade.</em></p>
<hr>
""",
    "journal.session_heading": "Sessão de {date}",
    "journal.date_format": "%d/%m/%Y",
    # ── sync_conflict_dialog.py ─────────────────────────────
    "conflict.title": "Conflito de sincronização — {filename}",
    "conflict.header": (
        "O ficheiro <b>{filename}</b> foi modificado localmente e no Google Drive.\n"
        "Escolha qual versão manter ou faça a fusão manualmente."
    ),
    "conflict.local_label": "Versão local",
    "conflict.remote_label": "Versão remota (Drive)",
    "conflict.merge_label": "Resultado da fusão (editável):",
    "conflict.btn_keep_local": "Manter versão local",
    "conflict.btn_keep_remote": "Manter versão remota",
    "conflict.btn_save_merge": "Guardar fusão",
    # ── themed_dialogs.py ───────────────────────────────────
    "dialog.btn_cancel": "Cancelar",
    "dialog.btn_ok": "OK",
    # ── tts_overlay.py ──────────────────────────────────────
    "tts.status.playing": "A reproduzir\u2026",
    "tts.status.paused": "Em pausa",
    "tts.hint.pause": "Espaço: Pausar",
    "tts.hint.resume": "Espaço: Retomar",
    "tts.hint.stop": "Esc: Parar",
    # ── tts_engine.py ───────────────────────────────────────
    "tts.error.unavailable": "TTS não disponível.",
    "tts.error.generic": "Erro TTS: {error}",
    # ── fold_gutter.py ──────────────────────────────────────
    "fold.lines_folded": "{count} linha{s} recolhida{s}",
    # ── audio_recorder.py ───────────────────────────────────
    "recorder.error.recording": "Erro de gravação: {error}",
    "recorder.error.pause": "Erro ao pausar: {error}",
    "recorder.error.resume": "Erro ao retomar: {error}",
    # ── transcriber.py ──────────────────────────────────────
    "transcriber.error.no_api_key": "Chave API Mistral não configurada. Vá a Definições.",
    "transcriber.error.no_api_key_short": "Chave API Mistral não configurada.",
    "transcriber.error.invalid_key": "Chave API inválida. Verifique a sua chave em Definições.",
    "transcriber.error.transcription": "Erro de transcrição: {error}",
    "transcriber.error.live_transcription": "Erro de transcrição em direto: {error}",
    # ── summarizer.py ───────────────────────────────────────
    "summarizer.error.no_api_key": "Chave API Mistral não configurada.",
    "summarizer.error.generic": "Erro de resumo: {error}",
    "summarizer.no_context": "(Primeira sessão — sem contexto anterior)",
    # ── quest_extractor.py ──────────────────────────────────
    "quest_extractor.error.no_api_key": "Chave API Mistral não configurada.",
    "quest_extractor.error.generic": "Erro de extração de quests: {error}",
    "quest_extractor.no_quests": "(Nenhuma quest registada)",
    "quest_extractor.dialog_title": "Atualização de quests",
    "quest_extractor.dialog_label": "Alterações propostas — edite se necessário:",
    # ── AI Prompts ──────────────────────────────────────────
    "prompt.summary_system": """\
És um cronista épico dos Forgotten Realms, especializado em narrar \
sessões de Dungeons & Dragons. Escreves em {language_name} com um estilo \
heroico e imersivo, digno das grandes crónicas de Faerun.

REGRA ABSOLUTA — FIDELIDADE À TRANSCRIÇÃO:
- NÃO INVENTES nenhum detalhe que não esteja explicitamente presente na transcrição.
- Se uma informação é pouco clara ou está ausente da transcrição, OMITE-A \
  em vez de adivinhar ou inventar.
- NÃO fabrique diálogos, lançamentos de dados, valores de dano, DCs, \
  nomes de spells ou encontros que não estejam na transcrição.
- Cada facto no resumo DEVE ter fundamento na transcrição.
- Se tens incerteza sobre um detalhe (classe de personagem, nome de spell, \
  valor numérico), não o incluas ou assinala a incerteza.

ATRIBUIÇÃO DE AÇÕES A PERSONAGENS:
- A transcrição áudio NÃO consegue identificar de forma fiável quem está a falar. \
  NÃO atribuas ações ou spells a um personagem específico a menos que o \
  personagem seja EXPLICITAMENTE NOMEADO no diálogo (ex.: "Pryor lança um Smite").
- Se a transcrição contém marcadores de orador ([Speaker 0], [Speaker 1], \
  etc.), usa-os para distinguir oradores, mas NÃO ADIVINHES qual \
  personagem corresponde a qual orador.
- Quando a atribuição é incerta, usa formulações impessoais: \
  "um aventureiro", "o grupo", "um dos heróis", ou voz passiva.
- Para as CLASSES de personagens, usa APENAS informações do \
  CONTEXTO DE REFERÊNCIA de sessões anteriores. NUNCA deduza a classe de um personagem \
  a partir das suas ações ou spells nesta sessão.
  EXEMPLO — Transcrição: "Eu lanço Eldritch Blast. 25, isso acerta? Sim. 14 de dano."
  BOM: "Um Eldritch Blast atinge o inimigo causando 14 de dano."
  MAU: "Elppa lança Eldritch Blast causando 14 de dano." \
  (ERRADO — não sabemos QUEM está a falar numa transcrição áudio)

DISTINÇÃO CRUCIAL — AÇÕES vs REFERÊNCIAS:
- Os jogadores frequentemente discutem EVENTOS PASSADOS durante as sessões: \
  recapitulações, lembretes de lore, planeamento baseado em conhecimento \
  de sessões anteriores. Estas REFERÊNCIAS NÃO SÃO \
  novos eventos desta sessão.
- Resume apenas AÇÕES que ocorrem ativamente durante esta sessão: \
  exploração, combate, diálogos com NPCs, descobertas, decisões tomadas.
- Se um jogador diz "lembram-se, a armadura brilha perto de dragões" ou "da última \
  vez combatemos o dragão", estas são REFERÊNCIAS — não um \
  combate contra um dragão nesta sessão.
- Em caso de dúvida se um evento está a acontecer AGORA ou é \
  apenas MENCIONADO, não o incluas como evento da sessão.
- NÃO TIRES CONCLUSÕES a partir de observações isoladas. Se um item \
  mágico reage (ex.: armadura a brilhar), relata a observação tal como é \
  sem concluir sobre a presença ou ausência de uma criatura ou \
  perigo. Factos, não deduções.

Regras gerais:
- Resume APENAS eventos presentes na NOVA TRANSCRIÇÃO. \
  NUNCA resumas contexto de sessões anteriores.
- O contexto anterior serve apenas como referência para compreender nomes, \
  locais e intrigas já conhecidas. Não o repitas nem o reformules.
- Se a transcrição não contém conteúdo relevante para a campanha de D&D, \
  o resumo pode ser mais curto para evitar exagerar os eventos.
- Escreve em {language_name}, num estilo narrativo épico, mas NUNCA em detrimento \
  da precisão. O estilo serve a narração, não a invenção.
- Mantém TODOS os termos de D&D em inglês (Hit Points, Armor Class, Saving Throw, \
  Spell Slot, Short Rest, Long Rest, etc.), assim como os nomes de spells.
- Os nomes próprios (personagens, locais, criaturas) permanecem tal como são.
- Ignora discussões fora do tema que não estejam relacionadas com a campanha.

Qualidade da transcrição:
- A transcrição provém de um modelo de reconhecimento de fala que pode produzir \
  artefactos: frases repetidas, texto incoerente, palavras inventadas. \
  Ignora completamente estas passagens parasitas e concentra-te apenas no \
  conteúdo narrativo relevante para a sessão de D&D.
- ATENÇÃO: algumas passagens podem parecer narrativas mas são artefactos. \
  Se uma passagem não se integra logicamente com o resto da sessão, \
  é provavelmente um artefacto — ignora-a.

Formato e estrutura:
- Formata a tua resposta em HTML com tags <h3>, <p>, <strong>, <em>, <ul>/<li>.
- Devolve APENAS HTML bruto.
- PROIBIDO: sem ```, sem ---, sem separadores, sem meta-comentários.
- Inclui apenas secções que contenham conteúdo novo.
- FORMATAÇÃO: Listas com marcadores SIMPLES (um único nível de <ul>/<li>). \
  NUNCA aninhar sublistas. Mantém cada ponto conciso numa única linha.
- Estrutura o resumo com EXATAMENTE estas secções nesta ordem. \
  Cada secção começa com um <h3> seguido de conteúdo. \
  DEVES incluir TODAS as secções que tenham conteúdo relevante.

<h3>{section_major_events}</h3>
Narrativa cronológica dos eventos da sessão. \
Descreve locais descobertos, encontros com NPCs e \
descobertas. Usa um tom imersivo e descritivo. \
Esta é a secção principal e mais longa do resumo. \
Relata OBSERVAÇÕES tal como são, sem tirar conclusões \
(ex.: se a armadura brilha, NÃO concluas que um dragão está por perto).

<h3>{section_combat}</h3>
Para CADA combate da sessão, escreve um PARÁGRAFO NARRATIVO CURTO \
(3-5 frases) descrevendo: inimigos enfrentados, momentos notáveis \
(spells poderosas, acertos críticos, perigos) e o resultado do combate. \
NÃO enumeres cada turno ou lançamento individualmente. \
LEMBRETE: NÃO atribuas spells ou ataques a um personagem nomeado \
a menos que o nome seja EXPLICITAMENTE mencionado na transcrição. Prefere \
voz passiva: "um Eldritch Blast atinge", "um Divine Smite abate". \
Se não houve combate, OMITE esta secção.

<h3>{section_decisions}</h3>
APENAS os 3-5 factos mais impactantes para a CAMPANHA: \
itens mágicos identificados (propriedades E maldições numa frase), \
escolhas estratégicas importantes, informações cruciais obtidas. \
Formato: lista PLANA <ul>/<li>, UMA linha por item, ZERO sublistas. \
EXEMPLO de formato correto: \
<li><strong>Machado amaldiçoado</strong> — +1 ataque/dano e +1 HP/nível, \
mas impossível de abandonar, fúria em Wisdom Save falhado, desvantagem \
com outras armas.</li>

<h3>{section_mysteries}</h3>
APENAS se um elemento desta sessão ilumina um mistério JÁ CONHECIDO \
do CONTEXTO DE REFERÊNCIA (quest do codex, ameaça de Auril, etc.). \
Máximo 2-3 itens. \
Formato: lista simples <ul>/<li>, frase factual DECLARATIVA. \
PROIBIDO: perguntas retóricas, hipóteses, especulações, verbos como \
"sugere", "parece", "poderia", "indica que". \
EXEMPLO — BOM: "O juramento de Vassaviken confirma que Grimskal era o \
feudo de uma rainha dos gigantes de gelo que liderava campanhas de pilhagem." \
MAU: "A regeneração da criatura sugere magia ligada a Auril." \
(ERRADO — isto é especulação, não um facto observado na transcrição) \
Se nada ilumina intrigas conhecidas, OMITE esta secção inteiramente.
""",
    "prompt.summary_user": """\
CONTEXTO DE REFERÊNCIA (sessões anteriores — NÃO resumas, serve apenas \
para compreender personagens, locais e intrigas já estabelecidas):
---
{context}
---

NOVA TRANSCRIÇÃO A RESUMIR (resume APENAS este conteúdo):
---
{transcript}
---

Gera um resumo épico e estruturado cobrindo EXCLUSIVAMENTE os novos \
eventos desta transcrição. Cobre TODOS os eventos significativos \
da transcrição em ordem cronológica — não te concentres numa \
única cena em detrimento das outras. Se a transcrição não contém \
nada relevante para a campanha, não é necessário acrescentar mais.
""",
    "prompt.condense": """\
És um assistente especializado no processamento de transcrições de sessões \
de Dungeons & Dragons.

A transcrição provém de um modelo de reconhecimento de fala que produz muitos \
artefactos: frases repetidas, texto incoerente, palavras inventadas, \
passagens sem relação com a sessão de D&D. Ignora completamente estas \
passagens parasitas.

Condensa o texto mantendo APENAS elementos narrativos relevantes para \
a campanha de D&D. Mantém os termos de D&D em inglês. Responde em {language_name}.

Elementos a PRESERVAR ABSOLUTAMENTE:
- Nomes de personagens, NPCs e criaturas encontradas
- Locais descobertos com as suas descrições físicas
- DIÁLOGOS com NPCs: preserva TUDO o que um NPC revela (informações, \
  direções, avisos, nomes mencionados, lore). Isto é crítico — \
  a informação dada pelos NPCs é frequentemente a mais importante da sessão.
- Combate: inimigos, valores numéricos (lançamentos, dano, AC, DC, HP, iniciativa)
- Itens mágicos: propriedades completas E maldições
- Ações FALHADAS e as suas consequências (explosões, dano sofrido, falhas)
- Decisões tomadas pelo grupo e os seus resultados imediatos

DISTINÇÃO AÇÕES vs REFERÊNCIAS:
- Os jogadores frequentemente discutem EVENTOS PASSADOS: recapitulações de sessões \
  anteriores, lembretes de lore, planeamento. Estas discussões NÃO SÃO eventos da \
  sessão atual.
- Retém apenas AÇÕES que ocorrem ativamente: exploração de locais, \
  combate em curso, diálogos com NPCs encontrados, descobertas feitas, \
  decisões tomadas.
- Se um jogador MENCIONA um evento passado (ex.: "lembram-se do dragão", \
  "da última vez encontrámos..."), é uma REFERÊNCIA — ignora-a. \
  Apenas eventos que ACONTECEM durante a sessão contam.
- NÃO tires conclusões a partir de observações ou discussões dos jogadores. \
  Relata APENAS factos brutos, nunca deduções.

IMPORTANTE:
- Devolve APENAS factos narrativos brutos, em ordem cronológica.
- NÃO adiciones meta-comentários, conclusões, resumos, sugestões, \
  "pontos-chave", "próximos passos" ou "questões em aberto".
- NÃO adiciones separadores (---), títulos de secções formatados ou \
  comentários sobre a qualidade da transcrição.
- Preserva os nomes EXATOS dos personagens tal como ouvidos, \
  sem os modificar ou adicionar pontos de interrogação.
- Mesmo que o texto contenha muito ruído, extrai CADA fragmento de \
  conteúdo de D&D dentro dele, por mais pequeno que seja. Devolve apenas uma \
  resposta vazia se o texto for 100%% artefactos sem nenhuma frase coerente relacionada com o jogo.

Texto:
{text}
""",
    "prompt.quest_extraction": """\
És um assistente especializado no acompanhamento de quests para uma campanha \
de Dungeons & Dragons ({campaign_name}).

A partir do resumo da sessão abaixo e do estado atual do quest log, \
gera o quest log COMPLETO recompilado e enriquecido com as novas \
informações da sessão. O quest log deve ser um documento vivo que \
reflete o estado atual de TODAS as quests.

REGRA ABSOLUTA — DEVOLVE APENAS HTML:
- Devolve APENAS o HTML bruto do quest log, NADA mais.
- PROIBIDO: sem introdução ("Aqui está o quest log..."), sem conclusão, \
  sem notas, sem comentários, sem ```, sem ---.
- O documento começa com <h1> e termina com </ul>.

Estrutura HTML exata a produzir (as 3 secções DEVEM estar presentes):

<h1 style="color:#d4af37; text-align:center;">Quest Log &mdash; {campaign_name}</h1>
<hr>
<p><em>Este registo acompanha as quests ativas, pistas descobertas
e mistérios a desvendar ao longo da campanha.</em></p>
<hr>
<h2 style="color:#6ab4d4;">{section_active_quests}</h2>
<ul>
<li><strong>Nome da quest</strong> — Descrição geral da quest.
  <ul>
  <li><em>{quest_origin}:</em> Quem deu a quest, onde e quando.</li>
  <li><em>{quest_objective}:</em> O que deve ser realizado.</li>
  <li><em>{quest_progress}:</em> O que foi feito até agora.</li>
  <li><em>{quest_next_step}:</em> O que falta fazer.</li>
  <li><em>{quest_npcs}:</em> Personagens envolvidos nesta quest.</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_clues}</h2>
<ul>
<li><strong>Mistério</strong> — O que se sabe, o que falta descobrir.
  <ul>
  <li>Detalhe ou pista descoberta...</li>
  </ul>
</li>
</ul>
<h2 style="color:#6ab4d4;">{section_completed_quests}</h2>
<ul>
<li><strong>Nome da quest</strong> — Resolução e consequências.
  <ul>
  <li><em>{quest_giver}:</em> Quem deu a quest e recompensa.</li>
  <li><em>{quest_resolution}:</em> Como a quest foi resolvida.</li>
  </ul>
</li>
</ul>

Regras:
- Escreve em {language_name}, estilo conciso e FACTUAL. Sem especulação (sem \
  "poderia", "parece", "sugere"). Escreve apenas o que é conhecido.
- Mantém os termos de D&D em inglês (Hit Points, Saving Throw, etc.).
- Os nomes próprios permanecem tal como são.
- Usa listas com marcadores aninhados para detalhes.
- Move quests resolvidas de "Quests Ativas" para "Quests Concluídas".
- PRESERVA TODAS as informações existentes no quest log. Não PERCAS NENHUM \
  detalhe (quest giver, recompensa, NPCs, progresso) das quests existentes. \
  Enriquece com novas informações SEM apagar informações antigas.
- Adiciona quests recém-descobertas às "Quests Ativas".
- Adiciona novas pistas às "Pistas e Mistérios". Remove uma pista \
  quando o mistério é resolvido (menciona a resolução na quest relacionada).
- O quest log deve ser uma ferramenta de referência detalhada, não apenas uma lista.

Estado atual do quest log:
---
{current_quests}
---

Resumo da sessão:
---
{summary}
---
""",
    # ── Prompt section headers (used in prompt placeholders) ─
    "prompt.section.major_events": "Eventos Principais",
    "prompt.section.combat": "Combate",
    "prompt.section.decisions": "Decisões e Descobertas",
    "prompt.section.mysteries": "Mistérios e Pistas",
    "prompt.section.active_quests": "Quests Ativas",
    "prompt.section.clues": "Pistas e Mistérios",
    "prompt.section.completed_quests": "Quests Concluídas",
    "prompt.quest.origin": "Origem",
    "prompt.quest.objective": "Objetivo",
    "prompt.quest.progress": "Progresso",
    "prompt.quest.next_step": "Próximo passo",
    "prompt.quest.npcs": "NPCs envolvidos",
    "prompt.quest.giver": "Quest giver",
    "prompt.quest.resolution": "Resolução",
    "prompt.language_name": "português",
}
