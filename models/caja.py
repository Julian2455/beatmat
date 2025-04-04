from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .cliente import Cliente

class Caja(Base):
    __tablename__='caja'

    id=Column(Integer,primary_key=True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    gastos=Column(Float)
    cobros=Column(Float)
    adeudado=Column(Float)
    descripcion=Column(String(255))

    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('Cliente',back_populates='caja')
    detcaja=relationship('DetCaja',back_populates='caja')

    @classmethod
    def show_all(cls,page=1, per_page=10):
        db = SessionLocal()
        try:
            cajas = (
                db.query(cls)
                .offset((page -1) * per_page)
                .limit(per_page)
                .all()
            )
            return cajas
        finally:
            db.close()
    
    @classmethod
    def contar_cajas(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total
