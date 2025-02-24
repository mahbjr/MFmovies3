from fastapi import APIRouter, HTTPException
from database import get_engine
from modelos import ListaFavoritos, Filme, Usuario
from odmantic import ObjectId

router = APIRouter(
    prefix="/listaFavoritos",  # Prefixo para todas as rotas desta entidade
    tags=["ListaFavoritos"],   # Tag para documentação automática
)

engine = get_engine()

@router.get("/", response_model=list[ListaFavoritos])
async def get_all_listas() -> list[ListaFavoritos]:
    """
    Retorna todas as listas de favoritos cadastradas.
    """
    listas = await engine.find(ListaFavoritos)
    return listas

@router.get("/{lista_id}", response_model=ListaFavoritos)
async def get_lista(lista_id: str) -> ListaFavoritos:
    """
    Retorna uma lista de favoritos pelo ID.
    """
    lista = await engine.find_one(ListaFavoritos, ListaFavoritos.id == ObjectId(lista_id))
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de Favoritos não encontrada")
    return lista

@router.post("/", response_model=ListaFavoritos)
async def create_lista(lista: ListaFavoritos) -> ListaFavoritos:
    """
    Cria uma nova lista de favoritos.
    """
    if not lista.usuario:
        raise HTTPException(status_code=400, detail="Usuario é necessário para a Lista de Favoritos")
    # Verifica se o usuário associado existe
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(lista.usuario.id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    lista.usuario = usuario
    await engine.save(lista)
    return lista

@router.put("/{lista_id}", response_model=ListaFavoritos)
async def update_lista(lista_id: str, lista_data: dict) -> ListaFavoritos:
    """
    Atualiza uma lista de favoritos pelo ID utilizando os dados enviados como dicionário.
    """
    lista = await engine.find_one(ListaFavoritos, ListaFavoritos.id == ObjectId(lista_id))
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de Favoritos não encontrada")
    for key, value in lista_data.items():
        setattr(lista, key, value)
    await engine.save(lista)
    return lista

@router.delete("/{lista_id}")
async def delete_lista(lista_id: str) -> dict:
    """
    Deleta uma lista de favoritos pelo ID.
    """
    lista = await engine.find_one(ListaFavoritos, ListaFavoritos.id == ObjectId(lista_id))
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de Favoritos não encontrada")
    await engine.delete(lista)
    return {"message": "Lista de Favoritos deleted"}

@router.post("/{lista_id}/filmes/{filme_id}", response_model=ListaFavoritos)
async def add_filme_to_lista(lista_id: str, filme_id: str) -> ListaFavoritos:
    """
    Adiciona um filme à lista de favoritos.
    """
    lista = await engine.find_one(ListaFavoritos, ListaFavoritos.id == ObjectId(lista_id))
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de Favoritos não encontrada")
    
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrada")
    
    if filme not in lista.filmes:
        lista.filmes.append(filme)
        await engine.save(lista)
    return lista

@router.delete("/{lista_id}/filmes/{filme_id}", response_model=ListaFavoritos)
async def remove_filme_from_lista(lista_id: str, filme_id: str) -> ListaFavoritos:
    """
    Remove um filme da lista de favoritos.
    """
    lista = await engine.find_one(ListaFavoritos, ListaFavoritos.id == ObjectId(lista_id))
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de Favoritos não encontrada")
    
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrada")
    
    if filme in lista.filmes:
        lista.filmes.remove(filme)
        await engine.save(lista)
    return lista
