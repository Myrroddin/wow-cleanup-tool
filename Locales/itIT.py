TRANSLATIONS = {
    "itIT": {
        # Window title
        "window_title": "Strumento di Pulizia WoW",

        # Menu/Tab names
        "file_cleaner": "Pulizia File",
        "folder_cleaner": "Pulizia Cartelle",
        "orphan_cleaner": "Pulizia Orfani",
        "game_optimizer": "Ottimizzazione Gioco",
        "optimization_suggestions": "Suggerimenti di Ottimizzazione",
        "log": "Registro",
        "help_about": "Aiuto/Info",

        # Options section
        "options": "Opzioni",
        "wow_folder": "Cartella WoW:",
        "browse": "Sfoglia...",
        "browse_tooltip": "Sfoglia la cartella di World of Warcraft.",
        "font_size": "Dimensione carattere:",
        "font": "Carattere:",
        "theme": "Tema:",
        "language": "Lingua:",
        "file_action": "Azione file:",
        "delete_permanently": "Elimina definitivamente",
        "move_to_recycle": "Sposta nel Cestino",
        "enable_verbose": "Abilita registro dettagliato",
        "verbose_tooltip": "Quando abilitato, il registro registra ogni file/cartella/riga di AddOns.txt elaborati.",
        "external_log": "Registro esterno:",
        "fresh": "Nuovo",
        "fresh_tooltip": "Crea un nuovo file di registro ad ogni esportazione (sovrascrive quello esistente).",
        "append": "Aggiungi",
        "append_tooltip": "Aggiunge ogni esportazione al file di registro esistente (mantiene 10-20 sessioni a seconda della verbosità).",
        "check_updates": "Verifica aggiornamenti",
        "check_updates_tooltip": "Quando abilitato, controlla le nuove versioni su GitHub all'avvio.",
        "restore_defaults": "Ripristina predefiniti",
        "light": "Chiaro",
        "dark": "Scuro",

        # File Cleaner
        "scan": "Scansiona",
        "select_all": "Seleziona tutto",
        "expand_all": "Espandi tutto",
        "collapse_all": "Comprimi tutto",
        "process_selected": "Elabora selezionati",
        "scanning": "Scansione in corso…",
        "no_bak_old_found": "Nessun file .bak o .old trovato.",
        "files_found": "{} file trovati.",

        # Folder Cleaner
        "version": "Versione:",
        "path": "Percorso:",
        "preview": "Anteprima",
        "toggle_all": "Commuta tutti",
        "process_folders": "Elabora cartelle selezionate",

        # Orphan Cleaner
        "rebuild_addons": "Ricostruisci AddOns.txt",
        "no_orphans_found": "Nessun SavedVariables orfano trovato.",
        "orphans_found": "{} SavedVariable orfani trovati.",

        # Game Optimizer
        "scan_hardware": "Scansiona hardware",
        "system_matches": "Il tuo sistema corrisponde a:",
        "optimization_applied": "✓ Ottimizzazione applicata",
        "optimization_not_applied": "⚠ Ottimizzazione non ancora applicata",
        "graphics_presets": "Preset grafici ({}):",
        "graphics_presets_classic": "Preset grafici ({}):",
        "apply_preset": "Applica preset:",
        "apply": "Applica",
        "preset_applied": "✓ Preset {} applicato.",
        "error": "✗ Errore: {}",
        "low": "Basso",
        "medium": "Medio",
        "high": "Alto",
        "ultra": "Ultra",

        # Optimization Suggestions
        "manual_suggestions": "Suggerimenti di Ottimizzazione Manuale",
        "manual_disclaimer": "Nota: questa applicazione NON esegue automaticamente queste ottimizzazioni. Questi sono suggerimenti che devi implementare manualmente.",
        "clean_data_folder": "Pulisci la cartella Data del gioco",
        "clean_data_text": "Se sono passati alcuni anni o diverse espansioni da quando hai installato WoW, considera di eliminare la cartella Data nella directory principale di World of Warcraft. Questo *potrebbe* ridurre la dimensione del gioco e migliorare le prestazioni dello schermo di caricamento. Il launcher Battle.net ricostruirà automaticamente questa cartella quando necessario.",
        "enable_hdr": "Abilita HDR (High Dynamic Range)",
        "enable_hdr_text": "Controlla le impostazioni di visualizzazione del sistema operativo per vedere se HDR è disponibile. Se il tuo monitor lo supporta, abilitare HDR può migliorare significativamente la chiarezza visiva e la profondità del colore nel gioco.",
        "verify_refresh": "Verifica la frequenza di aggiornamento del monitor",
        "verify_refresh_text": "Assicurati che la frequenza di aggiornamento del monitor sia impostata al massimo supportato nelle impostazioni di visualizzazione del sistema operativo. Frequenze più elevate forniscono un'esperienza di gioco più fluida e una migliore reattività.",
        "enable_sam": "Abilita Smart Access Memory/Resizable BAR",
        "enable_sam_text": "Controlla le impostazioni del BIOS della scheda madre per Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). L'abilitazione consente alla CPU di accedere all'intera memoria GPU, migliorando potenzialmente le prestazioni.",
        "enable_xmp": "Abilita profili memoria XMP",
        "enable_xmp_text": "Accedi al BIOS della scheda madre e abilita XMP (Extreme Memory Profile) o le impostazioni DOCP/EOCP. Questo assicura che la RAM funzioni alla sua velocità nominale invece della velocità predefinita conservativa, migliorando le prestazioni complessive del sistema.",

        # Log tab
        "export_log": "Esporta registro",
        "clear_log": "Cancella registro",

        # Help/About
        "about_text": "Suite completa di manutenzione e ottimizzazione per World of Warcraft.\nPulisci file non necessari, gestisci addon, ottimizza le prestazioni di gioco e altro.\n\nChiudi sempre World of Warcraft prima di eseguire questo strumento.",
        "copyright": "Copyright © 2025 Paul Vandersypen. Rilasciato sotto i termini della GNU General Public License v3.0 (GPL-3.0-or-later). Consulta il file LICENSE allegato per i termini completi.",

        # Dialogs
        "invalid_folder": "Cartella non valida",
        "select_valid_wow": "Seleziona prima una cartella WoW valida.",
        "no_selection": "Nessuna selezione",
        "no_files_selected": "Nessun file selezionato da elaborare.",
        "no_folders_selected": "Nessuna cartella selezionata da pulire.",
        "no_orphans_selected": "Nessun orfano selezionato.",
        "confirm": "Conferma",
        "confirm_action": "Sei sicuro di voler {} {} {}?",
        "file_s": " file",
        "folder_s": " cartelle",
        "orphaned_savedvars": " SavedVariables orfani",
        "completed": "Completato",
        "processed": "{} {} elaborati.",        "restore_defaults_confirm": "Ripristinare tutte le impostazioni ai valori predefiniti?",
        "restart_required": "Impostazioni ripristinate. L'applicazione verrà ora riavviata.",
        "error_title": "Errore",
        "restore_error": "Ripristino predefiniti fallito: {}",
        "confirm_font": "Conferma carattere",
        "apply_font_confirm": "Applicare il carattere '{}' all'applicazione?",
        "select_font": "Seleziona carattere",
        "export_log_title": "Esporta registro",
        "log_empty": "Il registro è vuoto. Niente da esportare.",
        "log_exported": "Registro esportato con successo in:\n{}",
        "export_error": "Errore esportazione",
        "export_failed": "Esportazione registro fallita:\n{}",
        "addons_rebuilt": "Voci AddOns.txt ricostruite.\nTotale scritte: {}\nTotale rimosse: {}",

        # Log messages
        "session_started": "Sessione avviata — {}",
        "file_scan": "Scansione pulizia file: {} corrispondenze.",
        "orphan_scan": "Scansione pulizia orfani: {} orfani.",
        "file_processed": "Pulizia file: {} file elaborati.",
        "folder_processed": "Pulizia cartelle: {} cartelle elaborate.",
        "orphan_processed": "Pulizia orfani: {} orfani elaborati.",        "addons_txt_log": "[AddOns.txt] {}: {} voci scritte, {} rimosse",
        "preset_applied_log": "Preset {} applicato per {}",
        "preset_failed_log": "Applicazione preset {} fallita: {}",
        "change_language": "Cambia lingua",
        "change_language_question": "Cambiare lingua da {} a {}?\n\nL\'applicazione verrà riavviata per applicare la nuova lingua.",
        "language_changed": "Lingua cambiata",
        "language_changed_restart": "Lingua cambiata in {}.\nL\'applicazione verrà ora riavviata.",
        "apply": "Applica",
        "cancel": "Annulla",
        "scan_bak_old": "Scansiona file .bak / .old",
        "expand_all": "Espandi tutto",
        "collapse_all": "Comprimi tutto",
        "select_deselect_all": "Seleziona/Deseleziona tutto",
        "process_selected_files": "Elabora file selezionati",
        "scan_orphaned": "Scansiona SavedVariables orfani",
        "process_selected_folders": "Elabora cartelle selezionate",
        "select_deselect_all_folders": "Seleziona/Deseleziona tutte le cartelle",
        "select_deselect_all_screenshots": "Seleziona/Deseleziona tutti gli screenshot",
        "process_selected_screenshots": "Elabora Screenshot Selezionati",
        "no_screenshots_selected": "Nessuno screenshot selezionato.",
        "confirm_action_screenshots": "{} {} file di screenshot?",
        "processed_screenshots_count": "{} screenshot elaborati.",
        "screenshots_per_file": "Screenshot (per azione file)",
        "folder_screenshots": "Screenshot",
        "folder_logs": "Registri",
        "folder_errors": "Errori",
        "check_for_updates": "Verifica aggiornamenti",

        # Game Optimizer
        "game_optimizer_title": "Ottimizzatore Gioco",
        "game_optimizer_desc": "Ottimizza le prestazioni di World of Warcraft in base alla tua configurazione hardware.",
        "scan_hardware": "Scansiona hardware",
        "click_scan_hardware": "Clicca 'Scansiona hardware' per rilevare le capacità del tuo sistema.",
        "select_valid_wow_folder": "Seleziona una cartella WoW valida nelle Opzioni per abilitare le visualizzazioni per versione.",
        "recommended_settings": "Impostazioni consigliate:",
        "apply_preset_label": "Applica preset:",
        "apply_recommended_settings": "Applica impostazioni consigliate",
        "scanning_cpu": "Scansione CPU in corso...",
        "scanning_ram": "Scansione RAM in corso... (CPU rilevata: {} core/{} thread)",
        "scanning_gpu": "Scansione GPU in corso... (RAM rilevata: {} GB)",

        # Startup warning
        "important_notice": "Avviso importante",
        "startup_warning_text": "⚠️ Prima di usare questo strumento, assicurati che World of Warcraft sia completamente chiuso.\n\nEseguire lo strumento mentre WoW è aperto potrebbe interferire con i file di gioco.",
        "do_not_show_again": "Non mostrare più questo avviso",
        "ok": "OK",

        # Folder cleaner
        "select_valid_wow_folder_cleaner": "Seleziona una cartella WoW valida nelle Opzioni per abilitare il Pulitore Cartelle.",
        "preview_label": "Anteprima",
        "preview_hint": "(Clicca sull'immagine per ingrandire • Clicca di nuovo o premi Esc per chiudere)",
        "screenshots_not_found": "Cartella Screenshot non trovata per questa versione.",

        # Optimization Suggestions tab - detailed content
        "opt_sug_header": "Suggerimenti di Ottimizzazione Manuale",
        "opt_sug_disclaimer": "Nota: questa applicazione NON esegue automaticamente queste ottimizzazioni. Questi sono suggerimenti che devi implementare manualmente.",
        "opt_sug_clean_data_title": "Pulisci la cartella Data del gioco",
        "opt_sug_clean_data_text": "Se sono passati alcuni anni o diverse espansioni da quando hai installato WoW, considera di eliminare la cartella Data nella directory principale di World of Warcraft. Questo *potrebbe* ridurre la dimensione del gioco e migliorare le prestazioni dello schermo di caricamento. Il launcher Battle.net ricostruirà automaticamente questa cartella quando necessario.",
        "opt_sug_clean_data_tooltip": "Motivo: La cartella Data accumula risorse di gioco temporanee e in cache nel tempo. Eliminarla forza un nuovo download di file ottimizzati.\n\nLivello di rischio: Sicuro - Battle.net scaricherà automaticamente i file necessari.\n\nBenefici attesi: Schermate di caricamento più veloci, ridotto utilizzo disco (potenziale risparmio 10-20 GB).",
        "opt_sug_hdr_title": "Abilita HDR (High Dynamic Range)",
        "opt_sug_hdr_text": "Controlla le impostazioni di visualizzazione del sistema operativo per vedere se HDR è disponibile. Se il tuo monitor lo supporta, abilitare HDR può migliorare significativamente la chiarezza visiva e la profondità del colore nel gioco.",
        "opt_sug_hdr_tooltip": "Motivo: HDR offre una gamma di colori più ampia e un migliore contrasto, rendendo gli effetti visivi più vividi e realistici.\n\nLivello di rischio: Sicuro - facilmente attivabile/disattivabile nelle impostazioni OS.\n\nBenefici attesi: Miglioramento significativo della qualità visiva se il monitor supporta HDR10 o superiore.\n\nRequisiti: Monitor compatibile HDR e Windows 10/11 o macOS Catalina+.",
        "opt_sug_refresh_title": "Verifica la frequenza di aggiornamento del monitor",
        "opt_sug_refresh_text": "Assicurati che la frequenza di aggiornamento del monitor sia impostata al massimo supportato nelle impostazioni di visualizzazione del sistema operativo. Frequenze più elevate forniscono un'esperienza di gioco più fluida e una migliore reattività.",
        "opt_sug_refresh_tooltip": "Motivo: Molti sistemi impostano di default 60Hz anche se i monitor supportano 120Hz/144Hz/165Hz. Questo limita inutilmente la frequenza dei fotogrammi.\n\nLivello di rischio: Sicuro - nessun rischio hardware, facile da ripristinare.\n\nBenefici attesi: Gameplay più fluido, riduzione latenza input, miglior tempo di risposta.\n\nCome verificare: Windows: Impostazioni > Display > Avanzate > Frequenza di aggiornamento\nmacOS: Preferenze di Sistema > Monitor",
        "opt_sug_sam_title": "Abilita Smart Access Memory/Resizable BAR",
        "opt_sug_sam_text": "Controlla le impostazioni del BIOS della scheda madre per Smart Access Memory (AMD) o Resizable BAR (Intel/NVIDIA). L'abilitazione consente alla CPU di accedere all'intera memoria GPU, migliorando potenzialmente le prestazioni.",
        "opt_sug_sam_tooltip": "Motivo: Consente alla CPU di accedere all'intera memoria GPU in una volta, invece di piccoli blocchi da 256MB, riducendo i colli di bottiglia.\n\nLivello di rischio: Moderato - richiede modifiche al BIOS. Annota prima le impostazioni attuali.\n\nBenefici attesi: Aumento FPS 5-15% in scene intensive GPU.\n\nRequisiti:\n• AMD: CPU Ryzen 5000+ + GPU RX 6000+\n• Intel: CPU 10a gen+ + GPU RTX 3000+\n• Potrebbe richiedere aggiornamento BIOS",
        "opt_sug_xmp_title": "Abilita profili memoria XMP",
        "opt_sug_xmp_text": "Accedi al BIOS della scheda madre e abilita XMP (Extreme Memory Profile) o le impostazioni DOCP/EOCP. Questo assicura che la RAM funzioni alla sua velocità nominale invece della velocità predefinita conservativa, migliorando le prestazioni complessive del sistema.",
        "opt_sug_xmp_tooltip": "Motivo: La RAM spesso funziona a 2133MHz di default anche se è valutata per 3200MHz+. XMP abilita le velocità pubblicizzate.\n\nLivello di rischio: Moderato - modifica BIOS. Il sistema potrebbe non avviarsi se la RAM è instabile (facile da resettare).\n\nBenefici attesi: Aumento prestazioni CPU 10-20%, caricamenti più veloci, migliori 1% low.\n\nCome abilitare: Accedi al BIOS (di solito Canc/F2 all'avvio) > Trova impostazioni XMP/DOCP > Abilita > Salva ed esci",
        "opt_sug_reinstall_title": "Reinstalla WoW (Installazione pulita)",
        "opt_sug_reinstall_text": "Fai il backup delle cartelle AddOns e WTF, disinstalla tutte le versioni di WoW tramite Battle.net, reinstalla e ripristina i backup. Questo rimuove file legacy accumulati e dati obsoleti da anni di patch.",
        "opt_sug_reinstall_tooltip": "Motivo: Anni di aggiornamenti lasciano file obsoleti, risorse deprecate e dati frammentati che rallentano il caricamento e sprecano spazio.\n\nLivello di rischio: Basso - Le impostazioni/addon sono preservati nelle cartelle WTF/AddOns.\n\nBenefici attesi: Caricamenti più veloci, uso disco ridotto (5-15 GB risparmiati), stabilità migliorata.\n\nCome fare: 1) Backup di Interface\\AddOns e WTF\n2) Disinstalla tramite Battle.net\n3) Reinstalla WoW\n4) Copia le cartelle di backup",

        # Help/About tab - content
        "help_version_label": "Strumento di Pulizia WoW {}",
        "help_about_description": "Suite completa di manutenzione e ottimizzazione per World of Warcraft.\nPulisci file non necessari, gestisci addon, ottimizza le prestazioni di gioco e altro.\n\nChiudi sempre World of Warcraft prima di eseguire questo strumento.",
        "help_copyright": "Copyright © 2025 Paul Vandersypen. Rilasciato sotto i termini della GNU General Public License v3.0 (GPL-3.0-or-later). Consulta il file LICENSE allegato per i termini completi.",
        "support_patreon": "Supporta su Patreon",
        "donate_paypal": "Dona tramite PayPal",
        "github_repository": "Repository GitHub",
        "github_issues": "Segnala problemi",


        # Game Optimizer - hardware detection messages
        "hardware_detected": "✓ CPU: {} | RAM: {} | GPU: {}",
        "gpu_switch_notification": "⚠ Cambio GPU: Impostato per usare '{}' invece di '{}'. Questa modifica ottimizza le prestazioni utilizzando la tua GPU dedicata per una migliore esperienza di gioco. È sicuro e consigliato.",
        "scan_tooltip_refresh": "Non è necessario scansionare di nuovo a meno che non hai modificato CPU, GPU o RAM.\nClicca per aggiornare le informazioni hardware nella cache.",
        "scanning_ram_detected": "Scansione RAM in corso... (CPU rilevata: {} core/{} thread)",
        "scanning_gpu_detected": "Scansione GPU in corso... (RAM rilevata: {} GB)",
        "apply_preset_label": "Applica preset:",

        # Game Optimizer - Config.wtf modification dialogs
        "wow_running_title": "WoW in esecuzione",
        "wow_running_message": "World of Warcraft è attualmente in esecuzione. Le modifiche avranno effetto dopo il riavvio del gioco.\n\nVuoi continuare?",
        "permission_error_title": "Errore permessi",
        "permission_error_message": "Config.wtf è in sola lettura. Rimuovi l'attributo di sola lettura e riprova.",
        "config_readonly_status": "✗ Config.wtf è in sola lettura.",
        "confirm_apply_title": "Conferma applicazione",
        "confirm_apply_message": "Applicare il preset {} a {}?\n\nQuesto modificherà {} impostazioni grafiche in Config.wtf.\nVerrà creato automaticamente un backup.\n\nModifiche principali:\n• Preset: Impostazioni qualità {}\n• Prestazioni: {} ottimizzazioni",
        "cancelled_by_user": "Annullato dall'utente.",
        "settings_applied_status": "✓ {} impostazioni applicate.",
        "preset_applied_status": "✓ Preset {} applicato.",
        "apply_error_status": "✗ Errore: {}",

        # Preset tooltips
        "preset_tooltip_template": "Preset {}\n\nPrestazioni attese:\n{}\n\nClicca 'Applica' qui sotto per usare questo preset.",
        "perf_depends_hardware": "L'impatto sulle prestazioni dipende dal tuo hardware.",
        "perf_will_vary": "Le prestazioni varieranno",

        # Low preset performance estimates
        "low_perf_high": "Prestazioni eccellenti (100+ FPS nella maggior parte degli scenari)",
        "low_perf_mid": "Prestazioni molto buone (80-120 FPS)",
        "low_perf_low": "Buone prestazioni (60-80 FPS)",

        # Medium preset performance estimates
        "medium_perf_high": "Prestazioni eccellenti (90-120 FPS)",
        "medium_perf_mid": "Buone prestazioni (60-90 FPS)",
        "medium_perf_low": "Prestazioni moderate (45-60 FPS)",

        # High preset performance estimates
        "high_perf_high": "Prestazioni molto buone (70-100 FPS)",
        "high_perf_mid": "Buone prestazioni (50-70 FPS)",
        "high_perf_low": "Potrebbe avere difficoltà in raid (30-50 FPS)",

        # Ultra preset performance estimates
        "ultra_perf_high": "Buone prestazioni (60-80 FPS)",
        "ultra_perf_mid": "Prestazioni moderate (40-60 FPS)",
        "ultra_perf_low": "Prestazioni inferiori (20-40 FPS)",

        # WoW version names
        "version_retail": "Retail",
        "version_classic": "Classic",
        "version_classic_era": "Classic Era",
        "version_ptr": "PTR",
        "version_beta": "Beta",

        # Game Optimizer - additional strings
        "not_detected": "Non rilevato",
        "unknown_cpu": "CPU sconosciuta",
        "unknown_gpu": "Sconosciuta",
        "not_set": "Non impostato",
        "hover_for_details": "Passa sopra per i dettagli",

        # Orphan Cleaner - log messages
        "orphan_found_in": "[Pulizia Orfani] Trovato orfano in {0}: {1}",
        "orphan_total_found": "[Pulizia Orfani] Totale SavedVariables orfani: {0}",
        "orphan_moved_trash": "[Pulizia Orfani] Spostato nel cestino: {0}",
        "orphan_deleted": "[Pulizia Orfani] Eliminato: {0}",
        "orphan_error_deleting": "[Pulizia Orfani] Errore eliminazione {0}: {1}",
        "orphan_rebuilt_addons": "[Pulizia Orfani] Ricostruito: {0}",
        "orphan_error_writing_addons": "[Pulizia Orfani] Errore scrittura AddOns.txt {0}: {1}",
        "orphan_error_rebuild": "[Pulizia Orfani] Errore durante ricostruzione AddOns.txt: {0}",
        "new_setting_prefix": "[Nuovo] ",
        "details_colon": "Dettagli:",
        "updated_settings": "• Aggiornate {} impostazioni esistenti",
        "added_settings": "• Aggiunte {} nuove impostazioni",

        # Path Manager
        "select_wow_folder_title": "Seleziona cartella WoW",
        "unrecognized_installation": "Installazione non riconosciuta",
        "folder_not_valid_continue": "La cartella selezionata sembra non valida.\n\nVuoi continuare comunque?",
        "wow_folder_set": "Cartella WoW impostata: {}",

        # Performance
        "performance_execution_time": "[Prestazioni] {} ha richiesto {:.3f} secondi",
        "perf_moved_trash": "[{}] Spostato nel cestino: {}",
        "perf_deleted": "[{}] Eliminato: {}",
        "perf_error_deleting": "[{}] Errore eliminazione {}: {}",

        "select_valid_wow_optimizer": "Seleziona una cartella WoW valida nelle Opzioni per abilitare le visualizzazioni per versione.",
        "select_valid_wow_folder_cleaner": "Seleziona una cartella WoW valida nelle Opzioni per abilitare il Pulitore Cartelle.",

        # Main UI - Buttons and Messages
        "apply": "Applica",
        "cancel": "Annulla",
        "export_log": "Esporta registro",
        "clear_log": "Cancella registro",

        # Common Messages
        "no_files_selected": "Nessun file selezionato",
        "no_folders_selected": "Nessuna cartella selezionata",
        "no_orphans_selected": "Nessun orfano selezionato",

        # Common Messages
        "apply_font_question": "Applicare il carattere '{}' all'applicazione?",
        "select_valid_wow_first": "Si prega di selezionare prima una cartella WoW valida.",
        "restored": "Ripristinato",

        # File Cleaner
        "found_files_count": "Trovato {} file in tutte le versioni.",
        "confirm_action_files": "Sei sicuro di voler {} {} file?",
        "processed_files_count": "Elaborato {} file.",

        # Folder Cleaner
        "confirm_action_folders": "Sei sicuro di voler {} {} cartelle?",
        "processed_folders_count": "Elaborato {} cartelle.",

        # Orphan Cleaner
        "found_orphans_count": "Trovato {} SavedVariable orfano/i.",
        "confirm_action_orphans": "Sei sicuro di voler {} {} SavedVariables orfani?",
        "processed_orphans_count": "Elaborato {} orfano/i.",

        # Actions
        "move_to_trash": "spostare nel cestino",
        "delete_permanently_action": "eliminare permanentemente",

        # AddOns.txt Rebuild
        "rebuilt_addons_summary": "Voci AddOns.txt ricostruite.\nTotale scritto: {}\nTotale rimosso: {}",

        # Log Export
        "log_empty_nothing_export": "Il registro è vuoto. Niente da esportare.",

        # Settings Restore
        "settings_restored_restart": "Impostazioni ripristinate ai valori predefiniti. L'applicazione verrà riavviata ora.",
        "settings_restored_manual": "Impostazioni ripristinate ai valori predefiniti. Si prega di riavviare l'applicazione manualmente.",
        "failed_restore_defaults": "Impossibile ripristinare i valori predefiniti: {}",

        # File Cleaner

        # Folder Cleaner

        # Orphan Cleaner

        # Actions

        # AddOns.txt Rebuild

        # Log Export

        # Settings Restore

        # Orphan Cleaner Tab
        "orphan_description_part1": "Cerca SavedVariables di addon (.lua / .lua.bak) senza addon installato corrispondente (Interface/AddOns) in tutte le versioni WoW rilevate. Scansiona cartelle SavedVariables di account, server e personaggi. L'elaborazione ricostruisce anche AddOns.txt per corrispondere agli addon installati (preservando lo stato abilitato/disabilitato quando possibile).",
        "orphan_description_part2": "Nota: I file Blizzard_*.lua sono dati del gioco core e vengono automaticamente ignorati per sicurezza (ma i loro backup .lua.bak potrebbero essere eliminati).",
        "wtf_not_found": "Directory WTF non trovata. Avvia prima il gioco.",
        "unknown_preset": "Preset sconosciuto: {}",
        "backup_failed": "Creazione backup fallita: {}",
        "config_write_failed": "Scrittura configurazione fallita: {}",
        "config_updated": "{} impostazioni applicate a Config.wtf.",
        "settings_updated_added": "{} impostazioni aggiornate, {} nuove impostazioni aggiunte.",
        "backup_saved": " Backup salvato.",
        "version_path": "Versione: {}\nPercorso: {}",
        "optimizer_launch_required": "L'ottimizzatore richiede che {} sia stato avviato almeno una volta. Avvia WoW e raggiungi la schermata di selezione personaggio, poi esci dal gioco. Dopo di che, potrai usare l'ottimizzatore per applicare i preset grafici.",
        "system_matches": "Il tuo sistema corrisponde a: {}",
        "optimizer_title": "Ottimizzatore — {}",
        "recommendations_applied": "✓ Impostazioni consigliate applicate.",
        "applied_preset_log": "Preset {} applicato per {}",
        "apply_preset_failed_log": "Applicazione preset {} fallita: {}",
        "hardware_scan_complete": "Scansione hardware completata: salvato nelle impostazioni globali.",
        "hardware_scan_failed": "Scansione hardware fallita: {}",
        "scan_error": "✗ Errore: {}",

        # Game Validation
        "invalid_game_installation": "Installazione gioco non valida",
        "game_installation_incomplete": "L'installazione di World of Warcraft sembra incompleta.\n\nEsegui il gioco almeno una volta per inizializzare le cartelle Interface e WTF.\n\nDopo aver eseguito il gioco, potrai usare questo strumento per pulire la tua installazione.",

        # Startup Warning
        "user_disabled_warning": "L'utente ha disabilitato l'avviso di avvio.",

        # Update Checker
        "no_updates_available": "Nessun aggiornamento disponibile",
        "no_releases_published": "Stai eseguendo {}.\n\nNessuna release pubblicata ancora.",
        "update_check_failed": "Verifica aggiornamento fallita",
        "update_check_http_error": "Impossibile verificare aggiornamenti:\n\nHTTP {}: {}",
        "update_check_network_error": "Impossibile verificare aggiornamenti:\n\n{}",
        "update_check_error": "Errore verifica aggiornamento",
        "update_check_exception": "Errore durante verifica aggiornamenti:\n\n{}",
        "update_available": "Aggiornamento disponibile",
        "update_message": "È disponibile una nuova versione!\n\nVersione attuale: {}\nUltima versione: {}\n\nVuoi scaricarla ora?",
        "up_to_date": "Aggiornato",
        "up_to_date_message": "Stai eseguendo l'ultima versione ({}).",
        "browser_open_error": "Impossibile aprire il browser:\n\n{}",
        "download_update": "Scarica aggiornamento",
        "view_release": "Visualizza versione",
        "later": "Più tardi",
        "downloading_update": "Download aggiornamento",
        "downloading_update_file": "Download del file di aggiornamento...",
        "download_failed": "Download fallito",
        "download_failed_message": "Impossibile scaricare l'aggiornamento:\n\n{}",
        "update_ready": "Aggiornamento pronto",
        "update_downloaded_message": "Aggiornamento scaricato con successo!\n\nFile: {}\n\nVuoi installarlo ora?",
        "install_now": "Installa ora",
        "install_later": "Installa più tardi",
        "update_location": "Scaricato in: {}",
        "failed_to_fetch_release": "Impossibile recuperare le informazioni sulla versione da GitHub.",
        "no_download_available": "Nessun file scaricabile trovato per questa versione.",
        "install_update": "Installa aggiornamento",
        "please_run_installer": "La posizione di download è stata aperta.\n\nEsegui il programma di installazione per aggiornare l'applicazione.",
        "update_saved_message": "Aggiornamento salvato in:\n\n{}\n\nPuoi installarlo più tardi.",

        # File Cleaner - Log messages
        "file_cleaner_found_file": "[Pulizia File] Trovato file: {}",
        "file_cleaner_found": "[Pulizia File] Trovato: {}",
        "file_cleaner_total_found": "[Pulizia File] Totale file .bak/.old trovati: {}",
        "file_cleaner_moved_trash": "[Pulizia File] Spostato nel cestino: {}",
        "file_cleaner_deleted": "[Pulizia File] Eliminato: {}",
        "file_cleaner_error_deleting": "[Pulizia File] Errore eliminazione {}: {}",

        # Folder Cleaner - Log messages
        "folder_cleaner_found": "[Pulizia Cartelle] Trovato: {}",
        "folder_cleaner_total": "[Pulizia Cartelle] Totale cartelle pulibili: {}",
    },
}
