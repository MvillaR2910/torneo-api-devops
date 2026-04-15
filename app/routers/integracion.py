import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.IntegracionOut)
def crear_integracion(payload: schemas.IntegracionCreate, db: Session = Depends(get_db)):
    contenido = {
        "meta": {
            "antes": payload.meta.origen,
            "origen": "aws-futbol-api",
            "siguiente": None
        },
        "payload": {
            "geografia": payload.payload.geografia if payload.payload.geografia else {},
            "soporte": payload.payload.soporte if payload.payload.soporte else {},
            "futbol": {
                "equipo": {
                    "id": 1,
                    "nombre": "nacional",
                    "ciudad": "medellin",
                    "entrenador": "autuori"
                },
                "jugador": {
                    "id": 1,
                    "equipo_id": 1,
                    "nombre": "juan perez",
                    "posicion": "delantero",
                    "numero": 9
                },
                "partido": {
                    "id": 1,
                    "equipo_local_id": 1,
                    "equipo_visitante_id": 2,
                    "goles_local": None,
                    "goles_visitante": None,
                    "estado": "programado"
                }
            }
        }
    }

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

    integracion.contenido = {
        "meta": {
            "antes": payload.meta.origen,
            "origen": "aws-futbol-api",
            "siguiente": None
        },
        "payload": {
            "geografia": payload.payload.geografia if payload.payload.geografia else {},
            "soporte": payload.payload.soporte if payload.payload.soporte else {},
            "futbol": {
                "equipo": {
                    "id": 1,
                    "nombre": "nacional",
                    "ciudad": "medellin",
                    "entrenador": "autuori"
                },
                "jugador": {
                    "id": 1,
                    "equipo_id": 1,
                    "nombre": "juan perez",
                    "posicion": "delantero",
                    "numero": 9
                },
                "partido": {
                    "id": 1,
                    "equipo_local_id": 1,
                    "equipo_visitante_id": 2,
                    "goles_local": None,
                    "goles_visitante": None,
                    "estado": "programado"
                }
            }
        }
    }

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

@router.post("/forward")
def reenviar_a_otra_api(payload: schemas.ForwardRequest):
    try:
        response = requests.post(
            payload.url_destino,
            json=payload.body,
            headers=payload.headers if payload.headers else {},
            timeout=10
        )

        try:
            respuesta_json = response.json()
        except ValueError:
            respuesta_json = {"respuesta_texto": response.text}

        return {
            "mensaje": "json reenviado correctamente",
            "status_code_destino": response.status_code,
            "url_destino": payload.url_destino,
            "respuesta_destino": respuesta_json
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"error reenviando a la api destino: {str(e)}")