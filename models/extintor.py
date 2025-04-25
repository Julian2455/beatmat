from sqlalchemy import Column, Integer, String, ForeignKey, func, and_
from sqlalchemy.orm import relationship, joinedload
from db import Base, engine, SessionLocal
from .cliente import Cliente
from .lists import *
from .recarga import Recarga
from .tareas import Tareas
from .precios import Precios

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
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                    Extintor.id,
                    Extintor.numeracion,
                    Extintor.ubicacion,
                    Marca.nombre.label("marca"),
                    Tipo.nombre.label("tipo"),
                    Capacidad.nombre.label("capacidad"),
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(Extintor.cliente_id == id_cliente)
                .all()
            )
            resultado = []
            for ext in extintores:
                ext_id = ext.id
                ultima_recarga = (
                    db.query(Recarga)
                    .filter(Recarga.extintor_id == ext_id)
                    .order_by(Recarga.nuevo_control_recarga.desc())
                    .first()
                )
                ultima_tarea = (
                    db.query(Tareas)
                    .filter(Tareas.extintor_id == ext_id)
                    .order_by(Tareas.fecha.desc())
                    .first()
                )
                resultado.append({
                    "id": ext.id,
                    "numeracion": ext.numeracion,
                    "ubicacion": ext.ubicacion,
                    "marca": ext.marca,
                    "tipo": ext.tipo,
                    "capacidad": ext.capacidad,
                    "ultima_recarga": ultima_recarga,
                    "ultima_tarea": ultima_tarea
                })
            return resultado       
        except Exception as e:
            print(f"Error en consulta: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def buscar(cls, numeracion, marca_filter, tipo_filter, capacidad_filter, page=1, per_page=10, disponible=None):
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
            if disponible:
                query = query.filter(Extintor.cliente_id.is_(None))
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
    def contar_buscar(cls, numeracion, marca_filter, tipo_filter, capacidad_filter, disponible=None):
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
            if disponible:
                query = query.filter(Extintor.cliente_id.is_(None))
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
    
    @classmethod
    def asignar_cliente(cls, lista_extintores, id_cliente):
        db = SessionLocal()
        try:
            for id_extintor in lista_extintores:
                extintor = db.query(cls).filter_by(id=id_extintor).first()
                if extintor:
                    extintor.cliente_id = id_cliente
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db.close()
    
    @classmethod
    def liberar_extintor(cls, id_extintor):
        db = SessionLocal()
        try:
            extintor = db.query(cls).filter_by(id=id_extintor).first()
            if extintor:
                extintor.cliente_id = None
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db.close()
    
    @classmethod
    def show_all_client_pay(cls, client_id):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Capacidad.nombre.label('capacidad_nombre')
                )
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.cliente_id == client_id)
                .all()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def recharge_prices(cls, extintor_id):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.capacidad_id,
                Precios.valor.label("valor_num")
                )
                .join(Precios, Extintor.capacidad_id == Precios.capacidad_id)
                .filter(cls.id == extintor_id)
                .first()
            )
            print(extintores)
            return extintores
        finally:
            db.close()