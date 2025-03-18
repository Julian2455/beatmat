from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal

class Caja(Base):
    __tablename__='caja'

    id=Column(Integer,primary_key=True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    gastos=Column(Float,nullable=False)
    cobros=Column(Float,nullable=False)
    adeudado=Column(Float,nullable=False)
    descripcion=Column(String(255),nullable=False)

    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('cliente',back_populates='caja')
    detcaja=relationship('detcaja',back_populates='caja')