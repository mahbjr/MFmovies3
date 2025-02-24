from fastapi import APIRouter, HTTPException
from database import get_engine
from modelos import Avaliacao, Usuario
from odmantic import ObjectId

router = APIRouter(
    prefix="/usuarios",  # Prefixo para todas as rotas
    tags=["Usuários"],   # Tag para documentação automática
)

engine = get_engine()

@router.get("/", response_model=list[Usuario])
async def get_all_users() -> list[Usuario]:
    """
    Retorna todos os usuários cadastrados.
    """
    users = await engine.find(Usuario)
    return users

@router.get("/{user_id}", response_model=Usuario)
async def get_user(user_id: str) -> Usuario:
    """
    Retorna um usuário pelo ID.
    """
    user = await engine.find_one(Usuario, Usuario.id == ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return user

@router.post("/", response_model=Usuario)
async def create_user(user: Usuario) -> Usuario:
    """
    Cria um novo usuário.
    """
    # Verifica se já existe um usuário com o mesmo e-mail
    existing_user = await engine.find_one(Usuario, Usuario.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    await engine.save(user)
    return user

@router.put("/{user_id}", response_model=Usuario)
async def update_user(user_id: str, user_data: dict) -> Usuario:
    user = await engine.find_one(Usuario, Usuario.id == ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for key, value in user_data.items():
        setattr(user, key, value)
    await engine.save(user)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: str) -> dict:
    """
    Deleta um usuário pelo ID.
    """
    user = await engine.find_one(Usuario, Usuario.id == ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await engine.delete(user)
    return {"message": "Usuário deletado"}  

@router.get("/avaliacoes/filmes-usuarios")
async def avaliacoes_avancadas(limite: int, skip: int = 0, limit: int = 10):
    """
    Retorna avaliações com nota acima do limite especificado.
    """
    collection = engine.get_collection(Avaliacao)

    pipeline = [
        {"$match": {"nota": {"$gt": limite}}},
        {"$lookup": {
            "from": "filme",
            "localField": "filme",
            "foreignField": "_id",
            "as": "filme_info"
        }},
        {"$lookup": {
            "from": "usuario",
            "localField": "usuario",
            "foreignField": "_id",
            "as": "usuario_info"
        }},
        {"$unwind": {
            "path": "$filme_info",
            "preserveNullAndEmptyArrays": True
        }},
        {"$unwind": {
            "path": "$usuario_info",
            "preserveNullAndEmptyArrays": True
        }},
        {"$project": {
            "_id": 0,
            "nota": 1,
            "comentario": 1,
            "filme": {
                "titulo": "$filme_info.titulo",
                "diretor": "$filme_info.diretor",
                "anoLancamento": "$filme_info.anoLancamento",
                "genero": "$filme_info.genero"
            },
            "usuario": {
                "nome": "$usuario_info.nome",
                "email": "$usuario_info.email"
            }
        }},
        {"$skip": skip},
        {"$limit": limit}
    ]
    
    resultado = await collection.aggregate(pipeline).to_list(length=None)
    
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma avaliação encontrada com nota maior que {limite}"
        )
    
    return resultado