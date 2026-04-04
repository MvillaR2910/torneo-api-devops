from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/{equipo_id}", response_model=schemas.EquipoOut)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="equipo no encontrado")
    return equipo


@router.put("/{equipo_id}", response_model=schemas.EquipoOut)
def actualizar_equipo(equipo_id: int, payload: schemas.EquipoCreate, db: Session = Depends(get_db)):
    equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="equipo no encontrado")

    equipo.nombre = payload.nombre
    equipo.ciudad = payload.ciudad
    equipo.entrenador = payload.entrenador

    db.commit()
    db.refresh(equipo)
    return equipo


@router.delete("/{equipo_id}")
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="equipo no encontrado")

    db.delete(equipo)
    db.commit()
    return {"message": "equipo eliminado"}

@router.patch("/{equipo_id}", response_model=schemas.EquipoOut)
def actualizar_parcial_equipo(equipo_id: int, payload: schemas.EquipoPatch, db: Session = Depends(get_db)):
    equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="equipo no encontrado")

    datos = payload.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(equipo, campo, valor)

    db.commit()
    db.refresh(equipo)
    return equipo