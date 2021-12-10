from app.views import *
from app.base_dados import *
from app.estatisticas import *
from app.midia import *

class Interface():
	def __init__(self, local_base='csv/'):
		self._view = View()
		self._db = Base_Midias(local_base)
		self._dados_midia = []
	
	def filtrar_midia(self, filtros, midia=None):
		for filtro in filtros:
			self._view.filtra_por(filtro)

		if midia != None:
			pred = lambda x: x == midia
			self._view.filtra_por('tipo_midia', pred)
			self._view._composicao.drop('tipo_midia', axis=1, inplace=True)

	def lista_geral(self):
		self._view = View() #atualiza a view, limpando os outros filtros	
		filtros = ['nome', 'genero', 'ano_lancamento', 'tipo_midia', 'nota', 'ja_consumiu']

		self.filtrar_midia(filtros)

		print(self._view._composicao)
		print()

	def lista_livro(self):
		self._view = View()
		filtros = ['nome', 'num_paginas', 'autor', 'nota']

		self.filtrar_midia(filtros, 'Livro')

		print(self._view._composicao)
		print()


	def lista_filme(self):
		self._view = View() 

		filtros = ['nome', 'duracao', 'diretor', 'nota', 'elenco_y']

		self.filtrar_midia(filtros, 'Filme')

		print(self._view._composicao)
		print()

	def lista_serie(self):
		self._view = View()
		filtros = ['nome', 'num_episodios', 'num_temporadas', 'tempo_por_ep', 'nota', 'elenco_x']

		self.filtrar_midia(filtros, 'Série')

		print(self._view._composicao)
		print()
	
	def comentario_midia(self, midia=None):
		self._view = View()
		self.filtrar_midia(['nome', 'comentario'], midia)
		self._view.remove_linhas_com_nan()

		print(self._view._composicao)
		print()
	
	def estatisticas_geral(self):
		filtros = ['nome', 'genero', 'ano_lancamento', 'tipo_midia', 'nota', 'ja_consumiu']

		self.filtrar_midia(filtros)

		est = EstRegistros(self._view._composicao)

		est.est_geral()

		self._view = View()

	def estatisticas_livro(self):
		filtros = ['nome', 'num_paginas', 'autor', 'nota']

		self.filtrar_midia(filtros, 'Livro')

		est = EstLivros(self._view._composicao)

		est.est_geral_livros()

		self._view = View()

	def estatisticas_serie(self):
		filtros = ['nome', 'num_episodios', 'num_temporadas', 'tempo_por_ep', 'nota', 'elenco_x']

		self.filtrar_midia(filtros, 'Série')

		est = EstSeries(self._view._composicao)

		est.est_geral_series()

		self._view = View()

	def estatisticas_filme(self):
		filtros = ['nome', 'duracao', 'diretor', 'nota', 'elenco_y']

		self.filtrar_midia(filtros, 'Filme')

		est = EstFilmes(self._view._composicao)

		est.est_geral_filmes()

		self._view = View()

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
		self._dados_midia = [] #limpa os dados antigos antes de inserir os novos
		
		self._dados_midia.append(input(f"Digite o nome do(a) {midia}: "))
		self._dados_midia.append(input(f"Digite o genero do(a) {midia}: "))
		self._dados_midia.append(int(input("Digite o ano de lançamento: ")))

		if midia == 'filme':
			self.input_filme()

		elif midia == 'serie':
			self.input_serie()

		elif midia == 'livro':
			self.input_livro()

	def cria_registro(self, tipo_midia, nova_midia):
		nota = int(input(f"De uma nota para a(o) {tipo_midia}: "))
		comentario = input(f"Deixe um comentario sobre a(o) {tipo_midia}: ")
		consumiu = input(f"Você ja leu/viu a(o) {tipo_midia}? (S/N): ")

		booleano = None
		if consumiu in ['Sim', 'S', 's', 'sim', 'Y', 'Yes', 'yes', 'y']:
			booleano = True
		else:
			booleano = False

		return Registro(nota, nova_midia, comentario, booleano)

	def cria_midia(self, midia):
		nova_midia = None

		if midia == 'livro':
			nova_midia = Livro(*self._dados_midia)
		elif midia == 'filme':
			nova_midia = Filme(*self._dados_midia)
		elif midia == 'serie':
			nova_midia = Serie(*self._dados_midia)
 		
		return nova_midia

	def adicionar_registro(self, registro_novo, classe_acao, chamada):
		metodo = getattr(classe_acao, chamada)
		metodo(self._db, registro_novo)

		self._db.atualiza_arquivos()
		self._view = View()
	
	def remover_registro(self, nome, tipo_midia):
		self._db.remove_registro_nome(nome, tipo_midia)

		self._db.atualiza_arquivos()
		self._view = View()

