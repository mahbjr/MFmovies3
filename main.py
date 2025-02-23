from fastapi import FastAPI
from rotas import avaliacoes, filmes, home, listaFavoritos, usuarios

# FastAPI app instance
app = FastAPI()

# Rotas para Endpoints
app.include_router(home.router)
app.include_router(filmes.router)
app.include_router(usuarios.router)
app.include_router(avaliacoes.router)
app.include_router(listaFavoritos.router)