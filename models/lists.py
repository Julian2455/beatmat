from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from db import Base, engine, SessionLocal

class Marca(Base):
    __tablename__ = 'marca'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    extintores = relationship('Extintor', back_populates='marca')

class Tipo(Base):
    __tablename__ = 'tipo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False, unique=True)
    extintores = relationship('Extintor', back_populates='tipo')

class Capacidad(Base):
    __tablename__ = 'capacidad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(String(30), nullable=False, unique=True)
    extintores = relationship('Extintor', back_populates='capacidad')