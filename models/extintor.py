from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from db import Base, engine, SessionLocal
from .cliente import Cliente
from .lists import *
from .recarga import Recarga

class Extintor(Base):
    __tablename__='extintor'

    id=Column(Integer,primary_key=True,autoincrement=True)
    numeracion=Column(Integer,nullable=False,unique=True)
    marca_id=Column(Integer, ForeignKey('marca.id'), nullable=False)
    ubicacion=Column(String(70),nullable=False)
    tipo_id=Column(Integer, ForeignKey('tipo.id'), nullable=False)
    capacidad_id=Column(Integer, ForeignKey('capacidad.id'), nullable=False)

    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('Cliente',back_populates='extintor')
    marca=relationship('Marca', back_populates='extintores')
    tipo=relationship('Tipo', back_populates='extintores')
    capacidad=relationship('Capacidad', back_populates='extintores')
    recarga=relationship('Recarga',back_populates='extintor')
    detcaja=relationship('DetCaja',back_populates='extintor')
    tareas=relationship('Tareas',back_populates='extintor')

    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.nombre.label('capacidad_nombre')
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def show_all_client(cls, client_id):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.nombre.label('capacidad_nombre')
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.cliente_id == client_id)
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
        datos=cls(numeracion=numeracion,marca_id=marca,ubicacion=ubicacion,tipo_id=tipo,capacidad_id=capacidad)
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
                extintor.marca_id = marca
                extintor.ubicacion = ubicacion
                extintor.tipo_id = tipo
                extintor.capacidad_id = capacidad
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
            extintor = (db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.id.label('marca_id'),
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.id.label('tipo_id'),
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.id.label('capacidad_id'),
                Capacidad.nombre.label('capacidad_nombre')
            )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.id == id_extintor).first())
            return extintor
        except Exception as e:
            print(f"Error al obtener id: {e}")
            return None
        
    @classmethod
    def extintor_asociado_cliente(cls, id_cliente):
        try:
            db = SessionLocal()
            resultado = (
                db.query(Extintor, Recarga)
                .join(Recarga, Recarga.extintor_id == Extintor.id)
                .filter(Extintor.cliente_id == id_cliente)
                .all()
            )   
            return resultado
        except Exception as e:
            print(f"Error en consulta: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def buscar(cls, numeracion, marca_filter, tipo_filter, capacidad_filter, page=1, per_page=10):
        try:
            db = SessionLocal()
            query = (
                db.query(
                    Extintor.id,
                    Extintor.numeracion,
                    Marca.nombre.label('marca_nombre'),
                    Extintor.ubicacion,
                    Tipo.nombre.label('tipo_nombre'),
                    Capacidad.nombre.label('capacidad_nombre')
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
            )
            if numeracion:
                query = query.filter(Extintor.numeracion.like(f"{numeracion}%"))
            if marca_filter:
                query = query.filter(Extintor.marca_id == marca_filter)
            if tipo_filter:
                query = query.filter(Extintor.tipo_id == tipo_filter)
            if capacidad_filter:
                query = query.filter(Extintor.capacidad_id == capacidad_filter)
            extintores = (
                query
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return extintores
        except Exception as e:
            print(f"Error al buscar: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def contar_buscar(cls, numeracion, marca_filter, tipo_filter, capacidad_filter):
        try:
            db = SessionLocal()
            query = db.query(cls)
            if numeracion:
                query = query.filter(cls.numeracion.like(f"{numeracion}%"))
            if marca_filter:
                query = query.filter(cls.marca_id == marca_filter)
            if tipo_filter:
                query = query.filter(cls.tipo_id == tipo_filter)
            if capacidad_filter:
                query = query.filter(cls.capacidad_id == capacidad_filter)
            total = query.count()
            return total
        except Exception as e:
            print(f"Error al contar resultados: {e}")
            return 0
        finally:
            db.close()
    
    @classmethod
    def disponibles(cls):
        try:
            db = SessionLocal()
            extintor = (db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.id.label('marca_id'),
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.id.label('tipo_id'),
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.id.label('capacidad_id'),
                Capacidad.nombre.label('capacidad_nombre')
            )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(Extintor.cliente_id.is_(None))
                .all()
            )
            return extintor
        except Exception as e:
            print(f"Error al obtener id: {e}")
            return None