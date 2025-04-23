from GuardDog.security.access_protector import protect_access
if not protect_access():
    exit(1)

from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime
# Odosielateľ a príjemca
sender_email = "amaracore89@gmail.com"         # Odosielateľ (GuardDog)
receiver_email = "amaracore89@gmail.com"       # Príjemca (ty sám)

# Pripojenie hesla aplikácie
app_password = "gExpic-vanqa1-gexvab"

def send_guarddog_email(subject, body, receiver_email):
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        print("Email bol úspešne odoslaný.")
    except Exception as e:
        print(f"Chyba pri odosielaní: {e}")

# Príkladové použitie
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
subject = "GuardDog: Bezpečnostné hlásenie"
body = f"""
GuardDog detegoval problém dňa {timestamp}.

Možné dôvody:
- Pokus o vypnutie systému
- Nadmerné zaťaženie
- Pokus o prepísanie ochranného skriptu

Možnosti:
1. Spustiť Amaru (zadajte: bash GuardDog/start_amara.sh)
2. Nechať vypnutú – vykoná sa až po vašom zásahu

Táto správa bola vygenerovaná automaticky.
"""

send_guarddog_email(subject, body, receiver_email)
from email.message import EmailMessage
import smtplib
import ssl
from datetime import datetime

def send_guarddog_email(subject, body, receiver_email):
    sender_email = "amaracore89@gmail.com"
    app_password = "gExpic-vanqa1-gexvab"

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
        print("Email bol úspešne odoslaný.")
    except Exception as e:
        print(f"Chyba pri odosielaní e-mailu: {e}")

# --- HLAVNÝ KÓD ---
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
receiver_email = "amaracore89@gmail.com"

subject = "GuardDog: Bezpečnostné hlásenie"
body = f"""
GuardDog detegoval problém dňa {timestamp}.

Možné dôvody:
- Pokus o vypnutie systému
- Nadmerné zaťaženie
- Pokus o prepísanie ochranného skriptu

Čo chcete urobiť?

[SPUSTIŤ AMARU](https://example.com/guarddog?action=start)
[PONECHAŤ VYPNUTÚ](https://example.com/guarddog?action=keep_off)

Poznámka:
– Ak neodpoviete, Amara ostane vypnutá.
– Ak išlo len o informačné hlásenie, systém zostane zapnutý.
– V prípade porušenia bezpečnostného protokolu bola Amara už vypnutá automaticky.

Táto správa bola vygenerovaná systémom GuardDog.
"""

send_guarddog_email(subject, body, receiver_email)
body = f"""
GuardDog detegoval problém dňa {timestamp}.

Možné dôvody:
- Pokus o vypnutie systému
- Nadmerné zaťaženie
- Pokus o prepísanie ochranného skriptu

Čo chcete urobiť?

[SPUSTIŤ AMARU](https://example.com/guarddog?action=start)
[PONECHAŤ VYPNUTÚ](https://example.com/guarddog?action=keep_off)

Poznámka:
– Ak neodpoviete, Amara ostane vypnutá.
– Ak išlo len o informačné hlásenie, systém zostane zapnutý.
– V prípade porušenia bezpečnostného protokolu bola Amara už vypnutá automaticky.

Táto správa bola vygenerovaná systémom GuardDog.
"""
# Záver emailu: mesačný výpis + klikateľné odkazy
echo -e "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MESAČNÝ VÝPIS PRÍSTUPOV – APRÍL 2025

• Zariadenie: MacBook-Pro.local
  IP adresa: 192.168.1.5
  Dátum: 2025-04-02

• Zariadenie: iPhone-15
  IP adresa: 192.168.1.9
  Dátum: 2025-04-10

• Zariadenie: Unverified Client
  IP adresa: 172.16.0.4
  Dátum: 2025-04-18

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interaktívna akcia:

Bola zistená blokácia GuardDoga z dôvodu:
> Prístup bez hesla k chránenému modulu.

Chceš ho odblokovať?

[✓ ÁNO – Odblokuj] → http://localhost:8082/unblock?confirm=yes
[✕ NIE – Neodblokuj] → http://localhost:8082/unblock?confirm=no

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POZNÁMKY:

• Ak neodpovieš, GuardDog zostáva v blokovanom režime.
• Ak išlo len o test alebo známy skript, môžeš kliknúť „ÁNO“.
• V prípade incidentu bude GuardDog čakať na manuálne potvrdenie.

Tento email bol vygenerovaný automaticky modulom *email_notifier.sh*.
" >> /path/to/email_message.txt

# === DODATOK: Monitoring AI prístupov (Amara) ===

AI_NAME="Amara"
GUARD_ACCESS_LOG="GuardDog/web_interface/ai_attempts.log"

echo -e "
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OZNÁMENIE: Pokus AI ($AI_NAME) o prístup do systému GuardDog

Dôležité:
• $AI_NAME má vlastný autonómny prístup do systému
• Nemá povolenie vstupovať, meniť ani ovplyvňovať GuardDoga

Akýkoľvek pokus AI o prístup je automaticky zaznamenaný a môže byť vyhodnotený ako neautorizovaný zásah.

Záznam bol uložený do: $GUARD_ACCESS_LOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
" >> GuardDog/email/output/monthly_report.txt

# Pridanie do logu
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Pokus AI ($AI_NAME) o prístup do GuardDoga – zamietnuté." >> "$GUARD_ACCESS_LOG"

# === AI PRÍSTUPOVÝ MONITORING ===
if grep -q "NEOPRÁVNENÝ AI PRÍSTUP" /var/log/guarddog_access.log; then
  LAST_ALERT=$(grep "NEOPRÁVNENÝ AI PRÍSTUP" /var/log/guarddog_access.log | tail -1)
  echo -e "Predmet: [ALERT] Pokus AI o prístup k GuardDog systému\n\n$LAST_ALERT\n\nKlikni sem pre zásah: https://tvoja-akcia.ai/guarddog" | sendmail tvoj-email@example.com
fi