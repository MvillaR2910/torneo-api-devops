from datetime import datetime

from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.get("/", response_model=schemas.HealthCheckOut)
def health_check():
    return {
        "api": "torneo-api",
        "status": "canary",
        "version": "2.2.0",
        "fecha_despliegue": datetime.now().isoformat(),
        "deploy_date": "2026-06-03",
        "features_preview": [
            "stats-por-equipo-v2",
            "filtro-partidos-por-estado",
        ],
        "modified_by": "Sebastian Ruiz",
    }
