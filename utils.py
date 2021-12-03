def acao_invalida(acoes):
	print("Essa ação não é válida. As ações válidas são: ", end='')
		
	for	key, value in acoes.items():
		print(key, end=' ')

	print()

def midia_invalida(midias):
	print("Essa mídia não é válida. As mídias válidas são: ", end='')
		
	for	key, value in midias.items():
		print(key, end=' ')

	print()

def help():
	print("Por favor, digite uma ação e uma mídia válida")