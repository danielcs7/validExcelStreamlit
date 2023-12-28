from typing import Tuple
from pandas import DataFrame

def validarColunasAMenos(
    excel_modelo: DataFrame, arquivo: DataFrame
) -> Tuple[bool, str]:
    colunasAmais = set(arquivo.columns) - set(excel_modelo.columns)
    return len(colunasAmais) ==0, list(colunasAmais)