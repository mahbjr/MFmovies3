from fastapi import APIRouter, HTTPException
from database import get_engine
from modelos import Usuario
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
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=Usuario)
async def create_user(user: Usuario) -> Usuario:
    """
    Cria um novo usuário.
    """
    # Verifica se já existe um usuário com o mesmo e-mail
    existing_user = await engine.find_one(Usuario, Usuario.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    await engine.save(user)
    return user

@router.put("/{user_id}", response_model=Usuario)
async def update_user(user_id: str, user_data: Usuario) -> Usuario:
    """
    Atualiza os dados de um usuário existente.
    """
    user = await engine.find_one(Usuario, Usuario.id == ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Atualiza os campos desejados (supondo que o modelo possua 'name' e 'email')
    user.name = user_data.name
    user.email = user_data.email
    await engine.save(user)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: str) -> dict:
    """
    Deleta um usuário pelo ID.
    """
    user = await engine.find_one(Usuario, Usuario.id == ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await engine.delete(user)
    return {"message": "User deleted"}
