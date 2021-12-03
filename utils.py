def acao_invalida(acoes):
	print("Essa acao nao e valida. As acoes validas sao: ", end='')
		
	for	key, value in acoes.items():
		print(key, end=' ')

	print()

def midia_invalida(midias):
	print("Essa midia nao e valida. As midias validas sao: ", end='')
		
	for	key, value in midias.items():
		print(key, end=' ')

	print()

def help():
	print("Por favor, digite uma acao e uma midia valida")