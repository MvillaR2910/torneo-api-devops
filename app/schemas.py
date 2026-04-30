from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

model_config = ConfigDict(from_attributes=True)

class EquipoCreate(BaseModel):
    nombre: str
    ciudad: Optional[str] = None
    entrenador: Optional[str] = None


class EquipoOut(BaseModel):
    id: int
    nombre: str
    ciudad: Optional[str] = None
    entrenador: Optional[str] = None

class JugadorCreate(BaseModel):
    nombre: str
    posicion: str | None = None
    numero: int | None = None
    equipo_id: int


class JugadorOut(BaseModel):
    id: int
    nombre: str
    posicion: str | None = None
    numero: int | None = None
    equipo_id: int

class PartidoCreate(BaseModel):
    fecha: datetime
    equipo_local_id: int
    equipo_visitante_id: int
    goles_local: int | None = None
    goles_visitante: int | None = None
    estado: str

class PartidoOut(BaseModel):
    id: int
    fecha: datetime
    equipo_local_id: int
    equipo_visitante_id: int
    goles_local: int | None = None
    goles_visitante: int | None = None
    estado: str

class EquipoPatch(BaseModel):
    nombre: str | None = None
    ciudad: str | None = None
    entrenador: str | None = None


class JugadorPatch(BaseModel):
    equipo_id: int | None = None
    nombre: str | None = None
    posicion: str | None = None
    numero: int | None = None


class PartidoPatch(BaseModel):
    fecha: datetime | None = None
    equipo_local_id: int | None = None
    equipo_visitante_id: int | None = None
    goles_local: int | None = None
    goles_visitante: int | None = None
    estado: str | None = None

class IntegracionMeta(BaseModel):
    antes: str | None = None
    origen: str
    siguiente: str | None = None

class IntegracionPayload(BaseModel):
    geografia: dict[str, Any] | None = None
    soporte: dict[str, Any] | None = None
    futbol: dict[str, Any] | None = None

class IntegracionCreate(BaseModel):
    meta: IntegracionMeta
    payload: IntegracionPayload

class IntegracionOut(BaseModel):
    id: int
    contenido: dict

    model_config = ConfigDict(from_attributes=True)

class IntegracionPatch(BaseModel):
    contenido: dict | None = None

class ForwardRequest(BaseModel):
    url_destino: str
    body: dict
    headers: dict | None = None


class ForwardPatchByIdRequest(BaseModel):
    url_destino: str
    id_destino: int
    body: dict
    headers: dict[str, str] | None = None


class FutbolEquipoInput(BaseModel):
    id: int
    nombre: str
    ciudad: str | None = None
    entrenador: str | None = None


class FutbolJugadorInput(BaseModel):
    id: int
    equipo_id: int
    nombre: str
    posicion: str | None = None
    numero: int | None = None


class FutbolPartidoInput(BaseModel):
    id: int
    equipo_local_id: int
    equipo_visitante_id: int
    goles_local: int | None = None
    goles_visitante: int | None = None
    estado: str


class IntegracionRecibidaRequest(BaseModel):
    meta: dict[str, Any] | None = None
    trace_id: str
    payload: dict[str, Any]


class IntegracionCompletarRequest(BaseModel):
    integracion_id: int | None = None
    trace_id: str | None = None
    equipo: FutbolEquipoInput
    jugador: FutbolJugadorInput
    partido: FutbolPartidoInput


class ActualizarDestinoRequest(BaseModel):
    integracion_id: int | None = None
    trace_id: str | None = None
    url_destino: str
    headers: dict[str, str] | None = None
