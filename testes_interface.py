import unittest
from unittest.case import TestCase
from unittest.mock import patch
import pandas as pd

from interface import Interface

from views import View
from patch import _sincroniza_db

class TestesInterface(unittest.TestCase):
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
