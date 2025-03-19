from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal

class Tareas(Base):
    __tablename__='tareas'

    id=Column(Integer,primary_key=True,autoincrement=True)
    tamizacion=Column(Integer,nullable=False)
    peso=Column(Integer,nullable=False)
    control_tacho=Column(Integer,nullable=False)
    relleno_polvo=Column(Integer,nullable=False)
    cambio_manometro=Column(Integer,nullable=False)
    oring=Column(Integer,nullable=False)
    gatillo=Column(Integer,nullable=False)
    pintura=Column(Integer,nullable=False)
    interior=Column(Integer,nullable=False)
    valvula=Column(Integer,nullable=False)
    bastago_bronce=Column(Integer,nullable=False)
    otro=Column(Integer,nullable=False)
    observacion=Column(String(255))

    extintor_id=Column(Integer, ForeignKey('extintor.id'))

    extintor=relationship('extintor',back_populates='tareas')