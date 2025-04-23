from GuardDog.security.access_protector import protect_access
if not protect_access():
    exit(1)

import os
import time
import psutil
import hashlib
from datetime import datetime

MONITOR_INTERVAL = 10  # sekúnd
CPU_THRESHOLD = 90.0   # percent
RAM_THRESHOLD = 90.0   # percent
LOG_FILE = "GuardDog/monitoring/monitoring_log.txt"

MONITORED_FILES = {
    "GuardDog/guarddog_core.sh": None,
    "GuardDog/self_protect/self_protect.py": None,
    "GuardDog/email_notifier/email_notifier.py": None,
}

def calculate_checksum(file_path):
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
            return hashlib.sha256(file_data).hexdigest()
    except FileNotFoundError:
        return None

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a") as log:
        log.write(full_message)
    print(full_message.strip())

def monitor_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    if cpu_usage > CPU_THRESHOLD:
        log_event(f"VAROVANIE: CPU zaťaženie prekročilo limit ({cpu_usage}%)")

    if ram_usage > RAM_THRESHOLD:
        log_event(f"VAROVANIE: RAM zaťaženie prekročilo limit ({ram_usage}%)")

def monitor_files():
    for path in MONITORED_FILES:
        current_checksum = calculate_checksum(path)
        if MONITORED_FILES[path] is None:
            MONITORED_FILES[path] = current_checksum
            log_event(f"Zaznamenaný počiatočný stav súboru: {path}")
        elif current_checksum != MONITORED_FILES[path]:
            if current_checksum is None:
                log_event(f"UPOZORNENIE: Súbor bol vymazaný: {path}")
            else:
                log_event(f"UPOZORNENIE: Súbor bol zmenený: {path}")
            MONITORED_FILES[path] = current_checksum

def main():
    log_event("Monitoring engine spustený.")
    while True:
        try:
            monitor_resources()
            monitor_files()
            time.sleep(MONITOR_INTERVAL)
        except Exception as e:
            log_event(f"CHYBA v monitoringu: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main()