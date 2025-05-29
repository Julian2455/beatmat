from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, desc
from sqlalchemy.orm import relationship,sessionmaker,joinedload
from db import Base, engine, SessionLocal
from datetime import date

class Gastos(Base):
    __tablename__='gastos'

    id = Column(Integer,primary_key= True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    insumo = Column(String(70), nullable=False)
    gasto=Column(Float)

    @property
    def fecha_formateado(self):
        if self.fecha:
            return self.fecha.strftime("%d-%m-%Y")
        return ""
    
    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            gastos = (
                db.query(cls)
                .order_by(desc(cls.fecha))
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return gastos
        finally:
            db.close()
    
    @classmethod
    def contar_gastos(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total
    
    @classmethod
    def registrar(cls,fecha,insumo,gasto):
        datos=cls(fecha=fecha,insumo=insumo,gasto=gasto)
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
    def buscar(cls, fecha, page=1, per_page=10):
        try:
            db = SessionLocal()
            query = (
                db.query(cls)
            )
            if fecha:
                query = query.filter(cls.fecha == fecha)
            resultado = (
                query
                .order_by(desc(cls.fecha))
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
    def contar_buscar(cls, fecha):
        try:
            db = SessionLocal()
            query = db.query(cls)
            if fecha:
                query = query.filter(cls.fecha == fecha)
            total = query.count()
            return total
        except Exception as e:
            print(f"Error al contar resultados: {e}")
            return 0
        finally:
            db.close()