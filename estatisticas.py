import pandas as pd
from views import *


# Classe Estatistica serve para mostrar informações gerais
# a partir de um dataframe

class Estatistica:
    def __init__(self, df_registro):
        self.info_estats = df_registro

    def media(self, tipo):
        return(round(self.info_estats[tipo].mean(),2))

    def moda(self, tipo):
        df = self.info_estats[tipo].mode()
        return(df.to_string(index=False))

    def maximo(self, tipo):
        return(max(self.info_estats[tipo]))

    def minimo(self, tipo):
        return(min(self.info_estats[tipo]))

class EstRegistros(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def media_notas(self):
        print("A nota média das mídias selecionadas pelo filtro é:")
        print(self.media('nota'))

    def moda_notas(self):
        print("Nota(s) atribuída(s) com mais frequência:")
        print(self.moda('nota'))

    def maior_nota(self):
        print("A MAIOR nota atribuída às mídias selecionadas pelo filtro é:")
        print(self.maximo('nota'))

    def menor_nota(self):
        print("A MENOR nota atribuída às mídias selecionadas pelo filtro é:")
        print(self.minimo('nota'))

    def midia_mais_consumida(self):
        print("Mídia(s) mais consumida(s):")
        print(self.moda('tipo_midia'))

    def genero_mais_consumido(self):
        print("Gênero(s) mais consumido(s):")
        print(self.moda('genero'))

    def ano_com_mais_lancamentos(self):
        print("Ano(s) com maior número de lançamentos:")
        print(self.moda('ano_lancamento'))

    def est_geral(self):
        self.media_notas()
        print("\n")
        self.moda_notas()
        print("\n")
        self.maior_nota()
        print("\n")
        self.menor_nota()
        print("\n")
        self.midia_mais_consumida()
        print("\n")
        self.genero_mais_consumido()
        print("\n")
        self.ano_com_mais_lancamentos()
        print("\n")

class EstLivros(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def media_num_paginas(self):
        print("O número de páginas medio dos livros lidos é:")
        print(self.media('num_paginas'), ' páginas')

    def autor_mais_lido(self):
        print("Autor(es) mais lido(s):")
        print(self.moda('autor'))

    def est_geral_livros(self):
        self.media_num_paginas()
        print("\n")
        self.autor_mais_lido()
        print("\n")

class EstFilmes(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def duracao_media(self):
        print("A duração média dos filmes selecionados é:")
        print(self.media('duracao'), ' minutos')

    def diretor_mais_visto(self):
        print("Você assistiu mais filmes do(s) diretor(es):")
        print(self.moda('diretor'))

    def est_geral_filmes(self):
        self.duracao_media()
        print("\n")
        self.diretor_mais_visto()
        print("\n")

class EstSeries(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def num_medio_episodios(self):
        print("O número médio de episódios das séries vistas é:")
        print(self.media('num_episodios'))

    def serie_mais_episodios(self):
        print("Maior número de episódios assistidos:")
        print(self.maximo('num_episodios'))

    def num_medio_temporadas(self):
        print("O número médio de temporadas das séries vistas é:")
        print(self.media('num_temporadas'))

    def serie_mais_temporadas(self):
        print("Maior número de temporadas assistidas:")
        print(self.maximo('num_temporadas'))

    def tempo_medio_episodio(self):
        print("O tempo médio dos episódios das séries selecionadas é de:")
        print(self.media('tempo_por_ep'), ' minutos')

    def est_geral_series(self):
        self.num_medio_episodios()
        print("\n")
        self.serie_mais_episodios()
        print("\n")
        self.num_medio_temporadas()
        print("\n")
        self.serie_mais_temporadas()
        print("\n")
        self.tempo_medio_episodio()
        print("\n")



    