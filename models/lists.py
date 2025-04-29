from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from db import Base, engine, SessionLocal

class Marca(Base):
    __tablename__ = 'marca'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    extintores = relationship('Extintor', back_populates='marca')
    precios = relationship('Precios', back_populates='marca')

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            clientes = (
                db.query(cls).all()
            )
            return clientes
        finally:
            db.close()

class Tipo(Base):
    __tablename__ = 'tipo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False, unique=True)
    extintores = relationship('Extintor', back_populates='tipo')
    precios = relationship('Precios', back_populates='tipo')

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            clientes = (
                db.query(cls).all()
            )
            return clientes
        finally:
            db.close()

class Capacidad(Base):
    __tablename__ = 'capacidad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False, unique=True)
    extintores = relationship('Extintor', back_populates='capacidad')
    precios = relationship('Precios', back_populates='capacidad')

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            clientes = (
                db.query(cls).all()
            )
            return clientes
        finally:
            db.close()