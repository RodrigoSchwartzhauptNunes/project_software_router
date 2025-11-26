#!/bin/sh

##IP="$1"
##LOG="/var/log/hakiguard.log"
##
##echo "[HakiGuard Rule] Aplicando rate-limit para $IP" >> $LOG
##
### Cria tabela e cadeia se ainda não existirem (idempotente)
##nft list table inet hakiguard 2>/dev/null >/dev/null || nft add table inet hakiguard
##nft list chain inet hakiguard ratelimit 2>/dev/null >/dev/null || nft add chain inet hakiguard ratelimit { type filter hook input priority 0 \; }
##
### Adiciona regra de rate limit simples:
### Permite apenas 20 pacotes por segundo com burst de 40
##nft add rule inet hakiguard ratelimit ip saddr $IP limit rate 20/second burst 40 packets accept
##
##echo "[HakiGuard Rule] Rate-limit ativo para IP: $IP (20pps, burst 40)" >> $LOG
##