import pandas as pd
from copy import copy
from typing import List, Optional, Callable

from base_dados import Base_Midias

# Esta classe é utilizada para organização interna
#
# Ela é instanciada no momento que o módulo for importado pelo cliente,
# fazendo com que carregue os dados do banco de dados
#
# Seu objetivo é impedir que haja um acesso ao DB, e o carregamento de seu
# conteúdo à memória, à cada nova construção de View()
class _ViewCache():
    _instancia: Base_Midias
    _dfs: List[pd.DataFrame]

    def __init__(self):
        self._dfs = []
        self._instancia = Base_Midias('csv/')

    def atualiza(self):
        self._instancia.atualiza_arquivos()
        self._dfs = self._instancia.retorna_dataframes()

    def obtem_dbs(self):
        self.atualiza()

        return self._dfs

class FiltroAmbiguoException(Exception):
    filtro_ambiguo: str

    def __init__(self, filtro_ambiguo: str):
        self.filtro_ambiguo = filtro_ambiguo

        mensagem = f'O filtro \'{filtro_ambiguo}\' é ambíguo:'
        mensagem += ' existe mais de uma tabela com esta coluna no banco de dados'

        super().__init__(mensagem)

class FiltroInexistenteException(Exception):
    filtro_inexistente: str

    def __init__(self, filtro_inexistente: str):
        self.filtro_inexistente = filtro_inexistente

        mensagem = f'O filtro \'{filtro_inexistente}\' não está presente no banco de dados'

        super().__init__(mensagem)

CACHE = _ViewCache()

class View():
    _data: List[pd.DataFrame]
    _filtros: List[str]

    _composicao: pd.DataFrame

    _instancia: _ViewCache

    def __init__(self):
        self._filtros = []
        self._composicao = pd.DataFrame()

        self._instancia = CACHE
        self._sincroniza_db()

    def _sincroniza_db(self):
        self._data = self._instancia.obtem_dbs()

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
        colunas = []
        for df in self._data:
            colunas.extend(df.columns)

        colunas_nao_ambiguas = [coluna for coluna in colunas \
                                if colunas.count(coluna)==1]

        return [filtro for filtro in colunas_nao_ambiguas \
                if filtro not in self._filtros]

    def _obtem_coluna_do_filtro(self, filtro: str) -> pd.Series:
        # Filtro já foi aplicado
        if filtro in self.filtros:
            # TODO: Deve retornar erro ou não fazer nada?
            pass
        else:
            colunas_obtidas = [df[filtro] for df in self._data \
                               if filtro in df.columns]
            n_colunas_obtidas = len(colunas_obtidas)

            if n_colunas_obtidas == 0:
                raise FiltroInexistenteException(filtro)

            elif len(colunas_obtidas) > 1:
                # TODO: Resolver este caso
                raise FiltroAmbiguoException(filtro)
                return self

            # Deve ser sempre verdadeiro por causa dos dois if's acima
            assert len(colunas_obtidas) == 1
            return colunas_obtidas[0]

    def filtra_por(self, coluna: str, predicado: Optional[Callable] = None):
        alvo = self._obtem_coluna_do_filtro(coluna)

        if predicado:
            self._composicao[coluna] = alvo.loc[predicado]
        else:
            self._composicao[coluna] = alvo

        self._composicao = self._composicao.dropna()
        self._filtros.append(coluna)

    def __repr__(self) -> str:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            return self._composicao.__repr__()

