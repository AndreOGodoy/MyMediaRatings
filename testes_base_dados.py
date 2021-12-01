import unittest
import pandas as pd
from base_dados import Base_Midias
from midia import *
from registro import Registro

class TestesBaseDeDados(unittest.TestCase):
    def teste_não_tem_na_base_nome(self):
        db = Base_Midias('csv_teste/')
        
        self.assertEqual(db.retorna_registro_por_nome('NãoEstáNaBase'), 'Nenhum registro correspondente encontrado')

    def teste_não_tem_na_base_id(self):
        db = Base_Midias('csv_teste/')
        
        self.assertEqual(db.retorna_registro_id(-3), 'Nenhum registro correspondente encontrado')

    def teste_retorna_serie_nome(self):
        db = Base_Midias('csv_teste/')
        serie = db.retorna_registro_por_nome('Good Omens', tipo='Série')
        registro_esperado = Registro(10, Serie('Good Omens', 'Comédia, Fantasia', 2019, 6, 55, 1, ['Michael Sheen', 'David Tennant', 'Frances McDormand', 'Jon Hamm']), 'Lindo, Belo e Bem Gay. É uma das minhas favoritas do Neil Gaiman.', True)
        
        self.assertEqual(serie[0], registro_esperado)

    def teste_retorna_serie_id(self):
        db = Base_Midias('csv_teste/')
        serie = db.retorna_registro_id(0)
        registro_esperado = Registro(10, Serie('Good Omens', 'Comédia, Fantasia', 2019, 6, 55, 1, ['Michael Sheen', 'David Tennant', 'Frances McDormand', 'Jon Hamm']), 'Lindo, Belo e Bem Gay. É uma das minhas favoritas do Neil Gaiman.', True)
        
        self.assertEqual(serie, registro_esperado)
        
    def teste_retorna_filme_nome(self):
        db = Base_Midias('csv_teste/')
        filme = db.retorna_registro_por_nome('Click', tipo='Filme')
        registro_esperado = Registro(7.0, Filme('Click', 'Comédia, Drama, Fantasia', 2006, 107, ['Frank Coraci'], ['Adam Sandler', 'Kate Beckinsale', 'Christopher Walken']), 'Acredito que foi um bom filme, porém ficou visível que a ideia foi copiada do filme ""Do Que as Mulheres Gostam"" com Mel Gibson de 2001. A ideia de manipulação e controle é a mesma do filme de 2001, eles só mudaram um pouco o objeto de controle, porém o conteúdo é praticamente o mesmo.', True)
        
        self.assertEqual(filme[0], registro_esperado)
        
    def teste_retorna_filme_id(self):
        db = Base_Midias('csv_teste/')
        filme = db.retorna_registro_id(7)
        registro_esperado = Registro(7.0, Filme('Click', 'Comédia, Drama, Fantasia', 2006, 107, ['Frank Coraci'], ['Adam Sandler', 'Kate Beckinsale', 'Christopher Walken']), 'Acredito que foi um bom filme, porém ficou visível que a ideia foi copiada do filme ""Do Que as Mulheres Gostam"" com Mel Gibson de 2001. A ideia de manipulação e controle é a mesma do filme de 2001, eles só mudaram um pouco o objeto de controle, porém o conteúdo é praticamente o mesmo.', True)
        
        self.assertEqual(filme, registro_esperado)
        
    def teste_retorna_livro_nome(self):
        db = Base_Midias('csv_teste/')
        livro = db.retorna_registro_por_nome('1984', tipo='Livro')
        registro_esperado = Registro(10, Livro('1984', 'Drama, Distopia, Ficção Científica', 1949, ['George Orwell'], 354), 'Obra prima sem igual. Não importa quando ou quantas vezes você o leia, sempre haverá uma percepção de algum aspecto da sociedade que você não tinha visto antes. Praticamente uma profecia do mundo pós moderno. Não é uma leitura fácil, definitivamente. Mas vale muito a pena.', True)
        
        self.assertEqual(livro[0], registro_esperado)
        
    def teste_retorna_livro_nome(self):
        db = Base_Midias('csv_teste/')
        livro = db.retorna_registro_id(10)
        registro_esperado = Registro(10, Livro('1984', 'Drama, Distopia, Ficção Científica', 1949, ['George Orwell'], 354), 'Obra prima sem igual. Não importa quando ou quantas vezes você o leia, sempre haverá uma percepção de algum aspecto da sociedade que você não tinha visto antes. Praticamente uma profecia do mundo pós moderno. Não é uma leitura fácil, definitivamente. Mas vale muito a pena.', True)
        
        self.assertEqual(livro, registro_esperado)
    
    def teste_retorna_multiplos_registros(self):
        db = Base_Midias('csv_teste/')
        regs = db.retorna_registro_por_nome('Good Omens')
        
        self.assertEqual(len(regs), 2)
    
    def teste_tipo_indisponível(self):
        db = Base_Midias('csv_teste/')
        
        self.assertEqual(db.retorna_registro_por_nome('Good Omens', tipo='Tipo'), 'Nenhum registro correspondente encontrado')

    def teste_rejeita_nomeRepetido_mesmoTipo(self):
        db = Base_Midias('csv_teste/')
        serie = Serie('Good Omens', 'Comédia, Fantasia', 2019, 6, 55, 1, ['Michael Sheen', 'David Tennant'])
        registro_novo = Registro(None, serie, None, False)
        
        self.assertFalse(db.verifica_permitido_adicionar(registro_novo, 'Série'))
    
    def teste_aceita_nomeRepetido_outroTipo(self):
        db = Base_Midias('csv_teste/')
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 2014, 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'])
        registro_novo = Registro(None, filme, None, False)
        
        self.assertTrue(db.verifica_permitido_adicionar(registro_novo, 'Filme'))
    
    def teste_rejeita_avalia_semAssistir(self):
        db = Base_Midias('csv_teste/')
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo = Registro(8.8, filme, None, False)
        
        self.assertFalse(db.verifica_permitido_adicionar(registro_novo, 'Filme'))
    
    def teste_rejeita_comenta_semAssistir(self):
        db = Base_Midias('csv_teste/')
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo = Registro(None, filme, 'Muito bom!', False)

        self.assertFalse(db.verifica_permitido_adicionar(registro_novo, 'Filme'))
    
    def teste_adiciona_serie(self):
        db = Base_Midias('csv_teste/')
        serie = Serie('Brooklyn Nine-Nine', 'Comédia', 2013, 153, 22, 8, ['Andy Samberg', 'Stephanie Beatriz', 'Terry Crews'])
        registro_novo = Registro(7.8, serie, None, True)

        db.adiciona_serie(registro_novo)
        resgata_registro = db.retorna_registro_por_nome('Brooklyn Nine-Nine')

        self.assertEqual(resgata_registro[0], registro_novo)
    
    def teste_adiciona_filme(self):
        db = Base_Midias('csv_teste/')
        filme = Filme('Shang-Chi e a Lenda dos Dez Anéis', 'Ação, Aventura, Fantasia', 2021, 132, ['Destin Daniel Cretton'], ['Simu Liu', 'Awkwafina', 'Tony Chiu-Wai Leung'])
        registro_novo = Registro(8.8, filme, 'Muito bom!', True)

        db.adiciona_filme(registro_novo)
        resgata_registro = db.retorna_registro_por_nome('Shang-Chi e a Lenda dos Dez Anéis')

        self.assertEqual(registro_novo, resgata_registro[0])
    
    def teste_adiciona_livro(self):
        db = Base_Midias('csv_teste/')
        livro = Livro('Revolução dos Bichos', 'Sátira Política', 1945, ['George Orwell'], 112)
        registro_novo = Registro(8.9, livro, None, True)

        db.adiciona_livro(registro_novo)
        resgata_registro = db.retorna_registro_por_nome('Revolução dos Bichos')

        self.assertEqual(registro_novo, resgata_registro[0])

    def teste_mesmoID_difentesDFs(self):
        db = Base_Midias('csv_teste/')
        filme = Filme('A Culpa é das Estrelas', 'Drama, Romance', 2014, 126, ['Josh Boone'], ['Shailene Woodley', 'Ansel Elgort'])
        registro_novo = Registro(None, filme, None, False)

        db.adiciona_filme(registro_novo)
        id_registros = db.db_registros.loc[db.db_registros.index.max()]['id']
        id_filmes = db.db_filmes.loc[db.db_filmes.index.max()]['id']
        
        self.assertEqual(id_registros, id_filmes)

    def teste_remove_nao_tem_na_base_nome(self):
        db = Base_Midias('csv_teste/')
        self.assertEqual(db.remove_registro_nome('NaoEstaNaBase', tipo='Série'), 'Nenhum registro correspondente encontrado')
    
    def teste_remove_nao_tem_na_base_id(self):
        db = Base_Midias('csv_teste/')
        self.assertEqual(db.remove_registro_id(-7), 'Nenhum registro correspondente encontrado')

    def teste_remove_serie_nome(self):
        db = Base_Midias('csv_teste/')
        db.remove_registro_nome('Good Omens', tipo='Série')

        self.assertEqual(db.retorna_registro_por_nome('Good Omens', tipo='Série'), 'Nenhum registro correspondente encontrado')
    
    def teste_remove_filme_nome(self):
        db = Base_Midias('csv_teste/')
        db.remove_registro_nome('Click', tipo='Filme')

        self.assertEqual(db.retorna_registro_por_nome('Click', tipo='Filme'), 'Nenhum registro correspondente encontrado')
    
    def teste_remove_livro_nome(self):
        db = Base_Midias('csv_teste/')
        db.remove_registro_nome('1984', tipo='Livro')

        self.assertEqual(db.retorna_registro_por_nome('1984', tipo='Livro'), 'Nenhum registro correspondente encontrado')

    def teste_remove_serie_id(self):
        db = Base_Midias('csv_teste/')
        db.remove_registro_id(0)

        self.assertEqual(db.retorna_registro_id(0), 'Nenhum registro correspondente encontrado')
    
    def teste_remove_filme_id(self):
        db = Base_Midias('csv_teste/')
        db.remove_registro_id(7)

        self.assertEqual(db.retorna_registro_id(7), 'Nenhum registro correspondente encontrado')
    
    def teste_remove_livro_id(self):
        db = Base_Midias('csv_teste/')
        db.remove_registro_id(10)

        self.assertEqual(db.retorna_registro_id(10), 'Nenhum registro correspondente encontrado')