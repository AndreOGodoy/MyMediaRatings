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
		dados_registro = input(f"Por favor informe os dados da(o) {midia}: ")

		dados = dados_registro.split()

		print(dados[:-3])

		nova_midia = interface.cria_midia(midia, dados[:-3])
		registro_novo = Registro(dados[-3], nova_midia, dados[-2], dados[-1])

		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface._db, registro_novo)
	elif acao == 'remover':
		identificador = input(f"Digite o nome da(o) {midia}: ")

		metodo = getattr(acoes[acao][0], chamada)
		metodo(interface._db, identificador)

