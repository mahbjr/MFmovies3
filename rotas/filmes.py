from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from database import get_engine, db
from modelos import Avaliacao, Filme
from odmantic import AIOEngine, ObjectId

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

@router.get("/filmes/search", response_model=list[Filme])
async def search_filmes(titulo: str):
    """
    Busca filmes que contenham o texto informado no título (case insensitive)
    """
    query = {"titulo": {"$regex": titulo, "$options": "i"}}
    filmes = await engine.find(Filme, query)
    if not filmes:
        raise HTTPException(status_code=404, detail="Nenhum filme encontrado com o título informado")
    return filmes

@router.get("/filmes/ano")
async def filmes_por_ano(ano: int):
    try:
        ano = int(ano)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ano deve ser um integer")
    
    filmes = await engine.find(Filme, Filme.anoLancamento == ano)
    return filmes

@router.get("/filmes/contagem/total")
async def count_filmes() -> dict:
    """
    Conta o número total de filmes na coleção.
    """
    total = await db.filme.count_documents({})
    return {"totalFilmes": total}

@router.get("/filmes/contagem/por-genero")
async def filmes_por_genero():
    pipeline = [
        {"$group": {"_id": "$genero", "quantidade": {"$sum": 1}}}
    ]
    resultado = await db.filme.aggregate(pipeline).to_list(length=None)
    return resultado

@router.get("/filmes/ordenados")
async def filmes_ordenados(ordem: Literal["asc", "desc"] = "asc"):
    """
    Retorna todos os filmes cadastrados ordenados por ano de lançamento.
    Pode ser ordenado de forma crescente ou decrescente.
    """
    if ordem == "asc":
        filmes = await engine.find(Filme, sort=Filme.anoLancamento.asc())
    else:
        filmes = await engine.find(Filme, sort=Filme.anoLancamento.desc())
    return filmes


@router.get("/{filme_id}/avaliacoes")
async def listar_avaliacoes_filme(filme_id: str, engine: AIOEngine = Depends(get_engine)):
    """
    Retorna todas as avaliações de um filme específico, pelo ID do filme.
    """
    # Verificar se o filme existe
    filme = await engine.find_one(Filme, Filme.id == ObjectId(filme_id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    # Buscar todas as avaliações associadas ao filme pelo filme_id
    avaliacoes = await engine.find(Avaliacao, Avaliacao.filme == filme.id)

    if not avaliacoes:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma avaliação encontrada para este filme"
        )
    
    return avaliacoes