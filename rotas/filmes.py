from fastapi import APIRouter, HTTPException
from database import get_engine
from modelos import Filme
from odmantic import ObjectId

router = APIRouter(
    prefix="/filmes",  # Prefixo para todas as rotas
    tags=["Filmes"],   # Tag para documentação automática
)

engine = get_engine()

@router.get("/", response_model=list[Filme])
async def get_all_filmes() -> list[Filme]:
    """
    Retorna todos os filmes cadastrados.
    """
    filmes = await engine.find(Filme)
    return filmes

@router.get("/{filme_id}", response_model=Filme)
async def get_filme(filme_id: str) -> Filme:
    """
    Retorna um filme pelo ID.
    """
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme not found")
    return filme

@router.post("/", response_model=Filme)
async def create_filme(filme: Filme) -> Filme:
    """
    Cria um novo filme.
    """
    await engine.save(filme)
    return filme


@router.put("/{filme_id}", response_model=Filme)
async def update_filme(filme_id: str, filme_data: dict) -> Filme:
    """
    Atualiza um filme pelo ID utilizando os dados enviados como dicionário.
    """
    filme_obj = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme_obj:
        raise HTTPException(status_code=404, detail="Filme not found")
    for key, value in filme_data.items():
        setattr(filme_obj, key, value)
    await engine.save(filme_obj)
    return filme_obj

@router.delete("/{filme_id}")
async def delete_filme(filme_id: str) -> dict:
    """
    Deleta um filme pelo ID.
    """
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme not found")
    await engine.delete(filme)
    return {"message": "Filme deleted"}
