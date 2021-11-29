import pandas as pd
from copy import copy
from typing import List

from base_dados import Base_Midias

class View():
    _data: List[pd.DataFrame]
    _filtros: [str]

    _instancia: Base_Midias

    def __init__(self):
        self._filtros = []
        self._instancia = Base_Midias()
        self._sincroniza_db()

    def _sincroniza_db(self):
        # O código abaixo tem como objetivo obter os dataframes, atributos de Base_Midias, sem ter
        # que os referenciá-los diretamente. Assim, caso haja mudança no nome e/ou quantidade dos mesmos,
        # este método não será afetado

        self._instancia.atualiza_arquivos()
        # Obtem todos os atributos
        db_attr = dir(self._instancia)

        # Remove os métodos especiais como __init__ e __repr__
        db_attr_sem_especiais = filter(lambda attr: not attr.startswith('__') , db_attr)

        # Remove os métodos, deixando apenas os 'data attributes'
        db_data_attr = filter(lambda prop: not callable(getattr(self._instancia, prop)), db_attr_sem_especiais)

        self._data =  [getattr(self._instancia, df_name) for df_name in db_data_attr]

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
