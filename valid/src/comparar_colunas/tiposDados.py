from typing import Tuple
from pandas import DataFrame

def validarTiposDados(
    excel_modelo: DataFrame, arquivo: DataFrame
) -> Tuple[bool, str]:
    colunas_comuns = set(excel_modelo.columns).intersection(set(arquivo.columns))
    colunasTiposDif = [col for col in colunas_comuns if excel_modelo[col].dtype != arquivo[col].dtype]

    return len(colunasTiposDif) == 0,colunasTiposDif