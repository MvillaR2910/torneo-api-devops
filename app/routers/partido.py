from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.PartidoOut)
def crear_partido(payload: schemas.PartidoCreate, db: Session = Depends(get_db)):
    if payload.equipo_local_id == payload.equipo_visitante_id:
        raise HTTPException(status_code=400, detail="equipo_local_id y equipo_visitante_id no pueden ser iguales")

    partido = models.Partido(**payload.model_dump())
    db.add(partido)
    db.commit()
    db.refresh(partido)
    return partido


@router.get("/", response_model=list[schemas.PartidoOut])
def listar_partidos(db: Session = Depends(get_db)):
    return db.query(models.Partido).all()


@router.get("/{partido_id}", response_model=schemas.PartidoOut)
def obtener_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="partido no encontrado")
    return partido


@router.put("/{partido_id}", response_model=schemas.PartidoOut)
def actualizar_partido(partido_id: int, payload: schemas.PartidoCreate, db: Session = Depends(get_db)):
    if payload.equipo_local_id == payload.equipo_visitante_id:
        raise HTTPException(status_code=400, detail="equipo_local_id y equipo_visitante_id no pueden ser iguales")

    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="partido no encontrado")

    partido.fecha = payload.fecha
    partido.equipo_local_id = payload.equipo_local_id
    partido.equipo_visitante_id = payload.equipo_visitante_id
    partido.goles_local = payload.goles_local
    partido.goles_visitante = payload.goles_visitante
    partido.estado = payload.estado

    db.commit()
    db.refresh(partido)
    return partido


@router.delete("/{partido_id}")
def eliminar_partido(partido_id: int, db: Session = Depends(get_db)):
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="partido no encontrado")

    db.delete(partido)
    db.commit()
    return {"message": "partido eliminado"}

@router.patch("/{partido_id}", response_model=schemas.PartidoOut)
def actualizar_parcial_partido(partido_id: int, payload: schemas.PartidoPatch, db: Session = Depends(get_db)):
    partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="partido no encontrado")

    datos = payload.model_dump(exclude_unset=True)

    equipo_local_id = datos.get("equipo_local_id", partido.equipo_local_id)
    equipo_visitante_id = datos.get("equipo_visitante_id", partido.equipo_visitante_id)

    if equipo_local_id == equipo_visitante_id:
        raise HTTPException(status_code=400, detail="equipo_local_id y equipo_visitante_id no pueden ser iguales")

    for campo, valor in datos.items():
        setattr(partido, campo, valor)

    db.commit()
    db.refresh(partido)
    return partido