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

    def teste_adiciona_livro(self):
        livro1 = Livro('Revolução dos Bichos', 'Sátira Política', 1945, ['George Orwell'], 112)
        registro_novo1 = Registro(8.9, livro1, None, True)

        livro2 = Livro('Revolução dos Bichos 2', 'Sátira Política', 1946, ['George Orwell'], 112)
        registro_novo2 = Registro(8.9, livro2, None, True)
        
        livro3 = Livro('Revolução dos Bichos 3', 'Sátira Política', 1947, ['George Orwell'], 112)
        registro_novo3 = Registro(8.9, livro3, None, True)

        self.interface.adicionar_registro(registro_novo1, Base_Midias, 'adiciona_livro')
        self.interface.adicionar_registro(registro_novo2, Base_Midias, 'adiciona_livro')
        self.interface.adicionar_registro(registro_novo3, Base_Midias, 'adiciona_livro')

        self.interface._view.filtra_por('nome')

        self.assertEqual(3, len(self.interface._view._composicao))
        