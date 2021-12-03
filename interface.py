from views import *
from base_dados import *
from midia import *

class Interface():
	def __init__(self):
		self._view = View()
		self._db = Base_Midias('csv/')
		self._dados_midia = []

	def lista_livro(self):
		filtros = ['nome', 'num_paginas', 'autor', 'nota']

		for filtro in filtros:
			self._view.filtra_por(filtro)

		pred = lambda x: x == 'Livro'
		self._view.filtra_por('tipo_midia', pred)
		self._view._composicao.drop('tipo_midia', axis=1, inplace=True)

		print(self._view._composicao)
		print()

		self._view = View()

	def lista_filme(self):
		filtros = ['nome', 'duracao', 'diretor', 'nota', 'elenco_y']

		for filtro in filtros:
			self._view.filtra_por(filtro)

		pred = lambda x: x == 'Filme'
		self._view.filtra_por('tipo_midia', pred)
		self._view._composicao.drop('tipo_midia', axis=1, inplace=True)

		print(self._view._composicao)
		print()

		self._view = View()

	def lista_serie(self):
		filtros = ['nome', 'num_episodios', 'num_temporadas', 'tempo_por_ep', 'nota', 'elenco_x']

		for filtro in filtros:
			self._view.filtra_por(filtro)

		pred = lambda x: x == 'Série'
		self._view.filtra_por('tipo_midia', pred)
		self._view._composicao.drop('tipo_midia', axis=1, inplace=True)

		print(self._view._composicao)
		print()

		self._view = View()

	def limpa_dados(self):
		self._dados_midia = []

	def input_filme(self):
		self._dados_midia.append(int(input("Digite a duração do filme: ")))
		
		diretores = input("Digite o(s) nome(s) do(s) diretor(es): ")
		elenco = input("Digite o nome do elenco: ")		

		self._dados_midia.append(diretores.split(','))
		self._dados_midia.append(elenco.split(','))

	def input_serie(self):
		self._dados_midia.append(int(input("Digite o número de número de episódios: ")))		
		self._dados_midia.append(int(input("Digite o tempo por episódio: ")))		
		self._dados_midia.append(int(input("Digite o número de temporadas: ")))					

		elenco = input(f"Digite o nome do elenco: ")
		self._dados_midia.append(elenco.split(','))			

	def input_livro(self):
		autores = input("Digite o(s) nome(s) do(s) autor(es): ")
		self._dados_midia.append(autores.split(','))

		self._dados_midia.append(int(input("Digite o número de páginas: ")))

	def input_midia(self, midia):
		self._dados_midia.append(input(f"Digite o nome do(a) {midia}: "))
		self._dados_midia.append(input(f"Digite o genero do(a) {midia}: "))
		self._dados_midia.append(int(input("Digite o ano de lançamento: ")))

		if midia == 'filme':
			self.input_filme()

		elif midia == 'serie':
			self.input_serie()

		elif midia == 'livro':
			self.input_livro()


	def input_registro(self, midia):
		self.limpa_dados()

		nota = int(input(f"De uma nota para a(o) {midia}: "))
		comentario = input(f"Deixe um comentario sobre a(o) {midia}: ")
		consumiu = input(f"Você ja leu/viu a(o) {midia}? (S/N): ")

		booleano = None
		if consumiu in ['Sim', 'S', 's', 'sim', 'Y', 'Yes', 'yes', 'y']:
			booleano = True
		else:
			booleano = False

		return nota, comentario, booleano

	def cria_midia(self, midia):
		nova_midia = None

		if midia == 'livro':
			nova_midia = Livro(*self._dados_midia)
		elif midia == 'filme':
			nova_midia = Filme(*self._dados_midia)
		elif midia == 'serie':
			nova_midia = series(*self._dados_midia)
 		
		return nova_midia