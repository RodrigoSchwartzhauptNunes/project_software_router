import socket
import json
import os
import subprocess
import datetime

SOCKET_PATH = "/var/run/hakiguard.sock"
LOG_PATH = "/var/log/hakiguard.log"


def log(msg: str):
    """Registra mensagens em /var/log/hakiguard.log"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] {msg}\n"

    try:
        with open(LOG_PATH, "a") as f:
            f.write(linha)
    except:
        print("[HakiGuard] Falha ao escrever log.")


def apply_mitigation(ip: str):
    """Aplica regra de bloqueio usando nftables"""
    cmd = f"nft add rule inet filter input ip saddr {ip} drop"

    try:
        subprocess.call(cmd, shell=True)
        log(f"Mitigação aplicada: bloqueado {ip}")
    except Exception as e:
        log(f"Erro ao executar mitigação para IP {ip}: {e}")


def start_listener():
    """Cria e gerencia o socket do listener"""
    
    # Remove socket antigo
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen()

    log("HakiGuard Listener iniciado. Aguardando eventos...")

    while True:
        conn, _ = server.accept()
        data = conn.recv(16384)

        if not data:
            conn.close()
            continue

        try:
            payload = json.loads(data.decode())
            log(f"Alerta recebido: {payload}")
        except Exception as e:
            log(f"Erro ao decodificar JSON: {e}")
            conn.close()
            continue

        # Mitigação automática
        if payload.get("attack") is True:
            ip = payload.get("source_ip")
            if ip:
                apply_mitigation(ip)
            else:
                log("Alerta sem source_ip. Ignorado.")

        conn.close()


if __name__ == "__main__":
    start_listener()
