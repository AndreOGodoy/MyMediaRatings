# MyMediaRatings

## Grupo

- André de Oliveira Godoy
- Julia Fonseca de Sena
- Lucas Mariani Paiva Caldeira Brant
- Luiz Guilherme Leroy Vieira

## Interface

- Inicialmente pensado como programa em Linha de Comando
- Sistema de único usuário

## Funcionalidades

- [X] Banco de dados de mídias
- [X] Possibilidade de dar notas e fazer comentários nas mídias consumidas
- [X] Possibilidade de agrupar mídias em listagens variadas
- [X] Estatísticas relevantes:
	- [X] Nota média por categoria
	- [X] Tipos de mídia mais consumidos
	- [X] Gêneros mais consumidos
	- [X] Estatísticas específicas para livros, filmes e séries

## Funcionamento do Sistema

- Para executar o programa, no diretório raiz: python -m app
- Ao executar o programa, o usuário tem diversas opções acessíveis pela linha de comando:
	- listar -> mostra todos os dados das mídias de acordo com o filtro fornecido (exceto comentários)
	- estatisticas -> mostra as estatísticas relevantes de acordo com o filtro fornecido
	- adicionar -> adiciona uma mídia no banco de dados
	- remover -> remove uma mídia presente no banco de dados
	- comentário -> mostra os comentários do usuário de acordo com o filtro fornecido
	- sair -> termina a execução do programa
- Os filtros utilizados pelo sistema são:
	- geral
	- livro
	- filme
	- serie

## Tecnologias

- Python3
- Uso de CSV e Pandas como Banco de Dados

## Cobertura

- Link para o Codecov: https://app.codecov.io/gh/AndreOGodoy/MyMediaRatings
