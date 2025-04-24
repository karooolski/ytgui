class Debug:
    make_logs = True
    show_cmd_details = True
    append_debug_details_to_logs = True
    stop_downloading = False
    break_downloading = False
    run_gui = True

def is_download_stopped():
    if Debug.break_downloading == True:
        return True
    return False
