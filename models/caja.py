from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from .cliente import Cliente

class Caja(Base):
    __tablename__='caja'

    id=Column(Integer,primary_key=True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    cobro=Column(Float)
    adeudado=Column(Float)
    total=Column(Float)
    descripcion=Column(String(255))

    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('Cliente',back_populates='caja')
    detcaja=relationship('DetCaja',back_populates='caja')

    @property
    def fecha_formateado(self):
        if self.fecha:
            return self.fecha.strftime("%d-%m-%Y")
        return ""

    @classmethod
    def confirmar_compra(cls,id,fecha,total,cobro,deuda,totales,recargas,nuevos,adicionales,descripcion=None):
        datos=cls(fecha=fecha,cliente_id=id,cobro=cobro,adeudado=deuda,total=total,descripcion=descripcion)
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
    