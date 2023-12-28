from typing import Tuple
from pandas import DataFrame

def validarColunasPresentesEmOrdem(
    excel_modelo: DataFrame, arquivo: DataFrame
) -> Tuple[bool, str]:
    
    if excel_modelo.columns.equals(arquivo.columns):
        return True, "As colunas estão em ordem"
    else:
        return False, "AS colunas não estão na mesma ordem"