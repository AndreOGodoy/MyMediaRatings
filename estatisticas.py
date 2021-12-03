import pandas as pd

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

#Estatísticas para registro geral
class EstRegistros(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def media_notas(self):
        mensagem = "A nota média das mídias selecionadas pelo filtro é: "
        media = self.media('nota')
        return(mensagem + str(media))

    def moda_notas(self):
        mensagem = "Nota(s) atribuída(s) com mais frequência: "
        moda = self.moda('nota')
        return(mensagem + moda)

    def maior_nota(self):
        mensagem = "A MAIOR nota atribuída às mídias selecionadas pelo filtro é: "
        maximo = self.maximo('nota')
        return(mensagem + str(maximo))

    def menor_nota(self):
        mensagem = "A MENOR nota atribuída às mídias selecionadas pelo filtro é: "
        minimo = self.minimo('nota')
        return(mensagem + str(minimo))

    def midia_mais_consumida(self):
        mensagem = "Mídia(s) mais consumida(s): "
        midias = self.moda('tipo_midia')
        return(mensagem + midias)

    def genero_mais_consumido(self):
        mensagem = "Gênero(s) mais consumido(s): "
        generos = self.moda('genero')
        return(mensagem + generos)

    def ano_com_mais_lancamentos(self):
        mensagem = "Ano(s) com maior número de lançamentos: "
        anos = self.moda('ano_lancamento')
        return(mensagem + anos)

    def est_geral(self):
        print(self.media_notas())
        print("\n")
        print(self.moda_notas())
        print("\n")
        print(self.maior_nota())
        print("\n")
        print(self.menor_nota())
        print("\n")
        print(self.midia_mais_consumida())
        print("\n")
        print(self.genero_mais_consumido())
        print("\n")
        print(self.ano_com_mais_lancamentos())
        print("\n")

#Estatísticas exclusivas de livros
class EstLivros(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def media_num_paginas(self):
        mensagem = "O número de páginas médio dos livros lidos é: "
        paginas = str(self.media('num_paginas')) + ' páginas'
        return(mensagem + paginas)


    def autor_mais_lido(self):
        mensagem = "Autor(es) mais lido(s): "
        autor = self.moda('autor')
        return(mensagem + autor)

    def est_geral_livros(self):
        print(self.media_num_paginas())
        print("\n")
        print(self.autor_mais_lido())
        print("\n")

#Estatísticas exclusivas de filmes
class EstFilmes(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def duracao_media(self):
        mensagem = "A duração média dos filmes selecionados é: "
        duracao = str(self.media('duracao')) + ' minutos'
        return(mensagem + duracao)

    def diretor_mais_visto(self):
        mensagem = "Você assistiu mais filmes do(s) diretor(es): "
        diretor = self.moda('diretor')
        return(mensagem + diretor)

    def est_geral_filmes(self):
        print(self.duracao_media())
        print("\n")
        print(self.diretor_mais_visto())
        print("\n")

#Estatísticas exclusivas de séries
class EstSeries(Estatistica):
    def __init__(self, df_registro):
        super().__init__(df_registro)

    def num_medio_episodios(self):
        mensagem = "O número médio de episódios das séries vistas é: "
        episodios = str(self.media('num_episodios'))
        return(mensagem + episodios)

    def serie_mais_episodios(self):
        mensagem = "Maior número de episódios assistidos: "
        maior = str(self.maximo('num_episodios'))
        return(mensagem + maior)

    def num_medio_temporadas(self):
        mensagem = "O número médio de temporadas das séries vistas é: "
        temporadas = str(self.media('num_temporadas'))
        return(mensagem + temporadas)

    def serie_mais_temporadas(self):
        mensagem = "Maior número de temporadas assistidas: "
        maistemp = str(self.maximo('num_temporadas'))
        return(mensagem + maistemp)

    def tempo_medio_episodio(self):
        mensagem = "O tempo médio dos episódios das séries selecionadas é de: "
        tempo = str(self.media('tempo_por_ep')) + ' minutos'
        return(mensagem + tempo)

    def est_geral_series(self):
        print(self.num_medio_episodios())
        print("\n")
        print(self.serie_mais_episodios())
        print("\n")
        print(self.num_medio_temporadas())
        print("\n")
        print(self.serie_mais_temporadas())
        print("\n")
        print(self.tempo_medio_episodio())
        print("\n")
