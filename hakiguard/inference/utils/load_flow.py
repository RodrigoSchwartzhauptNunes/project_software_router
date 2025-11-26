import os
import csv

def load_last_flow(path):
    """
    Carrega o último flow gerado pelo CICFlowMeter.
    Retorna um dicionário com os campos do CSV.
    """

    if not os.path.exists(path):
        print("[HakiGuard-LoadFlow] Caminho não encontrado:", path)
        return None

    # listar arquivos .csv
    files = [f for f in os.listdir(path) if f.endswith(".csv")]

    if not files:
        print("[HakiGuard-LoadFlow] Nenhum arquivo CSV encontrado.")
        return None

    # último arquivo modificado
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    last_file = os.path.join(path, files[-1])

    try:
        with open(last_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            if not rows:
                print("[HakiGuard-LoadFlow] CSV vazio:", last_file)
                return None

            # retorna o último flow registrado
            return rows[-1]

    except Exception as e:
        print("[HakiGuard-LoadFlow] Erro ao ler CSV:", e)
        return None
