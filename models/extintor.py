from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal

class Extintor(Base):
    __tablename__='extintor'

    id=Column(Integer,primary_key=True,autoincrement=True)
    numeracion=Column(Integer,nullable=False)
    marca=Column(String(50),nullable=False)
    ubicacion=Column(String(70),nullable=False)
    tipo=Column(String(20),nullable=False)
    capacidad=Column(String(30),nullable=False)

    recarga=relationship('recarga',back_populates='extintor')
    detcaja=relationship('detcaja',back_populates='extintor')
    tareas=relationship('tareas',back_populates='extintor')