from views import *

from pandas import DataFrame
import numpy as np

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
def cria_db_teste(n: int = 100):
    rng = np.random.default_rng()

    escolhe_n_reps = lambda lista: rng.choice(lista, n)
    gera_num_pag = lambda: rng.choice([100, 200, 300, 400, 500, 600], 1)[0]
    gera_nota = lambda: np.round(rng.uniform(0, 10), 1)

    midias_possiveis = ['Livro', 'Filme', 'Serie', 'Animacao']
    notas_possiveis = [gera_nota() for _ in range(n)]
    generos_possiveis = ['Terror', 'Romance', 'Aventura', 'Ficção Científica']

    buffer = {}
    buffer['tipo_midia'] = escolhe_n_reps(midias_possiveis)
    buffer['n_paginas'] = [gera_num_pag() if midia == "Livro" \
                           else None for midia in buffer['tipo_midia']]
    buffer['nota'] = escolhe_n_reps(notas_possiveis)
    buffer['genero'] = escolhe_n_reps(generos_possiveis)

    df = pd.DataFrame.from_dict(buffer)
    return df

def _sincroniza_db(self):
    self._data = cria_db_teste(n=20)

class TestViews(TestCase):

    # Substituição da função. Patchs são desfeitos após o retorno da função,
    # o que não é problema pois _sincroniza_db() é utilizada
    # apenas para construção de View(),
    @patch(__module__+'.View._sincroniza_db', _sincroniza_db)
    def setUp(self):
        self.view = View()

    def test_numero_filtros_possiveis_nova_view(self):
        filtros_possiveis = self.view.obtem_filtros_possiveis()
        self.assertEqual(len(filtros_possiveis), 4)

    def test_aplica_filtro_nova_view(self):
        self.view.aplica_filtro("tipo_midia")
        filtros_aplicados = self.view.filtros

        self.assertEqual(filtros_aplicados, ["tipo_midia"])

    def test_numero_filtros_possiveis_apos_definir_filtro_unico(self):
        filtros_possiveis_inicial = self.view.obtem_filtros_possiveis()
        self.view.filtros = ["tipo_midia"]
        filtros_possiveis_final = self.view.obtem_filtros_possiveis()

        self.assertEqual(len(filtros_possiveis_inicial), len(filtros_possiveis_final) + 1)

    def test_numero_filtros_possiveis_apos_definir_filtro_duplo(self):
        filtros_possiveis_inicial = self.view.obtem_filtros_possiveis()
        self.view.filtros = ["tipo_midia", "genero"]
        filtros_possiveis_final = self.view.obtem_filtros_possiveis()

        self.assertEqual(len(filtros_possiveis_inicial), len(filtros_possiveis_final) + 2)

    def test_numero_filtros_possiveis_apos_redefinir_filtro(self):
        self.view.filtros = ["tipo_midia", "genero"]
        filtros_possiveis_pre_redef = self.view.obtem_filtros_possiveis()
        self.view.filtros = ["tipo_midia"]
        filtros_possiveis_pos_def = self.view.obtem_filtros_possiveis()

        self.assertEqual(len(filtros_possiveis_pre_redef), len(filtros_possiveis_pos_def) - 1)

    def test_numero_filtros_possiveis_apos_nova_aplicacao(self):
        filtros_possiveis_inicial = self.view.obtem_filtros_possiveis()
        self.view.filtros = ["Midia"]

    def test_numero_filtros_aplicados_nova_view(self):
        filtros = self.view.filtros
        self.assertEqual(len(filtros), 0)
