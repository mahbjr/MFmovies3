# Catalágo de Filmes

## Diagrama de Classes UML

```mermaid
classDiagram
direction LR
class Filme {
    +int id
    +string titulo
    +string diretor
    +int anoLancamento
    +string sinopse
    +int duracao
    +string genero
}

class Usuario {
    +int id
    +string nome
    +string email
}

class ListaFavoritos {
    +int id
    +string nome
}

class Avaliacao {
    +int id
    +int nota
    +string comentario
}

Usuario "1" -- "*" ListaFavoritos
ListaFavoritos "*" -- "*" Filme
Usuario "1" -- "*" Avaliacao
Avaliacao "*" -- "1" Filme
