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
        db=SessionLocal()
        try:
            db.add(datos)
            db.flush()
            from .detcaja import DetCaja
            for extintor_id in set(list(totales.keys()) + list(recargas.keys()) + list(nuevos.keys()) + list(adicionales.keys())):
                recarga_valor = recargas.get(extintor_id, None)
                nuevo_valor = nuevos.get(extintor_id, None)
                extra_valor = adicionales.get(extintor_id, None)
                total_valor = totales.get(extintor_id, None)
                detalle = DetCaja(
                    id_caja=datos.id,
                    id_extintor=extintor_id,
                    recarga=recarga_valor,
                    nuevo=nuevo_valor,
                    extras=extra_valor,
                    total=total_valor
                )
                db.add(detalle)
            db.commit()
            from .extintor import Extintor
            Extintor.actualizar_nuevo(nuevos)
            return True
        except Exception as e:
            print(f"Error al confirmar compra: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    