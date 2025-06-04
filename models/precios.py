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
    
    def verificar_y_agregar_precio(marca_id, tipo_id, capacidad_id):
        db = SessionLocal()
        try:
            recarga_existente = (
                db.query(Precios)
                .filter(
                    Precios.capacidad_id == capacidad_id,
                    Precios.nuevo == False
                )
                .first()
            )
            if not recarga_existente:
                nuevo_precio_recarga = Precios(
                    valor=0.0,
                    nuevo=False,
                    capacidad_id=capacidad_id,
                    tipo_id=None,
                    marca_id=None
                )
                db.add(nuevo_precio_recarga)
            nuevo_existente = (
                db.query(Precios)
                .filter(
                    Precios.marca_id == marca_id,
                    Precios.tipo_id == tipo_id,
                    Precios.capacidad_id == capacidad_id,
                    Precios.nuevo == True
                )
                .first()
            )
            if not nuevo_existente:
                nuevo_precio_extintor = Precios(
                    valor=0.0, 
                    nuevo=True,
                    capacidad_id=capacidad_id,
                    tipo_id=tipo_id,
                    marca_id=marca_id
                )
                db.add(nuevo_precio_extintor)
            if not recarga_existente or not nuevo_existente:
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Error al verificar/agregar precios: {e}")
            return False
        finally:
            db.close()
    
    @classmethod
    def revisar_nuevos(cls):
        db = SessionLocal()
        from .extintor import Extintor
        try:
            combinations_ids = (
                db.query(
                    Extintor.marca_id,
                    Extintor.tipo_id,
                    Extintor.capacidad_id
                )
                .distinct()
            ).all()
            for marca_id, tipo_id, capacidad_id in combinations_ids:
                existing_precio = (
                    db.query(cls)
                    .filter(
                        cls.marca_id == marca_id,
                        cls.tipo_id == tipo_id,
                        cls.capacidad_id == capacidad_id,
                        cls.nuevo == True
                    )
                    .first()
                )
                if not existing_precio:
                    nuevo_precio_extintor = Precios(
                        valor=0.0, 
                        nuevo=True,
                        capacidad_id=capacidad_id,
                        tipo_id=tipo_id,
                        marca_id=marca_id
                    )
                    db.add(nuevo_precio_extintor)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error al revisar los precios: {e}")
        finally:
            db.close()

    @classmethod
    def limpiar_nuevos(cls):
        db = SessionLocal()
        from .extintor import Extintor
        try:
            existing_extintor_combinations = (
                db.query(
                    Extintor.marca_id,
                    Extintor.tipo_id,
                    Extintor.capacidad_id
                )
                .distinct()
            ).all()
            existing_extintor_set = set(existing_extintor_combinations)
            all_precio_extintores = (
                db.query(
                    cls.id,
                    cls.marca_id,
                    cls.tipo_id,
                    cls.capacidad_id
                )
                .filter(cls.nuevo == True)
            ).all()
            precios_a_eliminar_ids = []
            for precio_id, marca_id, tipo_id, capacidad_id in all_precio_extintores:
                current_precio_combination = (marca_id, tipo_id, capacidad_id)
                if current_precio_combination not in existing_extintor_set:
                    precios_a_eliminar_ids.append(precio_id)
            if precios_a_eliminar_ids:
                db.query(cls).filter(cls.id.in_(precios_a_eliminar_ids)).delete(synchronize_session=False)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            db.close()
    
    @classmethod
    def revisar_recargas(cls):
        db = SessionLocal()
        from .extintor import Extintor
        try:
            existing_extintor_capacities = (
                db.query(Extintor.capacidad_id)
                .distinct()
            ).all()
            existing_extintor_capacity_set = set(c for c, in existing_extintor_capacities)
            existing_precio_recarga_capacities = (
                db.query(cls.capacidad_id)
                .filter(cls.nuevo == False)
                .distinct()
            ).all()
            existing_precio_recarga_capacity_set = set(c for c, in existing_precio_recarga_capacities)
            capacidades_a_agregar_recarga = []
            for cap_id in existing_extintor_capacity_set:
                if cap_id not in existing_precio_recarga_capacity_set:
                    capacidades_a_agregar_recarga.append(cap_id)
            if capacidades_a_agregar_recarga:
                for capacidad_id in capacidades_a_agregar_recarga:
                    nuevo_precio_recarga = Precios(
                        valor=0.0,
                        nuevo=False,
                        capacidad_id=capacidad_id
                    )
                    db.add(nuevo_precio_recarga)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error al agregar precios de recargas faltantes: {e}")
        finally:
            db.close()

    @classmethod
    def limpiar_recargas(cls):
        db = SessionLocal()
        from .extintor import Extintor
        try:
            existing_capacidad_ids = (
                db.query(Extintor.capacidad_id)
                .distinct()
            ).all()
            existing_capacidad_set = set(c for c, in existing_capacidad_ids)
            all_precio_recargas = (
                db.query(
                    cls.id,
                    cls.capacidad_id
                )
                .filter(cls.nuevo == False)
            ).all()
            precios_recargas_a_eliminar_ids = []
            for precio_id, capacidad_id in all_precio_recargas:
                if capacidad_id not in existing_capacidad_set:
                    precios_recargas_a_eliminar_ids.append(precio_id)
            if precios_recargas_a_eliminar_ids:
                db.query(cls).filter(cls.id.in_(precios_recargas_a_eliminar_ids)).delete(synchronize_session=False)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            db.close()