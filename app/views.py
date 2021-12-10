import pandas as pd
from copy import copy
from functools import reduce
from typing import List, Optional, Callable

from app.base_dados import Base_Midias

# Esta classe é utilizada para organização interna
#
# Ela é instanciada no momento que o módulo for importado pelo cliente,
# fazendo com que carregue os dados do banco de dados
#
# Ela é uma instância única compartilhada entre todas as Views, e
# Seu objetivo é impedir que haja varios carregamentos
# distindos da mesma informação à memória

class _ViewCache():
    _instancia: Base_Midias
    _dfs: List[pd.DataFrame]

    def __init__(self):
        self._dfs = []

    def atualiza(self):
        self._instancia = Base_Midias('csv/')
        self._dfs = self._instancia.retorna_dataframes()

    def obtem_dbs(self):
        self.atualiza()

        return self._dfs

class FiltroInexistenteException(Exception):
    filtro_inexistente: str

    def __init__(self, filtro_inexistente: str):
        self.filtro_inexistente = filtro_inexistente

        mensagem = f'O filtro \'{filtro_inexistente}\' não está presente no banco de dados'

        super().__init__(mensagem)

CACHE = _ViewCache()

class View():
    _data: pd.DataFrame
    _filtros: List[str]

    _composicao: pd.DataFrame

    # Diferencia uma composição cujo nenhum item
    # obedece os filtros de uma composição ainda
    # não teve nenhum filtro adicionado
    _primeiro_filtro: bool

    _instancia: _ViewCache

    def __init__(self):
        self._filtros = []

        self._data = pd.DataFrame()

        self._instancia = CACHE
        self._sincroniza_db()

        self._primeiro_filtro = True
        self._composicao = pd.DataFrame()

    def _merge_dbs(self, db1: pd.DataFrame, db2: pd.DataFrame) -> pd.DataFrame:
        result: pd.DataFrame = None

        try:
            result = pd.merge(db1, db2, on='id', how='outer')
        except IndexError:
            result = db1.reindex_axis(db1.columns.union(db2.columns), axis=1)

        assert result is not None
        return result

    def _sincroniza_db(self):
        dbs = self._instancia.obtem_dbs()
        self._data = reduce(self._merge_dbs, dbs)

    @property
    def filtros(self):
        return copy(self._filtros)

    @filtros.setter
    def filtros(self, novos_filtros: List[str]):
        for filtro in novos_filtros:
            coluna = self._obtem_coluna_do_filtro(filtro)

            self._composicao[filtro] = coluna
            self._filtros.append(filtro)

    def obtem_filtros_possiveis(self) -> List[str]:
        return [coluna for coluna in self._data.columns \
                if coluna not in self.filtros]

    def _obtem_coluna_do_filtro(self, filtro: str) -> pd.Series:
        # Filtro já foi aplicado
        if filtro in self.filtros:
            # TODO: Deve retornar erro ou não fazer nada?
            pass
        else:
            colunas_obtidas = [coluna for coluna in self._data.columns \
                                   if coluna == filtro]

            if len(colunas_obtidas) == 0:
                raise FiltroInexistenteException(filtro)

            return self._data[filtro]

    def filtra_por(self, coluna: str, predicado: Optional[Callable] = None):
        alvo = self._obtem_coluna_do_filtro(coluna)

        self._composicao[coluna] = alvo

        if predicado:
            mascara = alvo.apply(predicado)

            if not self._primeiro_filtro:
                mascara = mascara.iloc[self._composicao.index]

            tam = self._composicao.shape[0]
            self._composicao = self._composicao.loc[mascara[mascara].index.values]

        self._filtros.append(coluna)
        if self._primeiro_filtro:
            self._primeiro_filtro = False

    def remove_linhas_com_nan(self):
        self._composicao = self._composicao.dropna()

    def __repr__(self) -> str:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            return self._composicao.__repr__()

