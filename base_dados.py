import pandas as pd

from midia import *
from registro import Registro

class Base_Midias():
    db_registros = pd.DataFrame #DataFrame de colunas comuns aos tipos
    db_series = pd.DataFrame #DataFrame de colunas somente sobre séries
    db_filmes = pd.DataFrame #DataFrame de colunas somente sobre filmes
    db_livros = pd.DataFrame #DataFrame de colunas somente sobre livros
    endereco_pasta = str #Endereço da pasta onde se encontram os csv's

    def __init__(self, endereco):
        self.db_registros = pd.read_csv(endereco+'registros.csv', sep=';')
        self.db_series = pd.read_csv(endereco+'series.csv', sep=';')
        self.db_filmes = pd.read_csv(endereco+'filmes.csv', sep=';')
        self.db_livros = pd.read_csv(endereco+'livros.csv', sep=';')
        self.endereco_pasta = endereco

    #Retorna instância da classe Série com dados da linha com certo id
    def retorna_serie(self, id_serie, registro):
        serie_correspondente = self.db_series[self.db_series['id'] == id_serie]
        serie = Serie(registro['nome'].values[0], registro['genero'].values[0], registro['ano_lancamento'].values[0], 
                      serie_correspondente['num_episodios'].values[0], serie_correspondente['tempo_por_ep'].values[0], 
                      serie_correspondente['num_temporadas'].values[0], 
                      serie_correspondente['elenco'].values[0].split(', '))
        return serie
    
    #Retorna instância da classe Filme com dados da linha com certo id
    def retorna_filme(self, id_filme, registro):
        filme_correspondente = self.db_filmes[self.db_filmes['id'] == id_filme]
        filme = Filme(registro['nome'].values[0], registro['genero'].values[0], registro['ano_lancamento'].values[0], 
                      filme_correspondente['duracao'].values[0], filme_correspondente['diretor'].values[0].split(', '), 
                      filme_correspondente['elenco'].values[0].split(', '))
        return filme

    #Retorna instância da classe Livre com dados da linha com certo id
    def retorna_livro(self, id_livro, registro):
        livro_correspondente = self.db_livros[self.db_livros['id'] == id_livro]
        livro = Livro(registro['nome'].values[0], registro['genero'].values[0], registro['ano_lancamento'].values[0], 
                    livro_correspondente['autor'].values[0].split(', '), livro_correspondente['num_paginas'].values[0])
        return livro

    #Retorna os registros com nome correpondente, podendo o tipo da mídia ser especificado ou não
    def retorna_registro_por_nome(self, nome, tipo=False):
        registros_correspondentes = self.db_registros[self.db_registros['nome'] == nome]

        #Se tipo não foi especificado
        if tipo == False:
            registros = []
            #Retorna lista com os registros de todas as linhas com nome correspondente
            for _, linha in registros_correspondentes.iterrows():
                registros += self.retorna_registro_por_nome(linha['nome'], tipo=linha['tipo_midia'])
            
            if len(registros) > 0:
                return registros
        
        #Com tipo especificado, seleciona o registro correto
        registros_correspondentes = registros_correspondentes[registros_correspondentes['tipo_midia'] == tipo]
        if len(registros_correspondentes) == 0:
            return 'Nenhum registro correspondente encontrado'
        
        #Se for série, monta o registro
        if tipo == 'Série':
            id_serie = registros_correspondentes['id'].values[0]
            serie = self.retorna_serie(id_serie, registros_correspondentes)
            return [Registro(registros_correspondentes['nota'].values[0], serie, registros_correspondentes['comentario'].values[0], 
                            registros_correspondentes['ja_consumiu'].values[0])]

        #Se for filme, monta o registro
        elif tipo == 'Filme':
            id_filme = registros_correspondentes['id'].values[0]
            filme = self.retorna_filme(id_filme, registros_correspondentes)
            return [Registro(registros_correspondentes['nota'].values[0], filme, registros_correspondentes['comentario'].values[0], 
                            registros_correspondentes['ja_consumiu'].values[0])]

        #Se for livro, monta o registro
        elif tipo == 'Livro':
            id_livro = registros_correspondentes['id'].values[0]
            livro = self.retorna_livro(id_livro, registros_correspondentes)
            return [Registro(registros_correspondentes['nota'].values[0], livro, registros_correspondentes['comentario'].values[0], 
                            registros_correspondentes['ja_consumiu'].values[0])]

    #Retorna os registros com id correpondente
    def retorna_registro_id(self, num_id):
        #Seleciona o registro correspondente ao id
        registro_correspondente = self.db_registros[self.db_registros['id'] == num_id]

        if len(registro_correspondente) == 0:
            return 'Nenhum registro correspondente encontrado'
        
        #Identifica o tipo da mídia
        tipo = registro_correspondente['tipo_midia'].values[0]
        
        if tipo == 'Série':
            serie = self.retorna_serie(num_id, registro_correspondente)
            return Registro(registro_correspondente['nota'].values[0], serie, registro_correspondente['comentario'].values[0], 
                            registro_correspondente['ja_consumiu'].values[0])

        elif tipo == 'Filme':
            filme = self.retorna_filme(num_id, registro_correspondente)
            return Registro(registro_correspondente['nota'].values[0], filme, registro_correspondente['comentario'].values[0], 
                            registro_correspondente['ja_consumiu'].values[0])

        elif tipo == 'Livro':
            livro = self.retorna_livro(num_id, registro_correspondente)
            return Registro(registro_correspondente['nota'].values[0], livro, registro_correspondente['comentario'].values[0], 
                            registro_correspondente['ja_consumiu'].values[0])

    def verifica_permitido_adicionar(self, registro, tipo):
        #Se houver mídia de mesmo nome e tipo, considera que já está na base de dados
        mesmo_nome = self.db_registros[self.db_registros['nome'] == registro.midia.nome]
        if len(mesmo_nome[mesmo_nome['tipo_midia'] == tipo]) > 0:
            return False
        
        #Se ainda não consumiu a mídia, não pode avaliá-la ou comentá-la
        if registro.ja_consumiu == False and (registro.nota != None or registro.comentario != None):
            return False
        
        return True
    
    #Adiciona as colunas em db_registro, comuns a todas as mídias
    def adiciona_colunas_comuns(self, registro, ind, tipo):
        self.db_registros.loc[self.db_registros.index.max()+1] = [ind, registro.midia.nome, registro.midia.genero, registro.midia.ano, 
                                                                  tipo, registro.nota, registro.comentario, registro.ja_consumiu]

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
            elenco = elenco[:-2]
        else:
            elenco = None
        
        self.db_series.loc[self.db_series.index.max()+1] = [ind, registro.midia.episodios, registro.midia.temporadas, registro.midia.tempo_episodio, elenco]

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
            elenco = elenco[:-2]
        else:
            elenco = None
        
        #Transforma a lista de diretores em string com seus nomes
        if registro.midia.diretor != None:
            diretores = ''
            for n in registro.midia.diretor:
                diretores += n + ', '
            diretores = diretores[:-2]
        else:
            diretores = None
        
        self.db_filmes.loc[self.db_filmes.index.max()+1] = [ind, registro.midia.duracao, diretores, elenco]

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
            autores = autores[:-2]
        else:
            autores = None
        
        self.db_livros.loc[self.db_livros.index.max()+1] = [ind, registro.midia.paginas, autores]

    #Remove série do DataFrame específico
    def remove_serie(self, num_id):
        serie_correspondente = self.db_series[self.db_series['id'] == num_id]

        ind = serie_correspondente.index[0]
        self.db_series = self.db_series.drop(ind)
    
    #Remove livro do DataFrame específico
    def remove_livro(self, num_id):
        livro_correspondente = self.db_livros[self.db_livros['id'] == num_id]

        ind = livro_correspondente.index[0]
        self.db_livros = self.db_livros.drop(ind)

    #Remove filme do DataFrame específico
    def remove_filme(self, num_id):
        filme_correspondente = self.db_filmes[self.db_filmes['id'] == num_id]

        ind = filme_correspondente.index[0]
        self.db_filmes = self.db_filmes.drop(ind)
    
    #Remove registro identificado pelo nome; tipo não precisa ser indicado se só houver um registro com nome igual
    def remove_registro_nome(self, nome, tipo=False):
        registros_correspondentes = self.db_registros[self.db_registros['nome'] == nome]

        if tipo == False and len(registros_correspondentes) > 1: #Se há mais de um registro, precisa especificar o tipo
            return 'Informação de tipo de mídia necessária'
        elif tipo == False and len(registros_correspondentes) == 1: #Se há só um, infere o tipo
            tipo = registros_correspondentes['tipo_midia'].values[0]
        
        #Seleciona o registro do tipo informado
        registro_correspondente = registros_correspondentes[registros_correspondentes['tipo_midia'] == tipo]
        if len(registro_correspondente) == 0:
            return 'Nenhum registro correspondente encontrado'
        
        ind = registro_correspondente.index[0] #Índice do registro
        num_id = registro_correspondente['id'].values[0] #Identifica o id do registro
        self.db_registros = self.db_registros.drop(ind) #Remove a linha do DataFrame geral

        #Remove registro dos DataFrame correspondentes
        if tipo == 'Série':
            self.remove_serie(num_id)
            return
        elif tipo == 'Livro':
            self.remove_livro(num_id)
            return
        elif tipo == 'Filme':
            self.remove_filme(num_id)
            return

    #Remove registro identificado pelo id
    def remove_registro_id(self, num_id):
        registro_correspondente = self.db_registros[self.db_registros['id'] == num_id]

        if len(registro_correspondente) == 0:
            return 'Nenhum registro correspondente encontrado'
        
        #Infere o tipo da mídia
        tipo = registro_correspondente['tipo_midia'].values[0]

        ind = registro_correspondente.index[0] #Índice do registro
        self.db_registros = self.db_registros.drop(ind) #Remove a linha do DataFrame geral

        #Remove registro dos DataFrame correspondentes
        if tipo == 'Série':
            self.remove_serie(num_id)
            return
        elif tipo == 'Livro':
            self.remove_livro(num_id)
            return
        elif tipo == 'Filme':
            self.remove_filme(num_id)
            return

    #Retorna os dataframes
    def retorna_dataframes(self):
        return self.db_registros, self.db_series, self.db_filmes, self.db_livros

    #Atualiza os arquivos .csv com os dataframes atuais
    def atualiza_arquivos(self):
        self.db_registros.to_csv(self.endereco_pasta+'registros.csv', sep=';', index=False)
        self.db_series.to_csv(self.endereco_pasta+'series.csv', sep=';', index=False)
        self.db_filmes.to_csv(self.endereco_pasta+'filmes.csv', sep=';', index=False)
        self.db_livros.to_csv(self.endereco_pasta+'livros.csv', sep=';', index=False)
