from odmantic import Model, Reference
from typing import List

class Filme(Model):
    titulo: str
    diretor: str
    anoLancamento: int
    sinopse: str
    duracao: int
    genero: str

class Usuario(Model):
    nome: str
    email: str

class ListaFavoritos(Model):
    nome: str
    usuario: Usuario = Reference()  # Associação: cada lista pertence a um usuário
    filmes: List[Filme] = []         # Associação: muitos-para-muitos com Filme

class Avaliacao(Model):
    nota: int
    comentario: str
    usuario: Usuario = Reference()  # Cada avaliação está associada a um usuário
    filme: Filme = Reference()      # Cada avaliação está associada a um filme
