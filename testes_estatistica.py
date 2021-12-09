from typing import ChainMap
from numpy.core.numeric import NaN
from numpy.testing._private.utils import assert_equal
from estatisticas import *

import pandas as pd
from pandas import DataFrame
import numpy as np

import io
import sys

from unittest import TestCase

from views import View

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

class TestException(TestCase):
    def setUp(self):
        df = pd.DataFrame({'nome': ['Good Omens', 'The office', 'Vingadores: Ultimato', '1984'],
        'genero': ['', '', '', ''],
        'ano_lancamento': [np.NaN, np.NaN, np.NaN, np.NaN],
        'tipo_midia': ['', '', '', ''],
        'nota': [np.NaN, np.NaN, np.NaN, np.NaN],
        'comentario': ['com1', 'com2', 'com3', 'com4'],
        'ja_consumiu': [True, True, True, True]})

        self.est = EstRegistros(df)

    def test_media_notas_exception(self):
        with self.assertRaises(Exception):
            self.est.media_notas()
    
    def test_nota_mais_atribuida_exception(self):
        with self.assertRaises(Exception):
            self.est.moda_notas()

    def test_maior_nota_atribuida_exception(self):
        with self.assertRaises(Exception):
            self.est.maior_nota()

    def test_menor_nota_atribuida_exception(self):
        with self.assertRaises(Exception):
            self.est.menor_nota()

    def test_tipo_midia_mais_consumido_exception(self):
        with self.assertRaises(Exception):
            self.est.midia_mais_consumida()

    def test_genero_mais_consumido_exception(self):
        with self.assertRaises(Exception):
            self.est.genero_mais_consumido()

    def test_ano_com_mais_lancamentos_exception(self):
        with self.assertRaises(Exception):
            self.est.ano_com_mais_lancamentos()

#Testes de Integração
#Vão consistir em utilizar as funções presentes em Views
#e no banco de dados original para mostrar as estatísticas

class TestIntegracaoLivro(TestCase):
    def setUp(self):
        with open('./csv/registros.csv', 'a') as arqreg:
            arqreg.write('0;1984;Drama, Distopia, Ficção Científica;1949;Livro;10.0;Obra prima sem igual. Não importa quando ou quantas vezes você o leia, sempre haverá uma percepção de algum aspecto da sociedade que você não tinha visto antes. Praticamente uma profecia do mundo pós moderno. Não é uma leitura fácil, definitivamente. Mas vale muito a pena.;True\n')
            arqreg.write('1;Sherlock Holmes: Um Estudo em Vermelho;Ação, Mistério;1887;Livro;9.6;Achei muito espetacular, a trama foi muito bem elaborada ao ponto de te deixar boquiaberto a cada desfecho, simplesmente fenomenal.;True\n')
            arqreg.write('2;A Culpa é Das Estrelas;Drama, Romance;2012;Livro;10;Comentario;True')

        with open('./csv/livros.csv', 'a') as arqliv:
            arqliv.write('0;354.0;George Orwell\n')
            arqliv.write('1;122.0;Arthur Conan Doyle\n')
            arqliv.write('2;268.0;John Green')

    def test_integra_livro(self):
        self.view = View()
        filtros = ['nome', 'num_paginas', 'autor', 'nota']
        
        for filtro in filtros:
            self.view.filtra_por(filtro)

        est = EstLivros(self.view._composicao)
        saida = io.StringIO()
        sys.stdout = saida
        est.est_geral_livros()
        sys.stdout = sys.__stdout__

        #Asserts conferindo cada uma das saídas numéricas
        self.assertIn('é: 248', saida.getvalue())
        self.assertIn('é: 9.87', saida.getvalue())
        self.assertIn('frequência: 10', saida.getvalue())
        self.assertIn('é: 9.6', saida.getvalue())

    def tearDown(self):
        with open('./csv/registros.csv', 'w') as arqreg:
            arqreg.write('id;nome;genero;ano_lancamento;tipo_midia;nota;comentario;ja_consumiu\n')

        with open('./csv/livros.csv', 'w') as arqliv:
            arqliv.write('id;num_paginas;autor\n')

class TestIntegracaoFilme(TestCase):
    def setUp(self):
        with open('./csv/registros.csv', 'a') as arqreg:
            arqreg.write('0;Vingadores: Ultimato;Ação, Aventura, Drama, Ficção Científica;2019;Filme;9.0;É divertido porem não é aquele filme incrivel que mudaria sua vida;True\n')
            arqreg.write('1;Seven: Os Sete Crimes Capitais;Policial, Drama, Mistério;1995;Filme;8.0;comentario;True\n')
            arqreg.write('2;Moana - Um Mar de Aventuras;Animação, Aventura, Comédia;2016;Filme;8.5;Um filme ótimo para assistir com toda a família, aventuras, partes cômicas, partes sentimentais e muita música... Muita música mesmo. Recomendo demais esse filme;True')

        with open('./csv/filmes.csv', 'a') as arqfilm:
            arqfilm.write('0;181;Anthony Russo, Joe Russo;Robert Downey Jr, Chris Evans, Mark Ruffalo\n')
            arqfilm.write('1;127;David Fincher;Morgan Freeman, Brad Pitt, Kevin Spacey\n')
            arqfilm.write('8;107;Ron Clements, John Musker, Don Hall;Aulii Cravalho, Dwayne Johnson, Rachel House')

    def test_integra_filme(self):
        self.view = View()
        filtros = ['nome', 'duracao', 'diretor', 'nota', 'elenco_y']
        
        for filtro in filtros:
            self.view.filtra_por(filtro)

        est = EstFilmes(self.view._composicao)
        saida = io.StringIO()
        sys.stdout = saida
        est.est_geral_filmes()
        sys.stdout = sys.__stdout__

        #Asserts conferindo cada uma das saídas numéricas
        self.assertIn('é: 138.33', saida.getvalue())
        self.assertIn('é: 8.5', saida.getvalue())
        self.assertIn('é: 9', saida.getvalue())
        self.assertIn('é: 8', saida.getvalue())

    def tearDown(self):
        with open('./csv/registros.csv', 'w') as arqreg:
            arqreg.write('id;nome;genero;ano_lancamento;tipo_midia;nota;comentario;ja_consumiu\n')

        with open('./csv/filmes.csv', 'w') as arqfilm:
            arqfilm.write('id;duracao;diretor;elenco\n')
        
class TestIntegracaoserie(TestCase):
    def setUp(self):
        with open('./csv/registros.csv', 'a') as arqreg:
            arqreg.write('0;Good Omens;Comédia, Fantasia;2019;Série;10.0;Lindo, Belo e Bem Gay. É uma das minhas favoritas do Neil Gaiman.;True\n')
            arqreg.write('1;The Office;Comédia;2005;Série;9.5;Muito bom! Não se deixe enganar pelos primeiros episódios. Série leve, divertida, com episódios curtos, excelente para assistir nas refeições.;True\n')
            arqreg.write('2;Arquivo X;Policial, Drama, Mistério;1993;Série;8.0;A série é muito boa, apesar de ter iniciado nos anos 90 sem os recursos dos efeitos computadorizados de hoje, te prende no suspense de cada episódio. Parabéns aos atores e criadores da série. (Recomendo);True')

        with open('./csv/series.csv', 'a') as arqser:
            arqser.write('0;6;1;55;Michael Sheen, David Tennant, Frances McDormand, Jon Hamm\n')
            arqser.write('1;188;9;22;Steve Carell, Jenna Fischer, John Krasinski\n')
            arqser.write('2;217;11;45;David Duchovny, Gillian Anderson, Mitch Pileggi')

    def test_integra_livro(self):
        self.view = View()
        filtros = ['nome', 'num_episodios', 'num_temporadas', 'tempo_por_ep', 'nota', 'elenco_x']
        
        for filtro in filtros:
            self.view.filtra_por(filtro)

        est = EstSeries(self.view._composicao)
        saida = io.StringIO()
        sys.stdout = saida
        est.est_geral_series()
        sys.stdout = sys.__stdout__

        #Asserts conferindo cada uma das saídas numéricas
        self.assertIn('é: 137', saida.getvalue())
        self.assertIn('assistidos: 217', saida.getvalue())
        self.assertIn('assistidas: 11', saida.getvalue())
        self.assertIn('é de: 40.67', saida.getvalue())
        self.assertIn('é: 9.17', saida.getvalue())
        self.assertIn('é: 10', saida.getvalue())
        self.assertIn('é: 8.0', saida.getvalue())

    def tearDown(self):
        with open('./csv/registros.csv', 'w') as arqreg:
            arqreg.write('id;nome;genero;ano_lancamento;tipo_midia;nota;comentario;ja_consumiu\n')

        with open('./csv/series.csv', 'w') as arqser:
            arqser.write('id;num_episodios;num_temporadas;tempo_por_ep;elenco\n')
