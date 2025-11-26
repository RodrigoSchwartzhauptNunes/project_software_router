#!/bin/sh

INTERFACE=$(cat hakiguard/capture/interface.conf)
PCAP_DIR="hakiguard/capture/pcap/"
FILE="capture_$(date +%F_%H-%M-%S).pcap"

mkdir -p "$PCAP_DIR"

if [ -z "$INTERFACE" ]; then
    echo "[HakiGuard-Capture] Interface não definida em capture/interface.conf"
    exit 1
fi

echo "[HakiGuard-Capture] Iniciando captura na interface: $INTERFACE"
echo "[HakiGuard-Capture] Arquivo: $PCAP_DIR$FILE"

# Captura de tráfego usando tcpdump (promíscuo)
sudo tcpdump -i "$INTERFACE" -w "$PCAP_DIR$FILE" -U -n
