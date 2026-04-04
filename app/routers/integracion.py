from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.IntegracionOut)
def crear_integracion(payload: schemas.IntegracionCreate, db: Session = Depends(get_db)):
    contenido = payload.contenido.copy()

    payload_data = contenido.get("payload", {})

    payload_data["equipo"] = {
        "id": 1,
        "nombre": "nacional",
        "ciudad": "medellin",
        "entrenador": "autuori"
    }

    payload_data["jugador"] = {
        "id": 1,
        "equipo_id": 1,
        "nombre": "juan perez",
        "posicion": "delantero",
        "numero": 9
    }

    payload_data["partido"] = {
        "id": 1,
        "equipo_local_id": 1,
        "equipo_visitante_id": 2,
        "goles_local": None,
        "goles_visitante": None,
        "estado": "programado"
    }

    contenido["payload"] = payload_data

    integracion = models.Integracion(contenido=contenido)
    db.add(integracion)
    db.commit()
    db.refresh(integracion)
    return integracion


@router.get("/", response_model=list[schemas.IntegracionOut])
def listar_integraciones(db: Session = Depends(get_db)):
    return db.query(models.Integracion).all()


@router.get("/{integracion_id}", response_model=schemas.IntegracionOut)
def obtener_integracion(integracion_id: int, db: Session = Depends(get_db)):
    integracion = db.query(models.Integracion).filter(models.Integracion.id == integracion_id).first()
    if not integracion:
        raise HTTPException(status_code=404, detail="integracion no encontrada")
    return integracion


@router.put("/{integracion_id}", response_model=schemas.IntegracionOut)
def actualizar_integracion(integracion_id: int, payload: schemas.IntegracionCreate, db: Session = Depends(get_db)):
    integracion = db.query(models.Integracion).filter(models.Integracion.id == integracion_id).first()
    if not integracion:
        raise HTTPException(status_code=404, detail="integracion no encontrada")

    integracion.contenido = payload.contenido
    db.commit()
    db.refresh(integracion)
    return integracion


@router.patch("/{integracion_id}", response_model=schemas.IntegracionOut)
def actualizar_parcial_integracion(integracion_id: int, payload: schemas.IntegracionPatch, db: Session = Depends(get_db)):
    integracion = db.query(models.Integracion).filter(models.Integracion.id == integracion_id).first()
    if not integracion:
        raise HTTPException(status_code=404, detail="integracion no encontrada")

    datos = payload.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(integracion, campo, valor)

    db.commit()
    db.refresh(integracion)
    return integracion