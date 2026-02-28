from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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

    class Config:
        from_attributes = True