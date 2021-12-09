import unittest
from unittest.case import TestCase
from unittest.mock import Base, patch
import pandas as pd
import os

from interface import *

from views import View
from patch import _sincroniza_db

class TestesInterfaceUnidade(unittest.TestCase):
    @patch(__module__+'.View._sincroniza_db', _sincroniza_db)
    def setUp(self):
        self.interface = Interface('csv_teste/')

    def teste_filtra_midia_livro(self):
        filtros = ['id', 'nome', 'nota']

        self.interface.filtrar_midia(filtros, 'Livro')
        df = self.interface._view._composicao.merge(self.interface._db.db_registros, on='id')
        
        midias_presentes = df['tipo_midia'].unique()
        self.assertEqual(midias_presentes, ['Livro'])
    
    def teste_filtra_midia_serie(self):
        filtros = ['id', 'nome', 'nota']

        self.interface.filtrar_midia(filtros, 'Série')
        df = self.interface._view._composicao.merge(self.interface._db.db_registros, on='id')
        
        midias_presentes = df['tipo_midia'].unique()
        self.assertEqual(midias_presentes, ['Série'])

    def teste_filtra_midia_filme(self):
        filtros = ['id', 'nome', 'nota']

        self.interface.filtrar_midia(filtros, 'Filme')
        df = self.interface._view._composicao.merge(self.interface._db.db_registros, on='id')
        
        midias_presentes = df['tipo_midia'].unique()
        self.assertEqual(midias_presentes, ['Filme'])

class TestesInterfaceIntegracao(unittest.TestCase):
    def setUp(self):
        self.interface = Interface(local_base='csv/')
    
    def tearDown(self):
        path = 'csv/'
        for csv in os.listdir(path):
            with open(path + csv, 'r') as arquivo:
                linhas = arquivo.readlines()
            
            with open(path + csv, 'w') as arquivo:
                arquivo.write(linhas[0])

    def teste_adiciona_midia(self):
        livro = Livro('Revolução dos Bichos', 'Sátira Política', 1945, ['George Orwell'], 112)
        registro_novo1 = Registro(8.9, livro, None, True)

        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo2 = Registro(8.8, filme, 'Muito bom!', True)
        
        serie = Serie('Brooklyn Nine-Nine', 'Comédia', 2013, 153, 22, 8, ['Andy Samberg', 'Stephanie Beatriz', 'Terry Crews'])
        registro_novo3 = Registro(7.8, serie, None, True)

        self.interface.adicionar_registro(registro_novo1, Base_Midias, 'adiciona_livro')
        self.interface.adicionar_registro(registro_novo2, Base_Midias, 'adiciona_filme')
        self.interface.adicionar_registro(registro_novo3, Base_Midias, 'adiciona_serie')

        self.interface._view.filtra_por('nome')

        self.assertEqual(3, len(self.interface._view._composicao))

    def teste_remove_midia(self):
        livro = Livro('Revolução dos Bichos', 'Sátira Política', 1945, ['George Orwell'], 112)
        registro_novo1 = Registro(8.9, livro, None, True)

        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo2 = Registro(8.8, filme, 'Muito bom!', True)
        
        serie = Serie('Brooklyn Nine-Nine', 'Comédia', 2013, 153, 22, 8, ['Andy Samberg', 'Stephanie Beatriz', 'Terry Crews'])
        registro_novo3 = Registro(7.8, serie, None, True)

        self.interface.adicionar_registro(registro_novo1, Base_Midias, 'adiciona_livro')
        self.interface.adicionar_registro(registro_novo2, Base_Midias, 'adiciona_filme')
        self.interface.adicionar_registro(registro_novo3, Base_Midias, 'adiciona_serie')

        self.interface.remover_registro('Revolução dos Bichos', 'Livro')
        self.interface.remover_registro('Shang-Chi e a Lenda dos Dez Anéis', 'Filme')

        self.interface._view.filtra_por('nome')
        
        self.assertEqual(1, len(self.interface._view._composicao))
        
    def teste_lista_midia(self):
        livro = Livro('Revolução dos Bichos', 'Sátira Política', 1945, ['George Orwell'], 112)
        registro_novo1 = Registro(8.9, livro, None, True)

        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo2 = Registro(8.8, filme, 'Muito bom!', True)
        
        serie = Serie('Brooklyn Nine-Nine', 'Comédia', 2013, 153, 22, 8, ['Andy Samberg', 'Stephanie Beatriz', 'Terry Crews'])
        registro_novo3 = Registro(7.8, serie, None, True)
    
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 2014, 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'])
        registro_novo4 = Registro(None, filme, None, False)

        self.interface.adicionar_registro(registro_novo1, Base_Midias, 'adiciona_livro')
        self.interface.adicionar_registro(registro_novo2, Base_Midias, 'adiciona_filme')
        self.interface.adicionar_registro(registro_novo3, Base_Midias, 'adiciona_serie')
        self.interface.adicionar_registro(registro_novo4, Base_Midias, 'adiciona_filme')

        self.interface.lista_geral()
        self.assertEqual(4, len(self.interface._view._composicao))
        
        self.interface.lista_filme()
        self.assertEqual(2, len(self.interface._view._composicao))

        self.interface.lista_livro()
        self.assertEqual(1, len(self.interface._view._composicao))

        self.interface.lista_serie()
        self.assertEqual(1, len(self.interface._view._composicao))

    def testa_lista_comentario(self):
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo1 = Registro(8.8, filme, 'Muito bom!', True)

        livro = Livro('Revolução dos Bichos', 'Sátira Política', 1945, ['George Orwell'], 112)
        registro_novo2 = Registro(8.9, livro, 'Mais ou menos', True)

        self.interface.adicionar_registro(registro_novo1, Base_Midias, 'adiciona_filme')
        self.interface.adicionar_registro(registro_novo2, Base_Midias, 'adiciona_livro')

        self.interface.comentario_midia()

        self.assertEqual(2, len(self.interface._view._composicao))