from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal

class Extintor(Base):
    __tablename__='extintor'

    id=Column(Integer,primary_key=True,autoincrement=True)
    numeracion=Column(Integer,nullable=False)
    marca=Column(String,nullable=False)
    ubicacion=Column(String,nullable=False)
    tipo=Column(String,nullable=False)
    capacidad=Column(String,nullable=False)

    recarga=relationship('recarga',back_populates='extintor')