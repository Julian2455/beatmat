from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean, func
from sqlalchemy.orm import relationship,sessionmaker
from db import Base, engine, SessionLocal
from datetime import date

class Tareas(Base):
    __tablename__='tareas'

    id=Column(Integer,primary_key=True,autoincrement=True)
    tamizacion=Column(Boolean,nullable=False)
    peso=Column(Boolean,nullable=False)
    control_tacho=Column(Boolean,nullable=False)
    relleno_polvo=Column(Boolean,nullable=False)
    cambio_manometro=Column(Boolean,nullable=False)
    oring=Column(Boolean,nullable=False)
    gatillo=Column(Boolean,nullable=False)
    pintura=Column(Boolean,nullable=False)
    interior=Column(Boolean,nullable=False)
    valvula=Column(Boolean,nullable=False)
    bastago_bronce=Column(Boolean,nullable=False)
    otro=Column(Boolean,nullable=False)
    observacion=Column(String(255))
    fecha=Column(Date,nullable=False)
    cambio_manguera=Column(Boolean,nullable=True)
    prueba_hidraulica=Column(Boolean,nullable=True)
    empresa=Column(String(50),nullable=True)

    extintor_id=Column(Integer, ForeignKey('extintor.id'))

    extintor=relationship('Extintor',back_populates='tareas')

    @property
    def fecha_formateada(self):
        if self.fecha:
            return self.fecha.strftime("%d-%m-%Y")
        return ""

    @classmethod
    def show_all(cls):
        db = SessionLocal()
        try:
            tareas = db.query(cls).all()
            return tareas
        finally:
            db.close()

    @classmethod
    def show_filter(cls, extintor_id):  
        db = SessionLocal()
        try:
            tareas = db.query(cls).filter(cls.extintor_id == extintor_id).order_by(cls.id.desc()).all() 
            return tareas
        finally:
            db.close()
    
    @classmethod
    def registrar(cls,bastago,manometro,tacho,gatillo,interior,oring,otro,peso,pintura,relleno,tamizacion,valvula,manguera,ph,empresa,observacion,fecha,extintor_id):
        datos=cls(bastago_bronce=bastago,cambio_manometro=manometro,control_tacho=tacho,
                gatillo=gatillo,interior=interior,oring=oring,otro=otro,peso=peso,pintura=pintura,
                relleno_polvo=relleno,tamizacion=tamizacion,valvula=valvula,cambio_manguera=manguera,prueba_hidraulica=ph,empresa=empresa,observacion=observacion,
                fecha=fecha,extintor_id=extintor_id)
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
    def contar_tareas_en_rango(cls, fecha_inicio: date, fecha_fin: date) -> int:
        db = SessionLocal()
        try:
            count = (
                db.query(cls)
                .filter(cls.fecha >= fecha_inicio, cls.fecha <= fecha_fin)
                .count()
            )
            return count
        finally:
            db.close()

    @classmethod
    def eliminar_tarea(cls, tarea_id):
        db = SessionLocal()
        try:
            tarea = db.query(cls).filter(cls.id == tarea_id).first()
            if tarea:
                db.delete(tarea)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar la tarea: {e}")
            db.rollback()
            return False
        finally:
            db.close()