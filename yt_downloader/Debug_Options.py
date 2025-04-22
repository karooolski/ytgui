class Debug:
    make_logs = False
    show_cmd_details = True
    append_debug_details_to_logs = False
    stop_downloading = False
    break_downloading = False
    run_gui = True

def is_download_stopped():
    if Debug.break_downloading == True:
        return True
    return False
