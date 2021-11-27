import unittest
from base_dados import Base_Midias
from midia import *
from registro import Registro

class TestesBaseDeDados(unittest.TestCase):
    def teste_rejeita_nomeRepetido_mesmoTipo(self):
        db = Base_Midias()
        serie = Serie('Good Omens', 'Comédia, Fantasia', 6, 55, 1, 2019, ['Michael Sheen', 'David Tennant'])
        registro_novo = Registro(None, serie, None, False)
        self.assertFalse(db.verifica_permitido_adicionar(registro_novo, 'Série'))
    
    def teste_aceita_nomeRepetido_outroTipo(self):
        db = Base_Midias()
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'], 2014)
        registro_novo = Registro(None, filme, None, False)
        self.assertTrue(db.verifica_permitido_adicionar(registro_novo, 'Filme'))
    
    def teste_rejeita_avalia_semAssistir(self):
        db = Base_Midias()
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'], 2021)
        registro_novo = Registro(8.8, filme, None, False)
        self.assertFalse(db.verifica_permitido_adicionar(registro_novo, 'Filme'))
    
    def teste_rejeita_comenta_semAssistir(self):
        db = Base_Midias()
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'], 2021)
        registro_novo = Registro(None, filme, 'Muito bom!', False)
        self.assertFalse(db.verifica_permitido_adicionar(registro_novo, 'Filme'))
    
    def teste_adiciona_serie(self):
        db = Base_Midias()
        serie = Serie('Brooklyn Nine-Nine', 'Comédia', 153, 22, 8, 2013, ['Andy Samberg', 'Stephanie Beatriz', 'Terry Crews'])
        registro_novo = Registro(None, serie, None, False)
        db.adiciona_serie(registro_novo)
        ultima_linha_nome = db.db_registros.loc[db.db_registros.index.max()]['nome']
        self.assertEqual(ultima_linha_nome, 'Brooklyn Nine-Nine')
    
    def teste_adiciona_filme(self):
        db = Base_Midias()
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'], 2021)
        registro_novo = Registro(8.8, filme, 'Muito bom!', True)
        db.adiciona_filme(registro_novo)
        ultima_linha_nome = db.db_registros.loc[db.db_registros.index.max()]['nome']
        self.assertEqual(ultima_linha_nome, 'Shang-Chi e a Lenda dos Dez Anéis')
    
    def teste_adiciona_livro(self):
        db = Base_Midias()
        livro = Livro('Revolução dos Bichos', 'Sátira Política', ['George Orwell'], 112, 1945)
        registro_novo = Registro(None, livro, None, False)
        db.adiciona_livro(registro_novo)
        ultima_linha_nome = db.db_registros.loc[db.db_registros.index.max()]['nome']
        self.assertEqual(ultima_linha_nome, 'Revolução dos Bichos')

    def teste_mesmoID_difentesDFs(self):
        db = Base_Midias()
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'], 2014)
        registro_novo = Registro(None, filme, None, False)
        db.adiciona_filme(registro_novo)
        id_registros = db.db_registros.loc[db.db_registros.index.max()]['id']
        id_filmes = db.db_filmes.loc[db.db_filmes.index.max()]['id']
        self.assertEqual(id_registros, id_filmes)

    def teste_não_tem_na_base(self):
        db = Base_Midias()
        self.assertFalse(db.retorna_midia_nome('NãoEstáNaBase'))

    def teste_retorna_serie(self):
        db = Base_Midias()
        serie = db.retorna_midia_nome('Good Omens', tipo='Série')
        self.assertEqual(len(serie), 1)
        
    def teste_retorna_filme(self):
        db = Base_Midias()
        filme = db.retorna_midia_nome('Click', tipo='Filme')
        self.assertEqual(len(filme), 1)
        
    def teste_retorna_livro(self):
        db = Base_Midias()
        livro = db.retorna_midia_nome('Good Omens', tipo='Livro')
        self.assertEqual(len(livro), 1)
    
    def teste_retorna_multiplos_registros(self):
        db = Base_Midias()
        regs = db.retorna_midia_nome('Good Omens')
        self.assertEqual(len(regs), 2)
    
    def teste_tipo_indisponível(self):
        db = Base_Midias()
        self.assertFalse(db.retorna_midia_nome('Good Omens', tipo='Tipo'))
