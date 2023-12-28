import os
import pandas as pd

def obter_colunas(arquivo):
    # Lê o arquivo Excel e retorna as colunas como uma lista
    df = pd.read_excel(arquivo)
    return df.columns.tolist()

def comparar_colunas(modelo, pasta):
    # Obtém as colunas do modelo
    colunas_modelo = obter_colunas(modelo)

    # Lista para armazenar os resultados
    resultados = {}

    # Itera sobre os arquivos na pasta
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.xlsx'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            colunas_arquivo = obter_colunas(caminho_arquivo)

            # Compara as colunas do arquivo com as do modelo
            if colunas_arquivo == colunas_modelo:
                resultados[arquivo] = "Colunas iguais"
            else:
                resultados[arquivo] = "Colunas diferentes"

    return resultados
