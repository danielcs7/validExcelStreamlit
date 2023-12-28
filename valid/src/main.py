import streamlit as st
import os
import shutil
import time
from dotenv import load_dotenv
import pandas as pd
import tempfile  # Adicionando a importação do módulo tempfile
from loguru import logger
from comparar_colunas.colunasPresentes import validarColunasPresentes
from comparar_colunas.colunasPresentesNaMesmaOrdem import validarColunasPresentesEmOrdem
from comparar_colunas.existemColunasAmais import validarColunasAMais
from comparar_colunas.existemColunasAmenos import validarColunasAMenos
from comparar_colunas.quantidadeLinhas import validarQtdeLinhas
from comparar_colunas.tiposDados import validarTiposDados
from io import StringIO

load_dotenv()

input_dir = os.getenv('input_dir')
model_dir = os.getenv('model_dir')
outputCorretos = os.getenv('outputCorretos')
ouputRevisao = os.getenv('ouputRevisao')

excel_modelo = pd.read_excel(model_dir)

resultado = []
msg = []

def realizar_validacoes(excel_modelo, arquivo, filename):
    resultados = []
    testsFalhos = []

    if not isinstance(arquivo, pd.DataFrame):
        logger.error(f"Arquivo {filename} não pôde ser lido corretamente. Certifique-se de que é um arquivo XLSX válido.")
        return resultados, testsFalhos

    for idx, validacao in enumerate([validarColunasPresentes, 
                                    validarColunasPresentesEmOrdem, 
                                    validarColunasAMais, 
                                    validarColunasAMenos, 
                                    validarQtdeLinhas, 
                                    validarTiposDados], start=1):
        resultado, msg = validacao(excel_modelo, arquivo)
        if resultado:
            logger.info(f"Arquivo {filename} - teste {idx}, {validacao.__name__}:{msg}")
        else:
            logger.error(f"Arquivo {filename} - teste {idx}, {validacao.__name__}:{msg}")
            testsFalhos.append((validacao.__name__, msg))
            resultados.append(resultado)

    return resultados, testsFalhos

def main():
    st.title("Uploader de Arquivo XLSX")

    uploaded_file = st.file_uploader("Escolha um arquivo XLSX", type="xlsx")
    #uploaded_file = st.file_uploader("Faça upload de arquivos .xlsx", type="xlsx", accept_multiple_files=True)


    if uploaded_file is not None:
        st.success("Arquivo carregado com sucesso!")
        # Carregar o DataFrame a partir do arquivo XLSX
        # Criar um diretório temporário
        # Criar um diretório temporário
        temp_dir = tempfile.mkdtemp()

        # Salvar temporariamente o arquivo no diretório temporário
        temp_filepath = os.path.join(temp_dir, uploaded_file.name)
        uploaded_file.seek(0)
        with open(temp_filepath, 'wb') as temp_file:
            temp_file.write(uploaded_file.read())

        # Carregar o DataFrame a partir do arquivo XLSX
        df = pd.read_excel(temp_filepath)

        #df = pd.read_excel(uploaded_file)
        #df = uploaded_file
        # Obter apenas o nome do arquivo (sem a extensão .xlsx)
        filename_without_extension = os.path.splitext(os.path.basename(uploaded_file.name))[0]


        resultados, testsFalhos = realizar_validacoes(excel_modelo, df, filename_without_extension)

        # Exibir resultados no Streamlit
        st.subheader(f"Resultados para {filename_without_extension}:")
        if all(resultados):
            
            st.success(f"Arquivo {filename_without_extension} está em conformidade.")
            st.info("Todos os testes passaram.")
            #shutil.move(os.path.join(temp_filepath, filename_without_extension), outputCorretos)
            shutil.move(temp_filepath, os.path.join(outputCorretos, f"{filename_without_extension}.xlsx"))
        else:
            st.error(f"Arquivo {filename_without_extension} não está em conformidade. Erros nos testes:")
            for teste, erro in testsFalhos:
                st.error(f"- Teste {teste}: {erro}")
            #shutil.move(os.path.join(temp_filepath, filename_without_extension), ouputRevisao)
            shutil.move(temp_filepath, os.path.join(ouputRevisao, f"{filename_without_extension}.xlsx"))

        # Exibir mensagens de log no Streamlit
        st.subheader(f"Mensagens de Log para {filename_without_extension}:")
        #st.text_area("Log", value=log_messages)
        
        # Exibir algumas informações sobre o DataFrame
        st.subheader("Visualização do DataFrame:")
        st.write(df)

if __name__ == "__main__":
    main()
