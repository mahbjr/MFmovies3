from fastapi import FastAPI
from rotas import filmes, home

# FastAPI app instance
app = FastAPI()

# Rotas para Endpoints
app.include_router(home.router)
app.include_router(filmes.router)