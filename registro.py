from dataclasses import dataclass

from nota import Nota
from midia import *
from comentario import Comentario

@dataclass
class Registro():
    nota: Nota
    midia: Midia
    comentario: Comentario
    
def main():
    nota = Nota(10)
    midia = Livro("Teste", "TesteGenero", "TesteAutor", 200)
    comentario = Comentario("Um comentário teste")

    registro = Registro(nota, midia, comentario)
    
    
