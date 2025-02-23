from fastapi import APIRouter, HTTPException
from database import get_engine
from modelos import Avaliacao, Filme, Usuario
from odmantic import ObjectId

router = APIRouter(
    prefix="/avaliacoes",  # Prefixo para todas as rotas
    tags=["Avaliacoes"],   # Tag para documentação automática
)

engine = get_engine()

@router.get("/", response_model=list[Avaliacao])
async def get_all_avaliacoes() -> list[Avaliacao]:
    """
    Retorna todas as avaliações cadastradas.
    """
    avaliacoes = await engine.find(Avaliacao)
    return avaliacoes

@router.get("/{avaliacao_id}", response_model=Avaliacao)
async def get_avaliacao(avaliacao_id: str) -> Avaliacao:
    """
    Retorna uma avaliação pelo ID.
    """
    avaliacao = await engine.find_one(Avaliacao, Avaliacao.id == ObjectId(avaliacao_id))
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")
    return avaliacao

@router.post("/", response_model=Avaliacao)
async def create_avaliacao(avaliacao: Avaliacao) -> Avaliacao:
    """
    Cria uma nova avaliação.
    
    É necessário que a avaliação contenha referências válidas para um usuário e para um filme.
    """
    # Verifica se os campos de relacionamento foram informados
    if not avaliacao.usuario:
        raise HTTPException(status_code=400, detail="Usuario is required")
    if not avaliacao.filme:
        raise HTTPException(status_code=400, detail="Filme is required")
    
    # Verifica se o usuário associado existe
    usuario = await engine.find_one(Usuario, Usuario.id == ObjectId(avaliacao.usuario.id))
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    
    # Verifica se o filme associado existe
    filme = await engine.find_one(Filme, Filme.id == ObjectId(avaliacao.filme.id))
    if not filme:
        raise HTTPException(status_code=404, detail="Filme not found")
    
    avaliacao.usuario = usuario
    avaliacao.filme = filme
    await engine.save(avaliacao)
    return avaliacao

@router.put("/{avaliacao_id}", response_model=Avaliacao)
async def update_avaliacao(avaliacao_id: str, avaliacao_data: dict) -> Avaliacao:
    """
    Atualiza uma avaliação pelo ID.
    """
    avaliacao = await engine.find_one(Avaliacao, Avaliacao.id == ObjectId(avaliacao_id))
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")
    for key, value in avaliacao_data.items():
        setattr(avaliacao, key, value)
    await engine.save(avaliacao)
    return avaliacao

@router.delete("/{avaliacao_id}")
async def delete_avaliacao(avaliacao_id: str) -> dict:
    """
    Deleta uma avaliação pelo ID.
    """
    avaliacao = await engine.find_one(Avaliacao, Avaliacao.id == ObjectId(avaliacao_id))
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")
    await engine.delete(avaliacao)
    return {"message": "Avaliacao deleted"}
