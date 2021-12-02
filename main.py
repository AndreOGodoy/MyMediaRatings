import os
import pandas as pd

from registro import Registro
from interface import *

def help():
	print("Por favor, digite uma acao e uma midia desejada")

acoes = {
	'listar': (Interface, 'lista'),
	'adicionar': (Base_Midias, 'adiciona'),
	'remover': (Base_Midias, 'remove')
}

midias = {
	'livro': '_livro',
	'serie': '_serie',
	'filme': '_filme',
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
	chamada = acoes[acao][1] + midias[midia]

	if acao == 'listar':
		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface)
	elif acao == 'adicionar':
		interface.input_midia(midia)

		nova_midia = interface.cria_midia(midia)
		interface.limpa_dados() #linpa os dados da midia para caso o usuario queira adicionar de novo no futuro
		
		nota, comentario, booleano = interface.input_registro(midia)

		registro_novo = Registro(nota, nova_midia, comentario, booleano)

		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface._view._instancia._instancia, registro_novo)

		interface._view._instancia._instancia.atualiza_arquivos()
		interface._view = View()
	elif acao == 'remover':
		identificador = input(f"Digite o nome da(o) {midia}: ")

		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface._db, identificador)

		interface._view._instancia.atualizar_arquivos()
