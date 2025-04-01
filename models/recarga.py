from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .extintor import Extintor

class Recarga(Base):
    __tablename__='recarga'

    id=Column(Integer,primary_key=True,autoincrement=True)
    vto_control_recarga=Column(Date,nullable=False)
    nuevo_control_recarga=Column(Date,nullable=False)
    vto_ph=Column(Integer,nullable=False)
    fecha_fabricacion=Column(Integer,nullable=False)

    extintor_id=Column(Integer, ForeignKey('extintor.id'))

    extintor=relationship('Extintor',back_populates='recarga')

    @property
    def vto_control_recarga_formateado(self):
        if self.vto_control_recarga:
            return self.vto_control_recarga.strftime("%d-%m-%Y")
        return ""
        
    @property
    def nuevo_control_recarga_formateado(self):
        if self.nuevo_control_recarga:
            return self.nuevo_control_recarga.strftime("%d-%m-%Y") 
        return ""

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            recargas = db.query(cls).all()
            return recargas
        finally:
            db.close()

    @classmethod
    def show_filter(cls, extintor_id):  
        db = SessionLocal()
        try:
            recargas = db.query(cls).filter(cls.extintor_id == extintor_id).order_by(cls.id.desc()).all() 
            return recargas
        finally:
            db.close()