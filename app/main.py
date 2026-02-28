from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import equipo, jugador, partido

app = FastAPI(title="torneo api")
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "api torneo funcionando"}

app.include_router(equipo.router, prefix="/equipos", tags=["equipos"])
app.include_router(jugador.router, prefix="/jugadores", tags=["jugadores"])
app.include_router(partido.router, prefix="/partidos", tags=["partidos"])