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

    @classmethod
    def obtener_detalle_venta(cls, id_caja):
        from .detcaja import DetCaja
        from .extintor import Extintor
        from .lists import Capacidad, Marca, Tipo
        db = SessionLocal()
        try:
            caja_info = (
                db.query(
                    cls.id,
                    cls.fecha,
                    cls.cobro,
                    cls.adeudado,
                    cls.total,
                    cls.descripcion,
                    Cliente.nombre.label('cliente_nombre'),
                    Cliente.direccion.label('cliente_direccion'),
                    Cliente.telefono.label('cliente_telefono')
                )
                .join(Cliente, cls.cliente_id == Cliente.id)
                .filter(cls.id == id_caja)
                .first()
            )
            detalles = (
                db.query(
                    DetCaja.recarga,
                    DetCaja.nuevo,
                    DetCaja.extras,
                    DetCaja.total,
                    Extintor.numeracion,
                    Marca.nombre.label('marca_nombre'),
                    Capacidad.nombre.label('capacidad_nombre'),
                    Tipo.nombre.label('tipo_nombre')
                )
                .join(Extintor, DetCaja.id_extintor == Extintor.id)
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .filter(DetCaja.id_caja == id_caja)
                .all()
            )
            resultado = {
                'id': caja_info.id,
                'fecha': caja_info.fecha,
                'cobro': caja_info.cobro,
                'adeudado': caja_info.adeudado,
                'total': caja_info.total,
                'descripcion': caja_info.descripcion,
                'cliente': caja_info.cliente_nombre,
                'direccion': caja_info.cliente_direccion,
                'telefono': caja_info.cliente_telefono,
                'detalles': []
            }
            for detalle in detalles:
                resultado['detalles'].append({
                    'numeracion': detalle.numeracion,
                    'marca': detalle.marca_nombre,
                    'capacidad': detalle.capacidad_nombre,
                    'tipo': detalle.tipo_nombre,
                    'recarga': detalle.recarga,
                    'nuevo': detalle.nuevo,
                    'extras': detalle.extras,
                    'total': detalle.total
                })   
            return resultado
        except Exception as e:
            print(f"Error al obtener detalles de venta: {e}")
            return None
        finally:
            db.close()