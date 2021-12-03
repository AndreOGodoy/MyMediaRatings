import os
import pandas as pd

from registro import Registro
from interface import *

from utils import *

acoes = {
	'listar': (Interface, 'lista'),
	'adicionar': (Base_Midias, 'adiciona'),
	'remover': (Base_Midias, 'remove')
}

tipos_midia = {
	'livro': 'Livro',
	'serie': 'Série',
	'filme': 'Filme',
}

interface = Interface()

while(True):
	comando = input("Digite um comando: ")

	if comando == "sair":
		break
	elif len(comando.split()) != 2:
		help()
		continue

	acao, midia = comando.split()

	if acao not in acoes:
		acao_invalida(acoes)	
		continue
	elif midia not in tipos_midia:
		midia_invalida(tipos_midia)
		continue

	chamada = acoes[acao][1] + '_' + midia 

	if acao == 'listar':
		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface)
	elif acao == 'adicionar':
		interface.input_midia(midia)

		nova_midia = interface.cria_midia(midia)
		
		nota, comentario, booleano = interface.input_registro(midia)

		registro_novo = Registro(nota, nova_midia, comentario, booleano)

		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface._db, registro_novo)

		interface._db.atualiza_arquivos()
		interface._view = View()
	elif acao == 'remover':
		nome = input(f"Digite o nome da(o) {midia}: ")

		interface._db.remove_registro_nome(nome, tipos_midia[midia])

		interface._db.atualiza_arquivos()
		interface._view = View()
