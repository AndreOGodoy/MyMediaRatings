import pandas as pd

from midia import *
from registro import Registro

class Base_Midias():
    db_registros = pd.read_csv('csv/registros.csv', sep=';')
    db_series = pd.read_csv('csv/series.csv', sep=';')
    db_filmes = pd.read_csv('csv/filmes.csv', sep=';')
    db_livros = pd.read_csv('csv/livros.csv', sep=';')

    def verifica_permitido(self, registro, tipo):
        #Se houver mídia de mesmo nome e tipo, considera que já está na base de dados
        if len(self.db_registros[self.db_registros['nome'] == registro.midia.nome][self.db_registros['tipo_midia'] == tipo]) > 0:
            print('Mídia já está na base!')
            return False
        
        #Se ainda não consumiu a mídia, não pode avaliá-la ou comentá-la
        if registro.ja_consumiu == False and (registro.nota != None or registro.comentario != None):
            print('Não pode dar nota ou comentar antes de assistir!')
            return False
        
        return True
    
    #Adiciona as colunas em db_registro, comuns a todas as mídias
    def adiciona_colunas_comuns(self, registro, ind, tipo):
        self.db_registros.loc[self.db_registros.index.max()+1] = [ind, registro.midia.nome, registro.midia.genero, tipo, 
                                                                  registro.nota, registro.comentario, registro.ja_consumiu]

    #Adiciona série à base
    def adiciona_serie(self, registro):
        if self.verifica_permitido(registro, 'Série') == False:
            return

        ind = self.db_registros['id'].max() + 1 #Id da série sendo adicionada
        self.adiciona_colunas_comuns(registro, ind, 'Série')

        #Transforma a lista de elenco em string com os nomes do elenco
        if registro.midia.elenco != None:
            elenco = ''
            for n in registro.midia.elenco:
                elenco += n + ', '
            elenco += '\b\b'
        else:
            elenco = None
        
        self.db_series.loc[self.db_series.index.max()+1] = [ind, registro.midia.episodios, registro.midia.temporadas, registro.midia.ano, 
                                                            registro.midia.tempo_episodio, elenco]

    #Adiciona filme à base
    def adiciona_filme(self, registro):
        if self.verifica_permitido(registro, 'Filme') == False:
            return

        ind = self.db_registros['id'].max() + 1 #Id do filme sendo adicionado
        self.adiciona_colunas_comuns(registro, ind, 'Filme')

        #Transforma a lista de elenco em string com os nomes do elenco
        if registro.midia.elenco != None:
            elenco = ''
            for n in registro.midia.elenco:
                elenco += n + ', '
            elenco += '\b\b'
        else:
            elenco = None
        
        #Transforma a lista de diretores em string com seus nomes
        if registro.midia.diretor != None:
            diretores = ''
            for n in registro.midia.diretor:
                diretores += n + ', '
            diretores += '\b\b'
        else:
            diretores = None
        
        self.db_filmes.loc[self.db_filmes.index.max()+1] = [ind, registro.midia.duracao, diretores, elenco, registro.midia.ano]

    #Adiciona livro à base
    def adiciona_livro(self, registro):
        if self.verifica_permitido(registro, 'Livro') == False:
            return

        ind = self.db_registros['id'].max() + 1 #Id do livro sendo adicionado
        self.adiciona_colunas_comuns(registro, ind, 'Livro')

        ##Transforma a lista de autores em string com seus nomes
        if registro.midia.autor != None:
            autores = ''
            for n in registro.midia.autor:
                autores += n + ', '
            autores += '\b\b'
        else:
            autores = None
        
        self.db_livros.loc[self.db_livros.index.max()+1] = [ind, registro.midia.paginas, autores, registro.midia.ano]

    #Atualiza os arquivos .csv com os dataframes atuais
    def atualiza_arquivos(self):
        self.db_registros.to_csv('csv/registros.csv', sep=';', index=False)
        self.db_series.to_csv('csv/series.csv', sep=';', index=False)
        self.db_filmes.to_csv('csv/filmes.csv', sep=';', index=False)
        self.db_livros.to_csv('csv/livros.csv', sep=';', index=False)
