from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,sessionmaker,joinedload
from db import Base, engine, SessionLocal
from datetime import date
from .cliente import Cliente

class Caja(Base):
    __tablename__='caja'

    id=Column(Integer,primary_key=True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    cobro=Column(Float)
    adeudado=Column(Float)
    total=Column(Float)
    descripcion=Column(String(255))

    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('Cliente',back_populates='caja')
    detcaja=relationship('DetCaja',back_populates='caja')

    @property
    def fecha_formateado(self):
        if self.fecha:
            return self.fecha.strftime("%d-%m-%Y")
        return ""

    @classmethod
    def confirmar_compra(cls,id,fecha,total,cobro,deuda,totales,recargas,nuevos,adicionales,descripcion=None):
        datos=cls(fecha=fecha,cliente_id=id,cobro=cobro,adeudado=deuda,total=total,descripcion=descripcion)
        db=SessionLocal()
        try:
            db.add(datos)
            db.flush()
            extintores_ids=set()
            from .detcaja import DetCaja
            for extintor_id in set(list(totales.keys()) + list(recargas.keys()) + list(nuevos.keys()) + list(adicionales.keys())):
                extintores_ids.add(extintor_id)
                recarga_valor = recargas.get(extintor_id, None)
                nuevo_valor = nuevos.get(extintor_id, None)
                extra_valor = adicionales.get(extintor_id, None)
                total_valor = totales.get(extintor_id, None)
                detalle = DetCaja(
                    id_caja=datos.id,
                    id_extintor=extintor_id,
                    recarga=recarga_valor,
                    nuevo=nuevo_valor,
                    extras=extra_valor,
                    total=total_valor
                )
                db.add(detalle)
            db.commit()
            from .extintor import Extintor
            Extintor.actualizar_nuevo(nuevos)
            Extintor.actualizar_impreso(extintores_ids)
            return True
        except Exception as e:
            print(f"Error al confirmar compra: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            ventas = (
                db.query(
                    cls, 
                    Cliente.nombre.label('nombre')
                )
                .join(Cliente, cls.cliente_id == Cliente.id)
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return ventas
        finally:
            db.close()
    
    @classmethod
    def contar_ventas(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total
    
    @classmethod
    def obtener_fecha_minima(cls):
        db = SessionLocal()
        try:
            resultado = db.query(cls.fecha).order_by(cls.fecha.asc()).first()
            if resultado:
                return resultado[0]
            else:
                return date(2000, 1, 1) 
        finally:
            db.close()
    
    @classmethod
    def buscar(cls, cliente, fecha, page=1, per_page=10):
        try:
            db = SessionLocal()
            query = (
                db.query(
                    cls,
                    Cliente.nombre.label('nombre_cliente')
                )
                .join(Cliente, cls.cliente_id == Cliente.id)
            )
            if cliente:
                query = query.filter(cls.cliente_id == cliente)
            if fecha:
                query = query.filter(cls.fecha == fecha)
            resultado = (
                query
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return resultado
        except Exception as e:
            print(f"Error al buscar: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def contar_buscar(cls, cliente, fecha):
        try:
            db = SessionLocal()
            query = db.query(cls)
            if cliente:
                query = query.filter(cls.cliente_id == cliente)
            if fecha:
                query = query.filter(cls.fecha == fecha)
            total = query.count()
            return total
        except Exception as e:
            print(f"Error al contar resultados: {e}")
            return 0
        finally:
            db.close()