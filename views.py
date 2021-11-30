import pandas as pd
from copy import copy
from typing import List

from base_dados import Base_Midias

# Esta classe é utilizada para organização interna
#
# Ela é instanciada no momento que o módulo for importado pelo cliente,
# fazendo com que carregue os dados do banco de dados
#
# Seu objetivo é impedir que haja um acesso ao DB, e o carregamento de seu
# conteúdo à memória, à cada nova construção de View()
class _ViewCache():
    _instancia = pd.DataFrame

    def __init__(self):
        self._instancia = Base_Midias('csv/')

    def obtem_dbs(self) -> List[pd.DataFrame]:
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

        # Retorna os 'data_attributes', que são os DataFrames
        return [getattr(self._instancia, df_name) for df_name in db_data_attr]

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
    _filtros: [str]

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
    def filtros(self, novos_filtros: [str]):
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

    def filtra_por(self, filtro: str):
            coluna = self._obtem_coluna_do_filtro(filtro)

            self._composicao[filtro] = coluna
            self._filtros.append(filtro)

    def __repr__(self) -> str:
        return self._composicao.__repr__()
