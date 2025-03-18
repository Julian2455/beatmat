from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal

class Recarga(Base):
    __tablename__='recarga'

    id=Column(Integer,primary_key=True,autoincrement=True)
    vto_control_recarga=Column(Date,nullable=False)
    nuevo_control_recarga=Column(Date,nullable=False)
    vto_ph=Column(Integer,nullable=False)
    fecha_fabricacion=Column(Integer,nullable=False)

    extintor_id=Column(Integer, ForeignKey('extintor.id'))

    extintor=relationship('extintor',back_populates='recarga')