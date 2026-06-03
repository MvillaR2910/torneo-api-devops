from datetime import datetime

from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.get("/", response_model=schemas.HealthCheckOut)
def health_check():
    return {
        "api": "torneo-api",
        "status": "stable",
        "version": "2.1.2",
        "fecha_despliegue": datetime.now().isoformat()
    }
