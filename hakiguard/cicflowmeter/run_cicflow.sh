#!/bin/sh

CICFM="hakiguard/cicflowmeter/CICFlowMeter-4.0/bin/CICFlowMeter"
OUTPUT_DIR="hakiguard/cicflowmeter/output/"
INTERFACE=$(cat hakiguard/capture/interface.conf)

if [ ! -f "$CICFM" ]; then
    echo "[HakiGuard] CICFlowMeter não encontrado em $CICFM"
    exit 1
fi

if [ -z "$INTERFACE" ]; then
    echo "[HakiGuard] Interface não definida em hakiguard/capture/interface.conf"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "[HakiGuard] Rodando CICFlowMeter na interface: $INTERFACE"
echo "[HakiGuard] Saída: $OUTPUT_DIR"

sudo "$CICFM" -i "$INTERFACE" -o "$OUTPUT_DIR"
