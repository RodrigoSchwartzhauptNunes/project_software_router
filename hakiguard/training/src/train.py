################################
#By: Rodrigo Schwartzhaupt Nunes
################################
#Treinamento de AI
################################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import RobustScaler
import numpy as np
import joblib
import os

#Importando aquivo
file_path = '/app/dataset/Portmap.csv'
data = pd.read_csv(file_path, low_memory=False)  # Definindo low_memory como False

data_filtered = data.iloc[:, 3:]

# Calcula a matriz de correlação
data_filtered = data_filtered.select_dtypes(include=['float64', 'int64'])
data_filtered = pd.get_dummies(data_filtered)

# Definindo o número da coluna que você quer prever (última coluna)
target_column_number = -1  # Índice da última coluna
x = data_filtered.drop(data_filtered.columns[target_column_number], axis=1)
y = data_filtered.iloc[:, target_column_number]

# Divisão em treinamento e teste
x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.2, random_state=42)

# Substituir infinitos por NaN
x_treino = x_treino.replace([np.inf, -np.inf], np.nan)
x_teste = x_teste.replace([np.inf, -np.inf], np.nan)

# Preencher NaNs com a média dos valores
x_treino = x_treino.fillna(x_treino.mean())
x_teste = x_teste.fillna(x_treino.mean())

# Escala dos dados usando RobustScaler
scaler = RobustScaler()
x_treino_scaled = scaler.fit_transform(x_treino)
x_teste_scaled = scaler.transform(x_teste)

# Criação e treinamento do modelo
modelo_arvoredecisao = RandomForestRegressor(random_state=42)
modelo_arvoredecisao.fit(x_treino_scaled, y_treino)
#modelo_regresaolinear = LinearRegression(random_state=42) ##retirado para teste da linha seguinte
modelo_regresaolinear = LinearRegression()
modelo_regresaolinear.fit(x_treino_scaled, y_treino)


# Realiza as previsões
previsao_arvoredecisao = modelo_arvoredecisao.predict(x_teste_scaled)
previsao_regresaolinear = modelo_regresaolinear.predict(x_teste_scaled)

#mostra porcentagem de acerto na tela
from sklearn.metrics import r2_score
print(r2_score(y_teste, previsao_arvoredecisao))
print(r2_score(y_teste, previsao_regresaolinear))

# Avaliação do modelo
tabela_aux = pd.DataFrame()
tabela_aux['y_teste'] = y_teste
tabela_aux['previsao_arvoredecisao'] = previsao_arvoredecisao
tabela_aux['previsao_regresaolinear'] = previsao_regresaolinear

plt.figure(figsize=(15, 6))
sns.lineplot(data=tabela_aux)
#plt.show() #retirado para salvar em um png linha seguinte
plt.savefig("output/grafico.png")

##salvando os modelos
# Diretório onde o modelo será salvo (volume montado)
model_dir = "/app/models"

# Salvando modelos
joblib.dump(modelo_arvoredecisao, f"{model_dir}/random_forest_model.pkl")
joblib.dump(modelo_regresaolinear, f"{model_dir}/linear_regression_model.pkl")

# Salvando também o scaler
joblib.dump(scaler, f"{model_dir}/scaler.pkl")

print("Modelos salvos em /app/models:")
print(os.listdir(model_dir))