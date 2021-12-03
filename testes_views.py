from views import *

import pandas as pd
from pandas import DataFrame
import numpy as np
import os
from typing import List

from unittest import TestCase
from unittest.mock import patch

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

class TestViews(TestCase):

    # Substituição da função. Patchs são desfeitos após o retorno da função,
    # o que não é problema pois _sincroniza_db() é utilizada
    # apenas para construção de View(),
    @patch(__module__+'.View._sincroniza_db', _sincroniza_db)
    def setUp(self):
        self.view = View()

    def test_nova_view_composicao_vazia(self):
        self.assertTrue(self.view._composicao.empty)

    def test_nova_view_sem_filtros(self):
        numero_filtros = len(self.view.filtros)
        self.assertTrue(numero_filtros == 0)

    # Método utilitário
    def arrays_sao_iguais(self, arr1: np.ndarray, arr2: np.ndarray):
        return (arr1 == arr2).all()

    # Obtem as colunas do atributo _data da view. Evita acesso a elementos
    # não-interface de view
    def colunas_view(self, view: View):
        como_string = view.__repr__()
        primeira_linha = como_string.split('\n')[0]

        como_lista = primeira_linha.split(' ')

        # Remove detalhe de impressão do Pandas
        nomes = filter(lambda x: x.replace('\\', '') != '', como_lista)

        return list(nomes)

    def test_conteudo_reflete_filtros(self):
        filtros_aplicados = ['tipo_midia', 'nome', 'autor', 'nota']
        self.view.filtros = filtros_aplicados[:2]
        for filtro in filtros_aplicados[2:]:
            self.view.filtra_por(filtro)

        colunas_obtidas = self.view._composicao.columns
        colunas_esperadas = filtros_aplicados
        self.assertTrue(self.arrays_sao_iguais(colunas_obtidas, filtros_aplicados))

    def test_filtros_possiveis_igual_total_colunas_db(self):
        filtros_possiveis = self.view.obtem_filtros_possiveis()
        colunas_db = cria_db_teste().columns

        self.assertTrue(self.arrays_sao_iguais(colunas_db, filtros_possiveis))

    def test_filtra_por_aplica_devido_filtro(self):
        filtro = 'duracao'

        self.view.filtra_por(filtro)
        filtros_aplicados = self.view.filtros

        self.assertEqual(filtros_aplicados, [filtro])

    def test_define_filtro_inexistente(self):
        with self.assertRaises(FiltroInexistenteException):
            self.view.filtros = ['coluna_nao_existente']

    def test_aplica_filtro_inexistente(self):
        self.assertRaises(FiltroInexistenteException, self.view.filtra_por, 'coluna_nao_existente')

    def test_numero_filtros_possiveis_apos_definir_filtro_unico(self):
        filtros_possiveis_inicial = self.view.obtem_filtros_possiveis()
        self.view.filtros = ['genero']
        filtros_possiveis_final = self.view.obtem_filtros_possiveis()

        self.assertEqual(len(filtros_possiveis_inicial), len(filtros_possiveis_final) + 1)

    def test_numero_filtros_possiveis_apos_definir_filtro_duplo(self):
        filtros_possiveis_inicial = self.view.obtem_filtros_possiveis()
        self.view.filtros = ['genero', 'autor']
        filtros_possiveis_final = self.view.obtem_filtros_possiveis()

        self.assertEqual(len(filtros_possiveis_inicial), len(filtros_possiveis_final) + 2)

    def test_numero_filtros_possiveis_apos_redefinir_filtro(self):
        self.view.filtros = ['genero', 'autor']
        filtros_possiveis_pre_redef = self.view.obtem_filtros_possiveis()
        self.view.filtros = ['duracao']
        filtros_possiveis_pos_def = self.view.obtem_filtros_possiveis()

        self.assertEqual(len(filtros_possiveis_pre_redef), len(filtros_possiveis_pos_def) + 1)


