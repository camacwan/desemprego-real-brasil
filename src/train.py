# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 23:34:50 2026

@author: Cauan
"""
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error

def preparar_e_treinar():
    # 1. Carregar os dados processados
    try:
        df = pd.read_csv("data/processed/subutilizacao_uf.csv")
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Execute o extract.py primeiro!")
        return

    print(f"Total de registros carregados: {len(df)}")
    
    # Ordenar por UF e Trimestre para garantir a cronologia correta
    df = df.sort_values(by=['uf', 'trimestre']).reset_index(drop=True)

    # 2. Engenharia de Recursos Avançada (Lags por Estado)
    # Criamos variáveis defasadas: o que aconteceu 1 trimestre atrás e 1 ano atrás (4 trimestres) em cada UF
    df['lag_1'] = df.groupby('uf')['taxa_subutilizacao'].shift(1)
    df['lag_4'] = df.groupby('uf')['taxa_subutilizacao'].shift(4)
    
    # Remover linhas com valores nulos gerados pelos lags
    df = df.dropna().reset_index(drop=True)
    
    # Codificação da UF
    df['uf_encoded'] = df['uf'].astype('category').cat.codes

    # 3. Definindo X (Features) e y (Target)
    features = ['lag_1', 'lag_4', 'uf_encoded']
    X = df[features]
    y = df['taxa_subutilizacao']

    # 4. Divisão Temporal Correta (cortando por índice para respeitar o tempo)
    split_index = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

    # 5. Modelagem com XGBoost otimizado para regressão
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, max_depth=4)
    model.fit(X_train, y_train)

    # 6. Avaliação do Modelo
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    
    print("Modelo aprimorado treinado com sucesso!")
    print(f"MSE (Erro Quadrático Médio): {mse:.4f}")
    print(f"RMSE (Raiz do Erro Quadrático Médio): {rmse:.4f} pontos percentuais")

if __name__ == "__main__":
    preparar_e_treinar()