from copy import deepcopy

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.metrics_store import registrar_evento
from app.database import get_db
from app import models, schemas

router = APIRouter()


def _buscar_integracion_base(
    db: Session,
    integracion_id: int | None = None,
    trace_id: str | None = None,
):
    if integracion_id is not None:
        integracion = db.query(models.Integracion).filter(models.Integracion.id == integracion_id).first()
    elif trace_id is not None:
        integracion = (
            db.query(models.Integracion)
            .filter(models.Integracion.contenido["trace_id"].as_string() == trace_id)
            .order_by(models.Integracion.id.desc())
            .first()
        )
    else:
        integracion = db.query(models.Integracion).order_by(models.Integracion.id.desc()).first()

    if not integracion:
        raise HTTPException(status_code=404, detail="integracion base no encontrada")

    return integracion


@router.post("/", response_model=schemas.IntegracionOut)
def crear_integracion(payload: schemas.IntegracionCreate, db: Session = Depends(get_db)):
    registrar_evento("CreaciÃ³n De Integracion")
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
    registrar_evento("Listar Integraciones")
    integraciones = db.query(models.Integracion).all()
    return [
        integracion
        for integracion in integraciones
        if (integracion.contenido or {}).get("payload", {}).get("futbol")
    ]


@router.get("/{integracion_id}", response_model=schemas.IntegracionOut)
def obtener_integracion(integracion_id: int, db: Session = Depends(get_db)):
    registrar_evento("Mostrar IntegraciÃ³n Por Id")
    integracion = db.query(models.Integracion).filter(models.Integracion.id == integracion_id).first()
    if not integracion:
        raise HTTPException(status_code=404, detail="integracion no encontrada")
    return integracion


@router.put("/{integracion_id}", response_model=schemas.IntegracionOut)
def actualizar_integracion(integracion_id: int, payload: schemas.IntegracionCreate, db: Session = Depends(get_db)):
    registrar_evento("Actualizar InformaciÃ³n De Integracion")
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
    registrar_evento("ActualizaciÃ³n Parcial De IntegraciÃ³n")
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
    registrar_evento("Envio De Data A Otra Api")
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


@router.patch("/forward/{id_destino}")
def actualizar_en_otra_api_por_id(id_destino: int, payload: schemas.ForwardPatchByIdRequest):
    registrar_evento("Actualizacion Remota Por Id")

    base_url = payload.url_destino.rstrip("/")
    url_final = f"{base_url}/{id_destino}"

    try:
        response = requests.patch(
            url_final,
            json=payload.body,
            headers=payload.headers if payload.headers else {},
            timeout=10
        )

        try:
            respuesta_json = response.json()
        except ValueError:
            respuesta_json = {"respuesta_texto": response.text}

        return {
            "mensaje": "json actualizado correctamente en la api destino",
            "status_code_destino": response.status_code,
            "url_destino": url_final,
            "respuesta_destino": respuesta_json
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"error actualizando la api destino: {str(e)}")


@router.post("/recibir", response_model=schemas.IntegracionOut)
def recibir_integracion(payload: schemas.IntegracionRecibidaRequest, db: Session = Depends(get_db)):
    registrar_evento("Recepcion De Integracion Externa")

    contenido = {
        "meta": payload.meta if payload.meta else {},
        "trace_id": payload.trace_id,
        "payload": payload.payload
    }

    integracion = models.Integracion(contenido=contenido)
    db.add(integracion)
    db.commit()
    db.refresh(integracion)
    return integracion


@router.post("/completar", response_model=schemas.IntegracionOut)
def completar_integracion(payload: schemas.IntegracionCompletarRequest, db: Session = Depends(get_db)):
    registrar_evento("Completar Integracion Con Futbol")

    integracion = _buscar_integracion_base(
        db=db,
        integracion_id=payload.integracion_id,
        trace_id=payload.trace_id,
    )

    contenido_actual = deepcopy(integracion.contenido or {})
    payload_actual = deepcopy(contenido_actual.get("payload", {}))

    payload_actual["futbol"] = {
        "equipo": payload.equipo.model_dump(),
        "jugador": payload.jugador.model_dump(),
        "partido": payload.partido.model_dump(),
    }

    integracion.contenido = {
        "meta": contenido_actual.get("meta", {}),
        "trace_id": contenido_actual.get("trace_id"),
        "payload": payload_actual,
    }

    db.commit()
    db.refresh(integracion)
    return integracion


@router.patch("/actualizar-destino")
def actualizar_integracion_en_destino(payload: schemas.ActualizarDestinoRequest, db: Session = Depends(get_db)):
    registrar_evento("Actualizar Integracion En Destino")

    integracion = _buscar_integracion_base(
        db=db,
        integracion_id=payload.integracion_id,
        trace_id=payload.trace_id,
    )

    body = deepcopy(integracion.contenido or {})

    if not body.get("payload", {}).get("futbol"):
        raise HTTPException(
            status_code=400,
            detail="la integracion seleccionada aun no tiene datos de futbol para actualizar en destino",
        )

    try:
        response = requests.patch(
            payload.url_destino,
            json=body,
            headers=payload.headers if payload.headers else {},
            timeout=15,
        )

        try:
            respuesta_destino = response.json()
        except ValueError:
            respuesta_destino = {"respuesta_texto": response.text}

        return {
            "mensaje": "integracion actualizada correctamente en la api destino",
            "url_destino": payload.url_destino,
            "body_enviado": body,
            "status_code_destino": response.status_code,
            "respuesta_destino": respuesta_destino,
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"error actualizando integracion en destino: {str(e)}")
