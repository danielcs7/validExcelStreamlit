from typing import Tuple
from pandas import DataFrame

def validarQtdeLinhas(
    excel_modelo: DataFrame, arquivo: DataFrame
) -> Tuple[bool, str]:
    num_linhas_df1 = len(excel_modelo)
    num_linhas_df2 = len(arquivo)
    return num_linhas_df1 == num_linhas_df2, num_linhas_df2 - num_linhas_df1