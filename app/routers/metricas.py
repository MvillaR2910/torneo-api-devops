from fastapi import APIRouter
from app.database import SessionLocal
from app import models
from app.metrics_store import obtener_metricas

router = APIRouter()

@router.get("/metricas")
def metricas():
    db = SessionLocal()
    try:
        total_integraciones = db.query(models.Integracion).count()
        total_equipos = db.query(models.Equipo).count()
        total_jugadores = db.query(models.Jugador).count()
        total_partidos = db.query(models.Partido).count()

        return {
            "api": "aws-futbol-api",
            "status": "ok",
            "metrics": {
                "integraciones_total": total_integraciones,
                "equipos_total": total_equipos,
                "jugadores_total": total_jugadores,
                "partidos_total": total_partidos
            },
            "data": obtener_metricas()
        }
    finally:
        db.close()