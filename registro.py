from dataclasses import dataclass

from midia import *

@dataclass
class Registro():
    nota: float
    midia: Midia
    comentario: str
    ja_consumiu: bool
