import os
import pandas as pd
from functools import reduce

from pandas import DataFrame
from typing import List

# A classe View faz uso de um método que sincroniza seu estado interno com o
# banco de dados
#
# Como esta sincronização é feita em seu __init__(), é custoso e
# potencialmente flaky instanciá-la, e, só então, substituir o
# método da instância por outra versão para testes
#
# Portando, criamos uma função que substituirá a original durante a fixture
# por meio de patching/mocking
def cria_db_teste() -> List[DataFrame]:
    dfs = []

    caminho = './csv_teste'
    for csv in os.listdir(caminho):
        caminho_csv = os.path.join(caminho, csv)
        df = pd.read_csv(caminho_csv, sep=';')
        dfs.append(df)

    return reduce(lambda df1, df2: pd.merge(df1, df2, on='id', how='outer'),
                  dfs)

def _sincroniza_db(self):
    self._data = cria_db_teste()

