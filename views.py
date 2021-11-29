import pandas as pd
from copy import copy
from typing import List

from base_dados import Base_Midias

class View():
    _data: List[pd.DataFrame]
    _filtros: [str]
    
    def __init__(self):
        self._sincroniza_db()
        self._filtros = []

    def _sincroniza_db(self):
        # Conexão com DB ainda não integrada
        self._data = [pd.DataFrame()]

    @property
    def filtros(self):
        return copy(self._filtros)

    @filtros.setter
    def filtros(self, novos_filtros: [str]):
        self._filtros = copy(novos_filtros)
        
    def obtem_filtros_possiveis(self) -> [str]:
        colunas = []
        for df in self._data:
            colunas.extend(df.columns)

        colunas_unicas = list(set(colunas))

        return [filtro for filtro in colunas_unicas if filtro not in self._filtros]

    def aplica_filtro(self, filtro: str):
        self._filtros.append(filtro)
    
    def print_data(self):
        print(self._data)
