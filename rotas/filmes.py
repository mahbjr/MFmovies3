from fastapi import APIRouter, HTTPException
from database import get_engine
from modelos import Filme
from odmantic import ObjectId

router = APIRouter(
    prefix="/filmes",  # Prefixo para todas as rotas
    tags=["Filmes"],   # Tag para documentação automática
)

engine = get_engine()

@router.get("/filmes/", response_model=list[Filme])
async def get_all_filmes() -> list[Filme]:
    """
    Retorna todos os filmes cadastrados.
    """
    filmes = await engine.find(Filme)
    return filmes

@router.get("/filmes/{filme_id}", response_model=Filme)
async def get_filme(filme_id: str) -> Filme:
    """
    Retorna um filme pelo ID.
    """
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme not found")
    return filme

@router.post("/filmes/", response_model=Filme)
async def create_filme(filme: Filme) -> Filme:
    """
    Cria um novo filme.
    """
    await engine.save(filme)
    return filme

@router.delete("/filmes/{filme_id}")
async def delete_filme(filme_id: str) -> dict:
    """
    Deleta um filme pelo ID.
    """
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme not found")
    await engine.delete(filme)
    return {"message": "Filme deleted"}
