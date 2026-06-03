import os
from datetime import datetime

from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.get("/", response_model=schemas.HealthCheckOut)
def health_check():
    deploy_type = os.getenv("DEPLOY_TYPE", "stable")
    version = os.getenv("APP_VERSION", "2.1.2")

    data = {
        "api": "torneo-api",
        "status": deploy_type,
        "version": version,
        "fecha_despliegue": datetime.now().isoformat(),
        "modified_by": "Sebastian Ruiz",
    }

    if deploy_type == "canary":
        data["deploy_date"] = os.getenv("DEPLOY_DATE", datetime.now().date().isoformat())
        data["features_preview"] = [
            "stats-por-equipo-v2",
            "filtro-partidos-por-estado",
        ]

    return data
