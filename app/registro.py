from dataclasses import dataclass

from app.midia import *

@dataclass
class Registro():
    nota: float
    midia: Midia
    comentario: str
    ja_consumiu: bool
