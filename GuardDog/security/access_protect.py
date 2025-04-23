from GuardDog.security.access_protector import protect_access
if not protect_access():
    exit(1)

import os
import sys
import getpass
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Nastavenie
CORRECT_PASSWORD = "1111"
ALLOWED_SCRIPT = "guarddog_core.sh"
BLOCK_FILE = "GuardDog/.blocked"
LOG_FILE = "GuardDog/access_logs.txt"
EMAIL_TO = "your@email.com"
EMAIL_FROM = "guarddog@system.local"
UNBLOCK_LINK = "https://yourdomain.com/unblock_guarddog"  # zmeň neskôr

def is_guarddog_core():
    return os.path.basename(sys.argv[0]) == ALLOWED_SCRIPT

def is_blocked():
    return os.path.exists(BLOCK_FILE)

def log_access(status, ip="local"):
    os.makedirs("GuardDog", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] STATUS: {status} | IP: {ip}\n")

def send_email(subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        with smtplib.SMTP("localhost") as server:
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

def protect_access():
    if is_guarddog_core():
        log_access("ALLOWED: CORE EXEMPTION")
        return True

    if is_blocked():
        log_access("DENIED: BLOCKED")
        send_email(
            "GuardDog blokovaný",
            f"Prístup bol zablokovaný po zlom hesle.\n\nOdomknúť: {UNBLOCK_LINK}"
        )
        print("GuardDog je zablokovaný. Pozri si email.")
        return False

    password = getpass.getpass("Zadaj GuardDog heslo: ")
    if password != CORRECT_PASSWORD:
        log_access("DENIED: WRONG PASSWORD")
        open(BLOCK_FILE, "w").close()
        send_email(
            "GuardDog prístup odmietnutý",
            f"Nesprávne heslo. Prístup bol zablokovaný.\n\nOdomknúť: {UNBLOCK_LINK}"
        )
        print("Zlé heslo. GuardDog zablokovaný.")
        return False

    log_access("ALLOWED")
    return True

def monthly_summary():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    now = datetime.now()
    one_month_ago = now - timedelta(days=30)
    relevant_logs = [line for line in lines if datetime.strptime(line[1:20], "%Y-%m-%d %H:%M:%S") >= one_month_ago]

    summary = "\n".join(relevant_logs)
    send_email("Mesačný výpis GuardDog prístupov", summary or "Žiadne prístupy za posledný mesiac.")

# Spusti len ak beží samostatne
if __name__ == "__main__":
    if protect_access():
        print("Prístup povolený.")
    else:
        sys.exit(1)

        # === POST-KONTROLA: AK BOL DETEGOVANÝ NEOPRÁVNENÝ AI PRÍSTUP, SPUSTÍ SA NOTIFIKAČNÝ MODUL ===
# Tento krok zabezpečí, že ak Amara alebo iná AI jednotka poruší prístupové pravidlá,
# GuardDog automaticky vykoná shell skript, ktorý skontroluje log a pošle e-mail.

try:
    notifier_script = "/workspaces/legendary/guarddog/email_notifier.sh"
    os.system(f"bash {notifier_script} >/dev/null 2>&1")
except Exception as e:
    # Nepretŕha ochranu, len zaznamená tichú chybu (ak by skript chýbal)
    with open(LOG_FILE, "a") as log:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{now}] CHYBA PRI SPUSTENÍ NOTIFIKÁCIE: {str(e)}\n")