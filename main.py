import json
import requests
import os
import time

import bot
import mail

LOG_FILE_PATH = "./.log"
CONFIG_FILE_PATH = "config.json"

LOG_MAX_UPDATES = 5
DAYS_AHEAD = 5
LOCATION = {
    "id": 3250,
    "name": "Stanwell Park"
}

def main():
    config = read_config()

    t_last_checked = get_log_last_atime()
    t_now = time.localtime(time.time())
    if less_than_24_hrs(t_now, t_last_checked):
        print_then_exit("Already checked today", 1)

    log_contents = read_log()
    update_str, days = new_update(t_now, config["ww_api_key"])
    log_contents.append(update_str)
    if len(log_contents) > LOG_MAX_UPDATES:
        log_contents = log_contents[-LOG_MAX_UPDATES:]

    overwrite_log(log_contents)
    msg = days_to_msg(days)
    subject = ""
    if (len(days) == 1): subject = f"{len(days)} Paragliding Day This Week"
    else: subject = f"{len(days)} Paragliding Days This Week"
    mail.send(config["bot_email"], config["user_email"], subject, msg)

def days_to_msg(days):
    if len(days) == 0: return "fucking shit"
    return '\n'.join([f"{day} looks good!" for day in days])

def read_config():
    config = None
    try:
        f = open(CONFIG_FILE_PATH, 'r')
        config = json.load(f)
        f.close()
    except:
        print_then_exit(f"ERROR: Could not read {CONFIG_FILE_PATH}", 0)

    required_keys = ["ww_api_key", "user_email", "bot_email"]
    if not all(key in config for key in required_keys):
        print_then_exit(f"ERROR: Missing fields in {CONFIG_FILE_PATH}. Please redownload.", 0)
    if config["ww_api_key"] == "" or config["ww_api_key"] == "?":
        print_then_exit(f"ERROR: Please input WillyWeather API key in {CONFIG_FILE_PATH}", 0)
    return config

def less_than_24_hrs(t1, t2):
    return False # bypass
    return t1.tm_year - t2.tm_year == 0 and t1.tm_yday - t2.tm_yday == 0

def print_then_exit(msg, exit_code):
    print(msg)
    print("EXITING")
    exit(exit_code)

def get_log_last_atime():
    try:
        log_st = os.stat(LOG_FILE_PATH)
        return time.localtime(log_st.st_atime)
    except:
        print_then_exit(f"ERROR: Could not find log file stats in {LOG_FILE_PATH}", 0)

def read_log():
    log_contents = []
    with open(LOG_FILE_PATH, "rt") as log:
        for line in log:
            log_contents.append(line)
    return log_contents

def new_update(t_now, api_key):
    update_str = f"Checked on {time.asctime(t_now)}"
    days = None
    try:
        days = bot.try_check_conditions(api_key, LOCATION["id"], LOCATION["name"], DAYS_AHEAD)
    except Exception as e:
        update_str += f" (FAILED) ({e})\n"
    else:
        update_str += " (SUCCESS)\n"
    return update_str, days

def overwrite_log(log_contents):
    with open(LOG_FILE_PATH, "wt") as log:
        for line in log_contents:
            log.write(line)

if __name__ == "__main__":
    main()

