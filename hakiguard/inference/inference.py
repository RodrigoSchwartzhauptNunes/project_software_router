import os
import json
import pickle
import numpy as np

from utils.preprocess import preprocess_flow
from utils.load_flow import load_last_flow
from bridge.send_result import send_to_router


MODELS_DIR = "hakiguard/models/"
FLOW_PATH = "hakiguard/cicflowmeter/output/"


def load_pickle(path):
    """Carrega arquivos pickle (modelos e scaler)."""
    with open(path, "rb") as f:
        return pickle.load(f)


def load_models():
    """Carrega SOMENTE o RandomForest e o Scaler.
       A LinearRegressionPARA TESTES FUTUROS.
    """

    rf = load_pickle(os.path.join(MODELS_DIR, "random_forest_model.pkl"))
    scaler = load_pickle(os.path.join(MODELS_DIR, "scaler.pkl"))

    # lr = load_pickle(os.path.join(MODELS_DIR, "linear_regression_model.pkl"))
    # return rf, lr, scaler

    return rf, None, scaler  # lr = None


def run_inference():
    """Executa toda a pipeline de inferência."""

    # 1. Carregar modelo RandomForest e scaler
    random_forest, linear_regression, scaler = load_models()

    # 2. Ler o último flow gerado pelo CICFlowMeter
    flow = load_last_flow(FLOW_PATH)

    if flow is None:
        print("[HakiGuard-Inference] Nenhum flow encontrado.")
        return

    # 3. Preprocessamento (garante consistência com o treinamento)
    features = preprocess_flow(flow)

    # Converter para formato de input do modelo
    features_scaled = scaler.transform([features])

    # 4. Previsão 
    pred_rf = random_forest.predict(features_scaled)[0]

    # ESSE NÃO EPRFFOMOU MUITO  VOU REALIZAR MAIS TESTES DE PORCENTAGEM DE TREINO MAIS TARDE
    # pred_lr = linear_regression.predict(features_scaled)[0] if linear_regression else None

    # 5. Decisão (threshold simples)
    attack_detected = pred_rf >= 0.5

    result = {
        "attack": bool(attack_detected),
        "prob": float(pred_rf),