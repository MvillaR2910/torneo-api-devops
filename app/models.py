from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Equipo(Base):
    __tablename__ = "equipo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=True)
    entrenador = Column(String, nullable=True)

    jugadores = relationship("Jugador", back_populates="equipo")


class Jugador(Base):
    __tablename__ = "jugador"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipo.id"), nullable=False)
    nombre = Column(String, nullable=False)
    posicion = Column(String, nullable=True)
    numero = Column(Integer, nullable=True)

    equipo = relationship("Equipo", back_populates="jugadores")


class Partido(Base):
    __tablename__ = "partido"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)

    equipo_local_id = Column(Integer, ForeignKey("equipo.id"), nullable=False)
    equipo_visitante_id = Column(Integer, ForeignKey("equipo.id"), nullable=False)

    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)
    estado = Column(String, nullable=False)