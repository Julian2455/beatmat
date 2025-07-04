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
    def registrar(cls, nombre):
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
    
    @classmethod
    def tiene_referencias(cls, id):
        db = SessionLocal()
        try:
            from .extintor import Extintor
            from .precios import Precios
            tiene_extintores = db.query(Extintor).filter_by(marca_id=id).first()
            tiene_precios = db.query(Precios).filter_by(marca_id=id).first()
            return tiene_extintores is not None or tiene_precios is not None
        finally:
            db.close()

    @classmethod
    def eliminar_por_id(cls, id):
        db = SessionLocal()
        try:
            if cls.tiene_referencias(id):
                return False
            obj = db.query(cls).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar Marca: {e}")
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
    def registrar(cls, nombre):
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
    
    @classmethod
    def tiene_referencias(cls, id):
        db = SessionLocal()
        try:
            from .extintor import Extintor
            from .precios import Precios
            tiene_extintores = db.query(Extintor).filter_by(tipo_id=id).first()
            tiene_precios = db.query(Precios).filter_by(tipo_id=id).first()
            return tiene_extintores is not None or tiene_precios is not None
        finally:
            db.close()

    @classmethod
    def eliminar_por_id(cls, id):
        db = SessionLocal()
        try:
            if cls.tiene_referencias(id):
                return False
            obj = db.query(cls).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar Tipo: {e}")
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
    def registrar(cls, nombre):
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

    @classmethod
    def tiene_referencias(cls, id):
        db = SessionLocal()
        try:
            from .extintor import Extintor
            from .precios import Precios
            tiene_extintores = db.query(Extintor).filter_by(capacidad_id=id).first()
            tiene_precios = db.query(Precios).filter_by(capacidad_id=id).first()
            return tiene_extintores is not None or tiene_precios is not None
        finally:
            db.close()

    @classmethod
    def eliminar_por_id(cls, id):
        db = SessionLocal()
        try:
            if cls.tiene_referencias(id):
                return False
            obj = db.query(cls).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar Capacidad: {e}")
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
    def registrar(cls, nombre):
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
    
    @classmethod
    def tiene_referencias(cls, id):
        db = SessionLocal()
        try:
            from .gastos import Gastos
            tiene_gastos = db.query(Gastos).filter_by(catgasto_id=id).first()
            return tiene_gastos is not None
        finally:
            db.close()

    @classmethod
    def eliminar_por_id(cls, id):
        db = SessionLocal()
        try:
            if cls.tiene_referencias(id):
                return False
            obj = db.query(cls).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar Categoria gasto: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def inicializar_registro_fijo(cls):
        db = SessionLocal()
        try:
            nitrogeno_existente = db.query(cls).filter_by(nombre="Nitrógeno").first()
            if not nitrogeno_existente:
                nuevo_nitrogeno = cls(nombre="Nitrógeno")
                db.add(nuevo_nitrogeno)
                db.commit()
        except Exception as e:
            print(f"Error al inicializar CatGasto: {e}")
            db.rollback()
        finally:
            db.close()

class CatPagos(Base):
    __tablename__ = 'catpagos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    caja = relationship('Caja', back_populates='catpagos')

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            lista = (
                db.query(cls).all()
            )
            return lista
        finally:
            db.close()
    
    @classmethod
    def registrar(cls, nombre):
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
    
    @classmethod
    def tiene_referencias(cls, id):
        db = SessionLocal()
        try:
            from .caja import Caja
            tiene_ventas = db.query(Caja).filter_by(medio_pago=id).first()
            return tiene_ventas is not None
        finally:
            db.close()

    @classmethod
    def eliminar_por_id(cls, id):
        db = SessionLocal()
        try:
            if cls.tiene_referencias(id):
                return False
            obj = db.query(cls).get(id)
            if obj:
                db.delete(obj)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar Medio de pago: {e}")
            db.rollback()
            return False
        finally:
            db.close()