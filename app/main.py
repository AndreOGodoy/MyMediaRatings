import os
import pandas as pd

from app.registro import Registro
from app.interface import *

from app.utils import *

acoes = {
	'listar': (Interface, 'lista'),
	'adicionar': (Base_Midias, 'adiciona'),
	'remover': (Base_Midias, 'remove'),
	'estatisticas': (Interface, 'estatisticas'),
	'comentarios': (Interface, 'comentario')
}

tipos_midia = {
	'livro': 'Livro',
	'serie': 'Série',
	'filme': 'Filme',
	'geral': None
}

interface = Interface()

while(True):
	comando = input("Digite um comando (listar, estatisticas, adicionar, remover, comentarios, sair): ")

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
		getattr(acoes[acao][0], chamada)(interface) #chama o lista_x relacionado
	elif acao == 'adicionar':
		interface.input_midia(midia)
		midia_nova = interface.cria_midia(midia)
		registro_novo = interface.cria_registro(midia, midia_nova)
		interface.adicionar_registro(registro_novo, acoes[acao][0], chamada)
	elif acao == 'remover':
		nome = input(f"Digite o nome da(o) {midia}: ")
		interface.remover_registro(nome, tipos_midia[midia])
	elif acao == 'estatisticas':
		getattr(acoes[acao][0], chamada)(interface) #chama o estatistica_x relacionado
	elif acao == 'comentarios':
		interface.comentario_midia(tipos_midia[midia])

