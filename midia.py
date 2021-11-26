from dataclasses import dataclass

@dataclass
class Midia():
    nome: str
    genero: str
    
@dataclass
class Filme(Midia):
    duracao: int 
    diretor: [str]
    elenco: [str]
    ano: int
    
@dataclass
class Serie(Midia):
    episodios: int
    tempo_episodio: int
    temporadas: int
    ano: int
    elenco: [str]

@dataclass
class Livro(Midia):
    autor: [str]
    paginas: int
    ano: int
