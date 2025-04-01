from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal

class Extintor(Base):
    __tablename__='extintor'

    id=Column(Integer,primary_key=True,autoincrement=True)
    numeracion=Column(Integer,nullable=False,unique=True)
    marca=Column(String(50),nullable=False)
    ubicacion=Column(String(70),nullable=False)
    tipo=Column(String(20),nullable=False)
    capacidad=Column(String(30),nullable=False)

    cliente=relationship('Cliente',back_populates='extintor')
    recarga=relationship('Recarga',back_populates='extintor')
    detcaja=relationship('DetCaja',back_populates='extintor')
    tareas=relationship('Tareas',back_populates='extintor')

    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            extintores = (
                db.query(cls)
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def contar_extintores(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total
    
    @classmethod
    def registrar(cls,numeracion,marca,ubicacion,tipo,capacidad):
        datos=cls(numeracion=numeracion,marca=marca,ubicacion=ubicacion,tipo=tipo,capacidad=capacidad)
        try:
            db = SessionLocal()
            db.add(datos)
            db.commit()
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def actualizar(cls, id_extintor, numeracion, marca, ubicacion, tipo, capacidad):
        try:
            db = SessionLocal()
            extintor = db.query(cls).filter_by(id=id_extintor).first()
            if extintor:
                extintor.numeracion = numeracion
                extintor.marca = marca
                extintor.ubicacion = ubicacion
                extintor.tipo = tipo
                extintor.capacidad = capacidad
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al actualizar extintor: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def get_by_id(cls, id_extintor):
        try:
            db = SessionLocal()
            extintor = db.query(cls).filter(cls.id == id_extintor).first()
            return extintor
        except Exception as e:
            print(f"Error al obtener id: {e}")
            return None