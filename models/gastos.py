from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, desc, func
from sqlalchemy.orm import relationship,sessionmaker,joinedload
from db import Base, engine, SessionLocal
from datetime import date
from .lists import CatGasto

class Gastos(Base):
    __tablename__='gastos'

    id = Column(Integer,primary_key= True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    catgasto_id = Column(Integer, ForeignKey('catgasto.id'), nullable=False)
    insumo = Column(String(70), nullable=False)
    gasto=Column(Float)

    catgasto = relationship('CatGasto', back_populates='gastos')

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
                db.query(
                    Gastos.id,
                    Gastos.fecha,
                    CatGasto.nombre.label("categoria_nombre"),
                    Gastos.insumo,
                    Gastos.gasto
                )
                .join(CatGasto, CatGasto.id == Gastos.catgasto_id)
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
    def registrar(cls,fecha,insumo,gasto,categoria):
        datos=cls(fecha=fecha,insumo=insumo,gasto=gasto,catgasto_id=categoria)
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
                db.query(
                    Gastos.id,
                    Gastos.fecha,
                    CatGasto.nombre.label("categoria_nombre"),
                    Gastos.insumo,
                    Gastos.gasto
                )
            )
            if fecha:
                query = query.filter(cls.fecha == fecha)
            resultado = (
                query
                .join(CatGasto, CatGasto.id == Gastos.catgasto_id)
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
    
    @classmethod
    def gastos_por_categoria_mes(cls, año, mes=None):
        db = SessionLocal()
        try:
            query = (
                db.query(
                    CatGasto.nombre.label('categoria'),
                    func.sum(cls.gasto).label('total_gasto'),
                    func.count(cls.id).label('cantidad_gastos')
                )
                .join(CatGasto, cls.catgasto_id == CatGasto.id)
                .filter(func.strftime('%Y', cls.fecha) == str(año))
            )
            if mes is not None:
                query = query.filter(func.strftime('%m', cls.fecha) == f"{mes:02d}")
            resultado = (
                query
                .group_by(CatGasto.id, CatGasto.nombre)
                .order_by(func.sum(cls.gasto).desc())
                .all()
            )
            datos_grafico = []
            for row in resultado:
                datos_grafico.append({
                    'categoria': row.categoria,
                    'total_gasto': float(row.total_gasto or 0),
                    'cantidad_gastos': int(row.cantidad_gastos or 0)
                })
            return datos_grafico
        except Exception as e:
            print(f"Error al obtener gastos por categoría: {e}")
            return []
        finally:
            db.close()