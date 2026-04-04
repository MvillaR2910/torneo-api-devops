from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.JugadorOut)
def crear_jugador(payload: schemas.JugadorCreate, db: Session = Depends(get_db)):
    jugador = models.Jugador(**payload.model_dump())
    db.add(jugador)
    db.commit()
    db.refresh(jugador)
    return jugador


@router.get("/", response_model=list[schemas.JugadorOut])
def listar_jugadores(db: Session = Depends(get_db)):
    return db.query(models.Jugador).all()


@router.get("/{jugador_id}", response_model=schemas.JugadorOut)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="jugador no encontrado")
    return jugador


@router.put("/{jugador_id}", response_model=schemas.JugadorOut)
def actualizar_jugador(jugador_id: int, payload: schemas.JugadorCreate, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="jugador no encontrado")

    jugador.nombre = payload.nombre
    jugador.posicion = payload.posicion
    jugador.numero = payload.numero
    jugador.equipo_id = payload.equipo_id

    db.commit()
    db.refresh(jugador)
    return jugador


@router.delete("/{jugador_id}")
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="jugador no encontrado")

    db.delete(jugador)
    db.commit()
    return {"message": "jugador eliminado"}

@router.patch("/{jugador_id}", response_model=schemas.JugadorOut)
def actualizar_parcial_jugador(jugador_id: int, payload: schemas.JugadorPatch, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="jugador no encontrado")

    datos = payload.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(jugador, campo, valor)

    db.commit()
    db.refresh(jugador)
    return jugador