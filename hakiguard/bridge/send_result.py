import socket
import json
import os

SOCKET_PATH = "/var/run/hakiguard.sock"
#SOCKET_PATH = "/tmp/hakiguard.sock"

def send_to_router(result: dict):
    """
    Envia um dicionário 'result' para o listener via UNIX socket.
    Esse método é chamado automaticamente pela IA em inference.py.
    """

    # Garante que o socket existe
    if not os.path.exists(SOCKET_PATH):
        print(f"[HakiGuard] ERRO: socket {SOCKET_PATH} não encontrado.")
        return False

    try:
        # Cria o cliente UNIX
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)

        # Converte dict em JSON e envia
        payload = json.dumps(result).encode()
        client.sendall(payload)

        client.close()
        return True

    except Exception as e:
        print(f"[HakiGuard] Falha ao enviar dados para o router: {e}")
        return False

'''
# Teste manual
if __name__ == "__main__":

    exemplo = {
        "attack": True,
        "prob": 0.95,
        "source_ip": "192.168.1.50",
        "flow_id": "test-flow"
    }

    ok = send_to_router(exemplo)

    if ok:
        print("[HakiGuard] Envio de teste concluído.")
    else:
        print("[HakiGuard] Falha no envio.")
'''