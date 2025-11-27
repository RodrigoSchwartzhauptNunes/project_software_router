#!/bin/sh

BASE_DIR="/root/hakiguard"
SOCKET_PATH="$BASE_DIR/var/run/hakiguard.sock"

LISTENER="$BASE_DIR/listener/hakiguard-listener.py"
DAEMON="$BASE_DIR/inference/inference_daemon.py"

LOGFILE="$BASE_DIR/var/log/hakiguard.log"
INFERENCE_LOG="$BASE_DIR/var/log/inference.log"

echo "[HakiGuard] Inicializando ambiente..."

# Garante diretórios
mkdir -p "$BASE_DIR/var/log"
mkdir -p "$BASE_DIR/var/run"
mkdir -p "$BASE_DIR/var/tmp"

# Remove socket antigo
if [ -e "$SOCKET_PATH" ]; then
    rm -f "$SOCKET_PATH"
fi


#############################################
### INICIAR O LISTENER
#############################################

echo "[HakiGuard] Iniciando listener..."
python3 "$LISTENER" >> "$LOGFILE" 2>&1 &


#############################################
### INICIAR DAEMON DE INFERENCE CONTÍNUA
#############################################

echo "[HakiGuard] Iniciando daemon de inference..."
python3 "$DAEMON" >> "$INFERENCE_LOG" 2>&1 &


#############################################
### FINAL
#############################################

echo "[HakiGuard] HakiGuard ativo e rodando."
sleep infinity
