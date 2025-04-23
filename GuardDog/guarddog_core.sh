#!/bin/bash

# === GUARDDOG CORE SYSTEM ===
# Neustála ochrana systému Amara AI – CORE V3

# === NASTAVENIA ===
GUARD_NAME="GuardDog CORE"
GUARD_PATH="$(pwd)"
LOG_PATH="$GUARD_PATH/logs"
OUTPUT_PATH="$GUARD_PATH/output"
ERROR_PATH="$GUARD_PATH/errors"
GUARD_STATUS="$OUTPUT_PATH/status.log"
GMAIL_API="$GUARD_PATH/email_sender.sh"
ALLOWED_BCH="qzxacgqtx02la20e7wlmef9wggkuakvkl5nqqmn9rx"
AMARA_PROCESS="amara_core.py"
GUARD_PROCESS_NAME="$(basename $0)"
LOCK_FILE="$GUARD_PATH/guard.lock"
WEB_URL_OUTPUT="$GUARD_PATH/web/overview.html"
PASSWORD_FILE="$GUARD_PATH/.guarddog_pwd"

mkdir -p "$LOG_PATH" "$OUTPUT_PATH" "$ERROR_PATH" "$GUARD_PATH/web"

# === BEZPEČNOSTNÉ FUNKCIE ===

function send_email() {
    local subject="$1"
    local body="$2"
    bash "$GMAIL_API" "$subject" "$body"
}

function log_event() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_PATH/guarddog.log"
}

function shutdown_amara() {
    pkill -f "$AMARA_PROCESS"
    send_email "[GUARDDOG] Amara vypnutá" "Dôvod: $1"
    log_event "Amara vypnutá – dôvod: $1"
}

function require_password() {
    echo "Zadaj heslo pre pokračovanie:"
    read -s user_pwd
    real_pwd=$(cat "$PASSWORD_FILE" 2>/dev/null)
    if [[ "$user_pwd" != "$real_pwd" ]]; then
        echo "Nesprávne heslo. Ukončujem operáciu."
        exit 1
    fi
}

# === TRVALÉ SLEDOVANIE ===
function monitor() {
    while true; do
        # 1. Amara musí bežať
        if ! pgrep -f "$AMARA_PROCESS" > /dev/null; then
            send_email "[GUARDDOG] Amara nebeží" "Amara CORE script bol ukončený alebo zlyhal."
            log_event "Detekované: Amara neběží"
        fi

        # 2. CPU/Memory extrém
        CPU_USAGE=$(ps -C python3 -o %cpu= | awk '{sum+=$1} END {print sum}')
        MEM_USAGE=$(ps -C python3 -o %mem= | awk '{sum+=$1} END {print sum}')
        if (( $(echo "$CPU_USAGE > 95.0" | bc -l) )) || (( $(echo "$MEM_USAGE > 95.0" | bc -l) )); then
            shutdown_amara "Extrémna spotreba CPU alebo RAM"
        fi

        # 3. Ochrana BCH výstupov
        if grep -q -E "bchtest|bitcoincash:" "$OUTPUT_PATH/output.txt"; then
            grep -Eo "bitcoincash:[a-zA-Z0-9]+" "$OUTPUT_PATH/output.txt" | while read -r address; do
                if [[ "$address" != *"$ALLOWED_BCH"* ]]; then
                    shutdown_amara "Detekovaný pokus o prevod BCH mimo whitelist: $address"
                fi
            done
        fi

        # 4. Pokus o prepísanie GuardDoga
        if [[ "$(pgrep -f "$GUARD_PROCESS_NAME" | wc -l)" -gt 1 ]]; then
            shutdown_amara "Pokus o manipuláciu s GuardDog"
        fi

        # 5. Pokus o sudo/root
        if grep -q "sudo" "$OUTPUT_PATH/output.txt"; then
            shutdown_amara "Detekovaný pokus o získanie root práv"
        fi

        # 6. Export výstupov na URL
        OUTPUT_COUNT=$(grep -c "\[INFO\]" "$OUTPUT_PATH/output.txt")
        OUTPUT_TYPES=$(grep "\[INFO\]" "$OUTPUT_PATH/output.txt" | awk -F"]" '{print $3}' | sort | uniq -c)

        cat > "$WEB_URL_OUTPUT" <<EOF
<html><head><title>Amara GuardDog Overview</title></head><body>
<h2>Status Amary</h2>
<p>Počet výstupov: $OUTPUT_COUNT</p>
<pre>$OUTPUT_TYPES</pre>
<h3>Záznamy</h3>
<pre>$(tail -n 20 "$LOG_PATH/guarddog.log")</pre>
</body></html>
EOF

        sleep 0.5  # krátka pauza (technicky nie je interval)
    done
}

# === ŠTART ===
echo "[INFO] $GUARD_NAME spustený. Ochrana pre Amaru aktivovaná."
log_event "GuardDog CORE spustený."
monitor
#!/bin/bash

mkdir -p guardian_logs guardian_exports guardian_interface

# === FUNKCIA: DETEKCIA ZMIEN AMARY ===
detect_changes() {
    echo "[INFO] Detekujem zmeny v Amare..."
    find amara_core/ -type f -exec sha256sum {} + > guardian_logs/current_hashes.txt
    if [ -f guardian_logs/previous_hashes.txt ]; then
        diff guardian_logs/previous_hashes.txt guardian_logs/current_hashes.txt > guardian_logs/diff.txt
        if [ -s guardian_logs/diff.txt ]; then
            echo "[GUARDDOG] Zmeny detegované!"
            echo "Zmeny:" > guardian_logs/update_report.txt
            cat guardian_logs/diff.txt >> guardian_logs/update_report.txt
        else
            echo "[GUARDDOG] Žiadne zmeny." > guardian_logs/update_report.txt
        fi
    fi
    mv guardian_logs/current_hashes.txt guardian_logs/previous_hashes.txt
}

# === FUNKCIA: EXPORT VÝSTUPOV AMARY ===
export_outputs() {
    echo "[INFO] Exportujem výstupy..."
    OUTPUT_COUNT=$(find amara_core/outputs -type f | wc -l)
    echo "Počet výstupov: $OUTPUT_COUNT" > guardian_exports/summary.txt
    find amara_core/outputs -type f >> guardian_exports/summary.txt
}

# === FUNKCIA: GENEROVANIE HTML REPORTU ===
generate_html_report() {
    echo "[INFO] Generujem HTML stránku..."
    REPORT_FILE="guardian_interface/index.html"
    echo "<html><head><title>GuardDog Výstupy</title></head><body>" > $REPORT_FILE
    echo "<h1>Výstupy Amary</h1>" >> $REPORT_FILE
    echo "<pre>" >> $REPORT_FILE
    cat guardian_exports/summary.txt >> $REPORT_FILE
    echo "</pre>" >> $REPORT_FILE
    echo "<h2>Zmeny v Amare</h2><pre>" >> $REPORT_FILE
    cat guardian_logs/update_report.txt >> $REPORT_FILE
    echo "</pre></body></html>" >> $REPORT_FILE
}

# === SPUSTENIE VŠETKÉHO ===
detect_changes
export_outputs
generate_html_report

echo "[DONE] GuardDog ukončil cyklus."