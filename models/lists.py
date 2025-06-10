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
    
    @classmethod
    def registrar_marca(cls, nombre):
        dato=cls(nombre=nombre)
        try:
            db = SessionLocal()
            db.add(dato)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
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
    
    @classmethod
    def registrar_tipo(cls, nombre):
        dato=cls(nombre=nombre)
        try:
            db = SessionLocal()
            db.add(dato)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
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

    @classmethod
    def registrar_capacidad(cls, nombre):
        dato=cls(nombre=nombre)
        try:
            db = SessionLocal()
            db.add(dato)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()

class CatGasto(Base):
    __tablename__ = 'catgasto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    gastos = relationship('Gastos', back_populates='catgasto')

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            categorias = (
                db.query(cls).all()
            )
            return categorias
        finally:
            db.close()
    
    @classmethod
    def registrar_categoria(cls, nombre):
        dato=cls(nombre=nombre)
        try:
            db = SessionLocal()
            db.add(dato)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()