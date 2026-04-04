from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import equipo, jugador, partido, integracion

app = FastAPI(title="torneo api v2")
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "api torneo v2 funcionando"}

app.include_router(equipo.router, prefix="/api/v2/equipos", tags=["equipos v2"])
app.include_router(jugador.router, prefix="/api/v2/jugadores", tags=["jugadores v2"])
app.include_router(partido.router, prefix="/api/v2/partidos", tags=["partidos v2"])
app.include_router(integracion.router, prefix="/api/v2/integracion", tags=["integracion v2"])