import json
import requests
import os
import time
import bot

LOG_MAX_UPDATES = 5
DAYS_AHEAD = 5
LOCATION = {
    "id": 3250,
    "name": "Stanwell Park"
}

def main():
    log_file_path = "./.log"
    auth_file_path = "./auth.txt"

    api_key = read_api_key(auth_file_path)

    t_last_checked = get_log_last_atime(log_file_path)
    t_now = time.localtime(time.time())
    if less_than_24_hrs(t_now, t_last_checked):
        print_then_exit("Already checked today", 1)

    log_contents = read_log(log_file_path)
    update_str = new_update(t_now, api_key)
    log_contents.append(update_str)
    if len(log_contents) > LOG_MAX_UPDATES:
        log_contents = log_contents[-LOG_MAX_UPDATES:]

    overwrite_log(log_file_path, log_contents)

def less_than_24_hrs(t1, t2):
    return False # bypass
    return t1.tm_year - t2.tm_year == 0 and t1.tm_yday - t2.tm_yday == 0

def print_then_exit(msg, exit_code):
    print(msg)
    print("EXITING")
    exit(exit_code)

def read_api_key(auth_file_path):
    with open(auth_file_path) as f:
        api_key = f.read()[10:]
        if api_key == "" or api_key == "?":
            print_then_exit(f"ERROR: Please input API_KEY in {auth_file_path}", 0)
    return api_key

def get_log_last_atime(log_file_path):
    try:
        log_st = os.stat(log_file_path)
        return time.localtime(log_st.st_atime)
    except:
        print_then_exit("ERROR: Could not find log file stats", 0)

def read_log(log_file_path):
    log_contents = []
    with open(".log", "rt") as log:
        for line in log:
            log_contents.append(line)
    return log_contents

def new_update(t_now, api_key):
    update_str = f"Checked on {time.asctime(t_now)}"
    try:
        bot.try_check_conditions(api_key, LOCATION["id"], LOCATION["name"], DAYS_AHEAD)
    except Exception as e:
        update_str += f" (FAILED) ({e})\n"
    else:
        update_str += " (SUCCESS)\n"
    return update_str

def overwrite_log(log_file_path, log_contents):
    with open(log_file_path, "wt") as log:
        for line in log_contents:
            log.write(line)

if __name__ == "__main__":
    main()

