from views import *
from midia import *

class Interface():
	def __init__(self):
		self._view = View()
		self._db = Base_Midias('csv/')

	def lista_livro(self):
		self._view.filtros = ['nome', 'num_paginas', 'autor', 'nota']
		
		print(self._view)
		print()

		self._view.filtros = []

	def lista_filme(self):
		self._view.filtros = ['nome', 'duracao', 'diretor', 'nota']
		
		print(self._view)
		print()

		self._view.filtros = []

	def lista_serie(self):
		self._view.filtros = ['nome', 'num_episodios', 'num_temporadas', 'tempo_por_ep', 'nota']
		
		print(self._view)
		print()

		self._view.filtros = []

	def cria_midia(self, midia, dados):
		nova_midia = None

		if midia == 'livro':
			nova_midia = Livro(*dados)
		elif midia == 'filme':
			nova_midia = Filme(*dados)
		elif midia == 'serie':
			nova_midia = series(*dados)
 		
		return nova_midia