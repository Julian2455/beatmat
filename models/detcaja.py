from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .caja import Caja
from .extintor import Extintor

class DetCaja(Base):
    __tablename__='detcaja'

    id_caja=Column(Integer,ForeignKey('caja.id'),primary_key=True)
    id_extintor=Column(Integer,ForeignKey('extintor.id'),primary_key=True)
    cantidad_entra=Column(Integer)
    cantidad_sale=Column(Integer)
    precio=Column(Float,nullable=False)

    caja=relationship('Caja',back_populates='detcaja')
    extintor=relationship('Extintor',back_populates='detcaja')