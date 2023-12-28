from typing import Tuple
from pandas import DataFrame

def validarColunasPresentes(
    excel_modelo: DataFrame, arquivo: DataFrame
) -> Tuple[bool, str]:
    if not isinstance(arquivo, DataFrame):
        return False, "Arquivo não pôde ser lido corretamente. Certifique-se de que é um arquivo XLSX válido."

    if set(excel_modelo.columns) == set(arquivo.columns):
        return True, "Todas as colunas estão presentes"
    else:
        return False, "Algumas colunas não estão presentes"
    
    

