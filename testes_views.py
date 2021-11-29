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

    return dfs

def _sincroniza_db(self):
    self._data = cria_db_teste()

class TestViews(TestCase):

    # Substituição da função. Patchs são desfeitos após o retorno da função,
    # o que não é problema pois _sincroniza_db() é utilizada
    # apenas para construção de View(),
    @patch(__module__+'.View._sincroniza_db', _sincroniza_db)
    def setUp(self):
        self.view = View()

    def test_numero_filtros_possiveis_nova_view(self):
        filtros_possiveis = self.view.obtem_filtros_possiveis()
        self.assertEqual(len(filtros_possiveis), 13)

    def test_filtra_por_aplica_filtro(self):
        self.view.filtra_por('duracao')
        filtros_aplicados = self.view.filtros

        self.assertEqual(filtros_aplicados, ['duracao'])

    def test_define_filtro_ambiguo(self):
        # A coluna 'ano_lancamento' está presente em 3 tabelas
        # Logo, é ambíguo filtrar pela mesma

        with self.assertRaises(FiltroAmbiguoException):
            self.view.filtros = ['ano_lancamento']

    def test_aplica_filtro_ambiguo(self):
        self.assertRaises(FiltroAmbiguoException, self.view.filtra_por, 'ano_lancamento')

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

    def test_numero_filtros_possiveis_apos_nova_aplicacao(self):
        filtros_possiveis_inicial = self.view.obtem_filtros_possiveis()
        self.view.filtros = ['genero']

    def test_numero_filtros_aplicados_nova_view(self):
        filtros = self.view.filtros
        self.assertEqual(len(filtros), 0)
