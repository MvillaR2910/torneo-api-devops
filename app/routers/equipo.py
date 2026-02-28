from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.EquipoOut)
def crear_equipo(payload: schemas.EquipoCreate, db: Session = Depends(get_db)):
    equipo = models.Equipo(
        nombre=payload.nombre,
        ciudad=payload.ciudad,
        entrenador=payload.entrenador,
    )
    db.add(equipo)
    db.commit()
    db.refresh(equipo)
    return equipo


@router.get("/", response_model=list[schemas.EquipoOut])
def listar_equipos(db: Session = Depends(get_db)):
    equipos = db.query(models.Equipo).all()
    return equipos