from typing import ChainMap
from numpy.testing._private.utils import assert_equal
from estatisticas import *

import pandas as pd
from pandas import DataFrame

from unittest import TestCase

#Testes simples, com todos os valores disponíveis
class TestEstatisticasSimples(TestCase):
    def setUp(self):
        df = pd.DataFrame({'nome': ['Good Omens', 'The office', 'Vingadores: Ultimato', '1984'],
        'genero': ['Fantasia', 'Comédia', 'Aventura', 'Drama'],
        'ano_lancamento': [2019, 2005, 2019, 1949],
        'tipo_midia': ['Série', 'Série', 'Filme', 'Livro'],
        'nota': [10, 8.5, 9, 10],
        'comentario': ['com1', 'com2', 'com3', 'com4'],
        'ja_consumiu': [True, True, True, True]})

        self.est = EstRegistros(df)

    def test_media_notas_valido(self):
        esperada = "A nota média das mídias selecionadas pelo filtro é: 9.38"
        chamada = self.est.media_notas()
        self.assertEqual(chamada, esperada)
    
    #Testes que retornam a moda podem retornar mais de um valor, logo
    # devemos estar atentos aos espacos obtidos no assert. 
    def test_nota_mais_atribuida_valido(self):
        esperada = "Nota(s) atribuída(s) com mais frequência: 10.0"
        chamada = self.est.moda_notas()
        self.assertEqual(chamada, esperada)

    def test_maior_nota_atribuida_valido(self):
        esperada = "A MAIOR nota atribuída às mídias selecionadas pelo filtro é: 10.0"
        chamada = self.est.maior_nota()
        self.assertEqual(chamada, esperada)

    def test_menor_nota_atribuida_valido(self):
        esperada = "A MENOR nota atribuída às mídias selecionadas pelo filtro é: 8.5"
        chamada = self.est.menor_nota()
        self.assertEqual(chamada, esperada)

    def test_tipo_midia_mais_consumido_valido(self):
        esperada = "Mídia(s) mais consumida(s): Série"
        chamada = self.est.midia_mais_consumida()
        self.assertEqual(chamada, esperada)


    def test_genero_mais_consumido_valido(self):
        esperada = "Gênero(s) mais consumido(s): Aventura, Comédia, Drama, Fantasia"
        chamada = self.est.genero_mais_consumido()
        self.assertEqual(chamada, esperada)

    def test_ano_com_mais_lancamentos_valido(self):
        esperada = "Ano(s) com maior número de lançamentos: 2019"
        chamada = self.est.ano_com_mais_lancamentos()
        self.assertEqual(chamada, esperada)

#Testes para os livros
class TestEstLivros(TestCase):
    def setUp(self):
        df = pd.DataFrame({'num_paginas': [200, 300, 400],
        'autor': ['Tolkien', 'Tolkien', 'Martin']})

        self.estLivros = EstLivros(df)

    def test_media_num_paginas_valido(self):
        esperada = "O número de páginas médio dos livros lidos é: 300.0 páginas"
        chamada = self.estLivros.media_num_paginas()
        self.assertEqual(chamada, esperada)

    def test_autor_mais_lido_valido(self):
        esperada = "Autor(es) mais lido(s): Tolkien"
        chamada = self.estLivros.autor_mais_lido()
        self.assertEqual(chamada, esperada)

#Testes para os filmes
class TestEstFilmes(TestCase):
    def setUp(self):
        df = pd.DataFrame({'duracao': [100, 95, 105],
        'diretor': ['Russo Brothers', 'Guillermo Del Toro', 'Russo Brothers']})

        self.estFilmes = EstFilmes(df)

    def test_duracao_media_valida(self):
        esperada = "A duração média dos filmes selecionados é: 100.0 minutos"
        chamada = self.estFilmes.duracao_media()
        self.assertEqual(chamada, esperada)

    def test_diretor_mais_visto_valido(self):
        esperada = "Você assistiu mais filmes do(s) diretor(es): Russo Brothers"
        chamada = self.estFilmes.diretor_mais_visto()
        self.assertEqual(chamada, esperada)

#Testes para as séries
class TestEstSeries(TestCase):
    def setUp(self):
        df = pd.DataFrame({'num_episodios': [6, 25, 55],
        'num_temporadas': [1, 6, 15],
        'tempo_por_ep': [50, 43, 22]})

        self.estSeries = EstSeries(df)

    def test_num_medio_episodios_valido(self):
        esperada = "O número médio de episódios das séries vistas é: 28.67"
        chamada = self.estSeries.num_medio_episodios()
        self.assertEqual(chamada, esperada)

    def test_serie_mais_episodios_valido(self):
        esperada = "Maior número de episódios assistidos: 55"
        chamada = self.estSeries.serie_mais_episodios()
        self.assertEqual(chamada, esperada)

    def test_num_medio_temporadas_valido(self):
        esperada = "O número médio de temporadas das séries vistas é: 7.33"
        chamada = self.estSeries.num_medio_temporadas()
        self.assertEqual(chamada, esperada)

    def test_serie_mais_temporadas_valido(self):
        esperada = "Maior número de temporadas assistidas: 15"
        chamada = self.estSeries.serie_mais_temporadas()
        self.assertEqual(chamada, esperada)

    def test_tempo_medio_episodio_valido(self):
        esperada = "O tempo médio dos episódios das séries selecionadas é de: 38.33 minutos"
        chamada = self.estSeries.tempo_medio_episodio()
        self.assertEqual(chamada, esperada)
