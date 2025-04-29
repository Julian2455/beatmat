from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .lists import Capacidad, Tipo, Marca

class Precios(Base):
    __tablename__ = 'precios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    nuevo = Column(Boolean, nullable=True)
    
    capacidad_id = Column(Integer, ForeignKey('capacidad.id'), nullable=True)
    tipo_id = Column(Integer, ForeignKey('tipo.id'), nullable=True)
    marca_id = Column(Integer, ForeignKey('marca.id'), nullable=True)

    capacidad = relationship('Capacidad', back_populates='precios')
    tipo = relationship('Tipo', back_populates='precios')
    marca = relationship('Marca', back_populates='precios')

    @classmethod
    def precio_nuevos(cls):
        db = SessionLocal()
        try:
            precios = (
                db.query(
                    cls.id.label('id'),
                    Marca.nombre.label('marca'),
                    Tipo.nombre.label('tipo'),
                    Capacidad.nombre.label('capacidad'),
                    cls.valor.label('valor')
                )
                .join(Marca, cls.marca_id == Marca.id)
                .join(Tipo, cls.tipo_id == Tipo.id)
                .join(Capacidad, cls.capacidad_id == Capacidad.id)
                .filter(cls.nuevo==True)
                .order_by(Marca.nombre, Tipo.nombre, Capacidad.nombre) #ver si cambiar el tipo de dato en capacidad para solo poner numeros y no la unidad de medida
            )
            return precios
        finally:
            db.close()
    
    @classmethod
    def precio_recargas(cls):
        db = SessionLocal()
        try:
            precios = (
                db.query(
                    cls.id.label('id'),
                    Capacidad.nombre.label('capacidad'),
                    cls.valor.label('valor')
                )
                .join(Capacidad, cls.capacidad_id == Capacidad.id)
                .filter(cls.nuevo==False)
                .order_by(Capacidad.nombre)
            )
            return precios
        finally:
            db.close()
    
    @classmethod
    def actualizar_precios(cls,lista_precios):
        try:
            db = SessionLocal()
            for id_precio, datos in lista_precios.items():
                item = db.query(cls).filter_by(id=id_precio).first()
                if item:
                    item.valor=datos['valor']
            db.commit()
        except Exception as e:
            print(f"Error al actualizar extintor: {e}")
            db.rollback()
            return False
        finally:
            db.close()