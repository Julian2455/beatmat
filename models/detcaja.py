from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .caja import Caja
from .extintor import Extintor

class DetCaja(Base):
    __tablename__='detcaja'

    id_caja=Column(Integer,ForeignKey('caja.id'),primary_key=True,nullable=False)
    id_extintor=Column(Integer,ForeignKey('extintor.id'),primary_key=True,nullable=False)
    recarga=Column(Float,nullable=True)
    nuevo=Column(Float,nullable=True)
    extras=Column(Float,nullable=True)
    total=Column(Float,nullable=True)

    caja=relationship('Caja',back_populates='detcaja')
    extintor=relationship('Extintor',back_populates='detcaja')