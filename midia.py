from dataclasses import dataclass

@dataclass
class Midia():
    nome: str
    genero: str
    
@dataclass
class Filme(Midia):
    duracao: int 
    diretor: str
    
@dataclass
class Serie(Midia):
    episodios: int
    temporadas: int
    lista_atores: [str]

@dataclass
class Livro(Midia):
    autor: str
    paginas: int

