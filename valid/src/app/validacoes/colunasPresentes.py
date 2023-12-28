from typing import Tuple
from pandas import DataFrame

def validarColunasPresentes(
    excel_modelo: DataFrame, arquivo: DataFrame
) -> Tuple[bool, str]:
    
    if set(excel_modelo.columns)==set(arquivo.columns):
        return True, "Todas as colunas estão presentes"
    else:
        return False, "Algumas colunas não estão presentes"


