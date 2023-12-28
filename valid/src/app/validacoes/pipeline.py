import os
import shutil
import time
import os

print(os.environ)


from loguru import logger
import pandas as pd
from loguru import logger
import colunasPresentes as validarColunasPres
import colunasPresentesNaMesmaOrdem as validColunasOrdem
import existemColunasAmais as validColunasMais
import existemColunasAmenos as validColunasMenos
import quantidadeLinhas as validQtLinhas
import tiposDados as validDtypes


#from .config import input_dir, model_dir,ouputRevisao,outputCorretos
#from validacoes import validarColunasAMais,validarColunasAMenos,validarColunasPresentes,validarColunasPresentesEmOrdem,validarQtdeLinhas,validarTiposDados


input_dir      = os.environ['input_dir']
model_dir      = os.environ['model_dir']
outputCorretos = os.environ['outputCorretos']
ouputRevisao   = os.environ['ouputRevisao']

resultado = []
resultados = []
testsFalhos = []

#LENDO O ARQUIVO MODELO
excel_modelo = pd.read_excel(f'{model_dir}')

# LISTA PARA ARMAZENAR OS NOMES DOS ARQUIVOS
fileNames = []

for filename in os.listdir(input_dir):
    if filename.endswith('.xlsx'):
        fileNames.append(filename)

fileNames.sort()

arquivosRecebidos = [
    (filename, pd.read_excel(os.path.join(input_dir, filename)))
    for filename in fileNames
]

validacoes = [
    validarColunasPres,
    validColunasOrdem,
    validColunasMais,
    validColunasMenos,
    validQtLinhas,
    validDtypes
]

for i,(filename, arquivo) in enumerate(arquivosRecebidos, start=1):
    log_file_name = f'auditoria:{filename[:-5]}-data:{time.strftime("%Y-%m-%d")}.log'

    logger.remove()
    logger.add(
        log_file_name,
        level='INFO',
        format='{time: YYYY-MM-DDTHH} | {level} | {message}',
    )

    resultados = validarColunasPres(excel_modelo,arquivo)



resultado = []
msg = []



'''
for idx, validacao in enumerate(validarColunasPres(), start=1):
    resultado, msg = validacao(excel_modelo,arquivo)
    if resultado:
        logger.info(f"Arquivo {filename} - teste {idx}, {validacao,__name__}:{msg}")
    else:
        logger.error(f"Arquivo {filename} - teste {idx}, {validacao,__name__}:{msg}")
        testsFalhos.append(idx)
        resultados.append(resultado)

'''
if all(resultados):
    logger.info(f"Todos os testes passaram")
    shutil.mov(input_dir,outputCorretos)
else:
    logger.critical(f"Um ou mais testes não passaram")
    shutil.mov(input_dir,ouputRevisao)
