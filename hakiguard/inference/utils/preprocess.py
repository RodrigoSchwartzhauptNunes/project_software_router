import numpy as np

# LISTA DE FEATURES USADAS NO TREINAMENTO
# Ajuste esta lista conforme os nomes do seu dataset final.
FEATURES = [
    "Flow Duration",
    "Tot Fwd Pkts",
    "Tot Bwd Pkts",
    "TotLen Fwd Pkts",
    "TotLen Bwd Pkts",
    "Fwd Pkt Len Max",
    "Fwd Pkt Len Min",
    "Bwd Pkt Len Max",
    "Bwd Pkt Len Min",
    "Flow Byts/s",
    "Flow Pkts/s",
    "Flow IAT Mean",
    "Fwd IAT Total",
    "Bwd IAT Total",
    "Fwd PSH Flags",
    "Bwd PSH Flags",
    "Init Fwd Win Byts",
    "Init Bwd Win Byts"
]

def convert(value):
    """Converte valores para float, tratando erros."""
    try:
        return float(value)
    except:
        return 0.0


def preprocess_flow(flow_dict):
    """
    Recebe um flow em formato dict (carregado do CSV),
    extrai somente as features usadas no treinamento
    e converte para lista numérica na ordem correta.
    """

    features = []

    for f in FEATURES:
        raw_value = flow_dict.get(f, 0)
        value = convert(raw_value)
        features.append(value)

    return np.array(features)
