import pandas as pd

from midia import *
from registro import Registro

class Base_Midias():
    db_registros = pd.read_csv('csv/registros.csv', sep=';')
    db_series = pd.read_csv('csv/series.csv', sep=';')
    db_filmes = pd.read_csv('csv/filmes.csv', sep=';')
    db_livros = pd.read_csv('csv/livros.csv', sep=';')

    def verifica_permitido_adicionar(self, registro, tipo):
        #Se houver mídia de mesmo nome e tipo, considera que já está na base de dados
        mesmo_nome = self.db_registros[self.db_registros['nome'] == registro.midia.nome]
        if len(mesmo_nome[mesmo_nome['tipo_midia'] == tipo]) > 0:
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
        if self.verifica_permitido_adicionar(registro, 'Série') == False:
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
        if self.verifica_permitido_adicionar(registro, 'Filme') == False:
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
        if self.verifica_permitido_adicionar(registro, 'Livro') == False:
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

    def retorna_midia_nome(self, nome, tipo=False):
        registros_correspondentes = self.db_registros[self.db_registros['nome'] == nome]

        if tipo == False:
            registros = []
            for _, linha in registros_correspondentes.iterrows():
                registros += self.retorna_midia_nome(linha['nome'], tipo=linha['tipo_midia'])
            return registros
        
        registros_correspondentes = registros_correspondentes[registros_correspondentes['tipo_midia'] == tipo]
        if len(registros_correspondentes) == 0:
            return False
        
        if tipo == 'Série':
            id_serie = registros_correspondentes['id'].values[0]
            serie_correspondente = self.db_series[self.db_series['id'] == id_serie]
            serie = Serie(registros_correspondentes['nome'].values[0], registros_correspondentes['genero'].values[0], 
                        serie_correspondente['num_episodios'].values[0], serie_correspondente['tempo_por_ep'].values[0], 
                        serie_correspondente['num_temporadas'].values[0], serie_correspondente['ano_lancamento'].values[0], 
                        serie_correspondente['elenco'].values[0].split(', '))
            return [Registro(registros_correspondentes['nota'].values[0], serie, registros_correspondentes['comentario'].values[0], 
                            registros_correspondentes['ja_consumiu'].values[0])]

        elif tipo == 'Filme':
            id_filme = registros_correspondentes['id'].values[0]
            filme_correspondente = self.db_filmes[self.db_filmes['id'] == id_filme]
            filme = Filme(registros_correspondentes['nome'].values[0], registros_correspondentes['genero'].values[0], 
                        filme_correspondente['duracao'].values[0], filme_correspondente['diretor'].values[0].split(', '), 
                        filme_correspondente['elenco'].values[0].split(', '), filme_correspondente['ano_lancamento'].values[0])
            return [Registro(registros_correspondentes['nota'].values[0], filme, registros_correspondentes['comentario'].values[0], 
                            registros_correspondentes['ja_consumiu'].values[0])]

        elif tipo == 'Livro':
            id_livro = registros_correspondentes['id'].values[0]
            livro_correspondente = self.db_livros[self.db_livros['id'] == id_livro]
            livro = Livro(registros_correspondentes['nome'].values[0], registros_correspondentes['genero'].values[0], 
                        livro_correspondente['autor'].values[0].split(', '), livro_correspondente['num_paginas'].values[0], 
                        livro_correspondente['ano_lancamento'].values[0])
            return [Registro(registros_correspondentes['nota'].values[0], livro, registros_correspondentes['comentario'].values[0], 
                            registros_correspondentes['ja_consumiu'].values[0])]

    #Atualiza os arquivos .csv com os dataframes atuais
    def atualiza_arquivos(self):
        self.db_registros.to_csv('csv/registros.csv', sep=';', index=False)
        self.db_series.to_csv('csv/series.csv', sep=';', index=False)
        self.db_filmes.to_csv('csv/filmes.csv', sep=';', index=False)
        self.db_livros.to_csv('csv/livros.csv', sep=';', index=False)
