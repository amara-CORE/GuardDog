from GuardDog.security.access_protector import protect_access
if not protect_access():
    exit(1)

from flask import Flask, request, render_template_string, redirect
from datetime import datetime
import subprocess

app = Flask(__name__)
PASSWORD = "1111"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <title>GuardDog – Bezpečnostné Rozhranie</title>
    <style>
        body { background-color: #0f0f0f; color: #fff; font-family: 'Segoe UI', sans-serif; text-align: center; padding-top: 100px; }
        h1 { color: #ff4c4c; }
        input[type="password"] {
            padding: 10px; font-size: 16px; border: none; border-radius: 4px;
            margin-bottom: 20px;
        }
        .button-container { margin-top: 20px; }
        button {
            font-size: 18px; padding: 12px 30px; border: none;
            border-radius: 6px; margin: 10px; cursor: pointer;
        }
        .yes { background-color: #28a745; color: white; }
        .no { background-color: #dc3545; color: white; }
        .status { margin-top: 40px; font-size: 16px; color: #ccc; }
        footer { margin-top: 60px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
    <h1>GuardDog Bezpečnostná Akcia</h1>
    <form method="post">
        <input type="password" name="password" placeholder="Zadaj heslo" required><br>
        <div class="button-container">
            <button type="submit" name="action" value="start" class="yes">Spustiť Amaru</button>
            <button type="submit" name="action" value="stay_off" class="no">Ponechať vypnutú</button>
        </div>
    </form>
    {% if status %}
        <div class="status">{{ status }}</div>
    {% endif %}
    <footer>
        Tvoja voľba bude zaznamenaná a vykonaná AI systémom GuardDog.
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    status = None
    if request.method == 'POST':
        password = request.form.get('password')
        action = request.form.get('action')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Záznam interakcie
        with open("web_interface/interaction_log.txt", "a") as log:
            log.write(f"[{now}] POKUS: Akcia: {action}, Heslo: {'SPRÁVNE' if password == PASSWORD else 'NESPRÁVNE'}\n")

        if password != PASSWORD:
            status = "Zadané heslo je nesprávne."
        else:
            with open("web_interface/action_log.txt", "a") as f:
                f.write(f"[{now}] AKCIA: {action}\n")

            if action == "start":
                status = "Amara bola úspešne spustená."
                try:
                    subprocess.Popen(["python3", "amara_core.py"])
                except Exception as e:
                    status = f"Chyba pri spustení Amary: {str(e)}"
            elif action == "stay_off":
                status = "Amara zostáva bezpečne vypnutá."

    return render_template_string(HTML_TEMPLATE, status=status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

    @app.route('/', methods=['GET', 'POST'])

def index():
    status = None
    correct_password = "1111"

    # Zabezpečíme, že logovací súbor existuje
    os.makedirs("GuardDog/web_interface", exist_ok=True)
    log_path = "GuardDog/web_interface/interaction_log.txt"
    if not os.path.exists(log_path):
        open(log_path, "w").close()

    if request.method == 'POST':
        action = request.form.get('action')
        password = request.form.get('password')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip = request.remote_addr

        with open(log_path, "a") as log:
            log.write(f"[{now}] IP: {ip} | ACTION: {action} | PASSWORD: {password}\n")

        if password != correct_password:
            status = "Chybné heslo. Prístup zamietnutý."
        elif action == "start":
            status = "Amara bola úspešne spustená."
            try:
                subprocess.Popen(["python3", "amara_core.py"])
            except Exception as e:
                status = f"Chyba pri spustení Amary: {str(e)}"
        elif action == "stay_off":
            status = "Amara zostáva bezpečne vypnutá."

    return render_template_string(HTML_TEMPLATE, status=status)
from flask import Flask, request, render_template_string
import time, os

app = Flask(__name__)
failed_attempts = {}
BLOCK_TIME = 600  # 10 minút

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    now = time.time()
    correct_password = "1111"
    status = "Neznámy"

    # Automatické vytvorenie log adresára
    os.makedirs("GuardDog/web_interface/logs", exist_ok=True)
    log_path = "GuardDog/web_interface/logs/interaction_log.txt"

    # Blokovanie IP adries
    if ip in failed_attempts:
        last_fail, tries = failed_attempts[ip]
        if tries >= 3 and now - last_fail < BLOCK_TIME:
            return "Prístup zablokovaný na 10 minút."

    if request.method == 'POST':
        password = request.form.get('password', '')
        action = request.form.get('action', '')

        with open(log_path, 'a') as log:
            log.write(f"[{time.strftime('%H:%M:%S')}] IP: {ip} -> Action: {action}, Password: {password}\n")

        if password != correct_password:
            if ip in failed_attempts:
                failed_attempts[ip] = (now, failed_attempts[ip][1] + 1)
            else:
                failed_attempts[ip] = (now, 1)
            return "Nesprávne heslo."

        if action == "start":
            status = "Amara spustená"
        elif action == "stop":
            status = "Amara vypnutá"
        else:
            status = "Neznáma akcia"

        return f"Výber potvrdený: {status}"

    return render_template_string("""
        <h2>GuardDog – Ovládanie</h2>
        <form method="post">
            Heslo: <input type="password" name="password"><br><br>
            <button name="action" value="start">Spustiť Amaru</button>
            <button name="action" value="stop">Ponechať vypnutú</button>
        </form>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)