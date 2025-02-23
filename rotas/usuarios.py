from fastapi import APIRouter, HTTPException
from database import get_engine, db
from modelos import Usuario, Filme, ListaFavoritos
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
async def update_user(user_id: str, user_data: dict) -> Usuario:
    user = await engine.find_one(Usuario, Usuario.id == ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
        raise HTTPException(status_code=404, detail="User not found")
    await engine.delete(user)
    return {"message": "User deleted"}

@router.get("/usuarios/{user_id}/favoritos/filmes", response_model=list[Filme])
async def get_filmes_favoritos(user_id: str) -> list[Filme]:
    # Aqui filtramos usando o campo "usuario", acessando o id do objeto de usuário
    lista = await engine.find_one(ListaFavoritos, ListaFavoritos.usuario.id == ObjectId(user_id))
    if not lista:
        raise HTTPException(status_code=404, detail="Lista de favoritos não encontrada")
    # Retornamos diretamente a lista de filmes, que já são objetos Filme
    return lista.filmes