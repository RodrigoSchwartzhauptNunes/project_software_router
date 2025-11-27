#!/bin/sh

# Caminhos locais ao módulo cicflowmeter
BASE_DIR="$(dirname $0)"
VENV="$BASE_DIR/venv/bin/activate"
CICFM="$BASE_DIR/venv/bin/cicflowmeter"
OUTPUT_DIR="$BASE_DIR/output/"
INTERFACE=$(cat "$BASE_DIR/../capture/interface.conf")

# Verifica interface
if [ -z "$INTERFACE" ]; then
    echo "[HakiGuard] Interface não definida em hakiguard/capture/interface.conf"
    exit 1
fi

# Verifica venv/cicflowmeter
if [ ! -f "$CICFM" ]; then
    echo "[HakiGuard] cicflowmeter não encontrado no venv:"
    echo "→ Rode: source hakiguard/cicflowmeter/venv/bin/activate && pip install cicflowmeter"
    exit 1
fi

echo "[HakiGuard] Usando venv localizado em: $VENV"
echo "[HakiGuard] Rodando CICFlowMeter na interface: $INTERFACE"
echo "[HakiGuard] Saída: $OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR"

# Ativa venv e roda o cicflowmeter
. "$VENV" && \
    cicflowmeter -i "$INTERFACE" -c  "$OUTPUT_DIR/flows_$(date +%F_%H-%M-%S).csv"
