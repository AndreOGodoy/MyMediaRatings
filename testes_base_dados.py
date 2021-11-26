import unittest
from base_dados import Base_Midias
from midia import *
from registro import Registro

class TestesBaseDeDados(unittest.TestCase):
    def setUp(self):
        self.db = Base_Midias()

    def teste_rejeita_nomeRepetido_mesmoTipo(self):
        serie = Serie('Good Omens', 'Comédia, Fantasia', 6, 55, 1, 2019, ['Michael Sheen', 'David Tennant'])
        registro_novo = Registro(None, serie, None, False)
        self.assertFalse(self.db.verifica_permitido(registro_novo, 'Série'))
    
    def teste_aceita_nomeRepetido_outroTipo(self):
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'], 2014)
        registro_novo = Registro(None, filme, None, False)
        self.assertTrue(self.db.verifica_permitido(registro_novo, 'Filme'))
    
    def teste_rejeita_avalia_semAssistir(self):
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'], 2021)
        registro_novo = Registro(8.8, filme, None, False)
        self.assertFalse(self.db.verifica_permitido(registro_novo, 'Filme'))
    
    def teste_rejeita_comenta_semAssistir(self):
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'], 2021)
        registro_novo = Registro(None, filme, 'Muito bom!', False)
        self.assertFalse(self.db.verifica_permitido(registro_novo, 'Filme'))
    
    def teste_adiciona_serie(self):
        serie = Serie('Brooklyn Nine-Nine', 'Comédia', 153, 22, 8, 2013, ['Andy Samberg', 'Stephanie Beatriz', 'Terry Crews'])
        registro_novo = Registro(None, serie, None, False)
        self.db.adiciona_serie(registro_novo)
        ultima_linha_nome = self.db.db_registros.loc[self.db.db_registros.index.max()]['nome']
        self.assertEqual(ultima_linha_nome, 'Brooklyn Nine-Nine')
    
    def teste_adiciona_filme(self):
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'], 2021)
        registro_novo = Registro(8.8, filme, 'Muito bom!', True)
        self.db.adiciona_filme(registro_novo)
        ultima_linha_nome = self.db.db_registros.loc[self.db.db_registros.index.max()]['nome']
        self.assertEqual(ultima_linha_nome, 'Shang-Chi e a Lenda dos Dez Anéis')
    
    def teste_adiciona_livro(self):
        livro = Livro('Revolução dos Bichos', 'Sátira Política', ['George Orwell'], 112, 1945)
        registro_novo = Registro(None, livro, None, False)
        self.db.adiciona_livro(registro_novo)
        ultima_linha_nome = self.db.db_registros.loc[self.db.db_registros.index.max()]['nome']
        self.assertEqual(ultima_linha_nome, 'Revolução dos Bichos')

    def teste_mesmoID_difentesDFs(self):
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'], 2014)
        registro_novo = Registro(None, filme, None, False)
        self.db.adiciona_filme(registro_novo)
        id_registros = self.db.db_registros.loc[self.db.db_registros.index.max()]['id']
        id_filmes = self.db.db_filmes.loc[self.db.db_filmes.index.max()]['id']
        self.assertEqual(id_registros, id_filmes)
