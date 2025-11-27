#!/usr/bin/env python3
import os
import time
import subprocess
import logging

BASE_DIR = "/root/hakiguard"
INFERENCE_SCRIPT = f"{BASE_DIR}/inference/inference.py"
FLOW_DIR = f"{BASE_DIR}/var/tmp"
LOG_PATH = f"{BASE_DIR}/var/log/inference.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_flow_file(file_path):
    logging.info(f"[HakiGuard-Inference] Processando arquivo: {file_path}")

    try:
        subprocess.run(
            ["python3", INFERENCE_SCRIPT, file_path],
            check=True
        )
        logging.info(f"[HakiGuard-Inference] Arquivo processado com sucesso: {file_path}")
    except Exception as e:
        logging.error(f"[HakiGuard-Inference] ERRO no processamento: {e}")

    try:
        os.remove(file_path)
        logging.info(f"[HakiGuard-Inference] Arquivo removido: {file_path}")
    except:
        logging.error(f"[HakiGuard-Inference] Falha ao remover: {file_path}")


def start_daemon():
    logging.info("[HakiGuard-Inference] Daemon iniciado e monitorando flows...")

    while True:
        try:
            files = [f for f in os.listdir(FLOW_DIR) if f.endswith(".csv")]
        except Exception as e:
            logging.error(f"[HakiGuard-Inference] Erro lendo diretório: {e}")
            time.sleep(2)
            continue

        for file in files:
            full_path = os.path.join(FLOW_DIR, file)
            process_flow_file(full_path)

        time.sleep(1)


if __name__ == "__main__":
    start_daemon()
