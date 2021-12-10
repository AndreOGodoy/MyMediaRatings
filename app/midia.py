from dataclasses import dataclass

@dataclass
class Midia():
    nome: str
    genero: str
    ano: int
    
@dataclass
class Filme(Midia):
    duracao: int 
    diretor: [str]
    elenco: [str]
    
@dataclass
class Serie(Midia):
    episodios: int
    tempo_episodio: int
    temporadas: int
    elenco: [str]

@dataclass
class Livro(Midia):
    autor: [str]
    paginas: int
