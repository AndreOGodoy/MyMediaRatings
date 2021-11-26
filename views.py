import pandas as pd
from copy import copy

class View():
    _data: pd.DataFrame
    _filtros: [str]
    
    def __init__(self):
        self._sincroniza_db()
        self._filtros = []

    def _sincroniza_db(self):
        # Conexão com DB ainda não integrada
        self._data = pd.DataFrame()

    @property
    def filtros(self):
        return copy(self._filtros)

    @filtros.setter
    def filtros(self, novos_filtros: [str]):
        self._filtros = copy(novos_filtros)
        
    def obtem_filtros_possiveis(self) -> [str]:
        return [filtro for filtro in list(self._data.columns) if filtro not in self._filtros]

    def aplica_filtro(self, filtro: str):
        self._filtros.append(filtro)
    
    def print_data(self):
        print(self._data)
