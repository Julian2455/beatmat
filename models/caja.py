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