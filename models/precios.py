from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .lists import Capacidad

class Precios(Base):
    __tablename__ = 'precios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(100), nullable=False)
    valor = Column(Float, nullable=False)
    
    capacidad_id = Column(Integer, ForeignKey('capacidad.id'), nullable=True)
    capacidad = relationship('Capacidad', back_populates='precios')