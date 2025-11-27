#!/bin/sh

#
# HakiGuard - rate limiting rule
# Uso:
#    sh rate_limit.sh <IP> <probabilidade>
#

IP="$1"
PROB="$2"

# Arquivos de estado
STATE_DIR="hakiguard/var/state"
mkdir -p "$STATE_DIR"

BLACKLIST="$STATE_DIR/blocked_ips.txt"

# Chain exclusiva do HakiGuard
CHAIN="hakiguard_ratelimit"

# Se o IP não foi passado, sai
if [ -z "$IP" ]; then
    echo "[HakiGuard] Nenhum IP recebido para rate-limit."
    exit 1
fi

echo "[HakiGuard] Aplicando rate-limit ao IP: $IP (prob: $PROB)"

# Marca IP como bloqueado
echo "$IP" >> "$BLACKLIST"

# Cria tabela e chain se não existirem
nft list table inet hakiguard >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[HakiGuard] Criando tabela nftables 'hakiguard'"
    nft add table inet hakiguard
fi

nft list chain inet hakiguard $CHAIN >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[HakiGuard] Criando chain de rate-limit: $CHAIN"
    nft add chain inet hakiguard $CHAIN "{ type filter hook prerouting priority 0; }"
fi

# Evita duplicação da regra para o mesmo IP
EXISTS=$(nft list chain inet hakiguard $CHAIN | grep "$IP")
if [ ! -z "$EXISTS" ]; then
    echo "[HakiGuard] Regra já existe para $IP. Nada a fazer."
    exit 0
fi

# Adiciona rate limit
# Limite: 100 pacotes por segundo (ajustável)
echo "[HakiGuard] Adicionando regra de rate limit para $IP"
nft add rule inet hakiguard $CHAIN ip saddr $IP limit rate 100/second accept
nft add rule inet hakiguard $CHAIN ip saddr $IP drop

echo "[HakiGuard] Rate-limit aplicado com sucesso."
exit 0
