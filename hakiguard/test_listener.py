import socket
import os
import json

SOCKET_PATH = "/tmp/hakiguard.sock"

# Remove socket antigo
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen()

print("[TEST LISTENER] Aguardando mensagem...")

while True:
    conn, _ = server.accept()
    data = conn.recv(8192)

    if data:
        try:
            obj = json.loads(data.decode())
            print("[TEST LISTENER] Recebido:", obj)
        except:
            print("[TEST LISTENER] Dados inválidos:", data)

    conn.close()
