from pydantic import BaseModel, ConfigDict
from typing import Optional
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

class IntegracionCreate(BaseModel):
    contenido: dict


class IntegracionOut(BaseModel):
    id: int
    contenido: dict

    model_config = ConfigDict(from_attributes=True)


class IntegracionPatch(BaseModel):
    contenido: dict | None = None