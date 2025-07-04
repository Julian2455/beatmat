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
    
    @classmethod
    def registrar(cls,vto_control,nuevo_control,vto_ph,fabricacion,extintor_id):
        datos=cls(vto_control_recarga=vto_control,nuevo_control_recarga=nuevo_control,
                vto_ph=vto_ph,fecha_fabricacion=fabricacion,extintor_id=extintor_id)
        try:
            db = SessionLocal()
            db.add(datos)
            db.commit()
            from .extintor import Extintor
            Extintor.actualizar_impreso(extintor_id)
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def contar_gastos(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total
    
    @classmethod
    def eliminar_recarga(cls, recarga_id, id_extintor):
        db = SessionLocal()
        try:
            recarga = db.query(cls).filter(cls.id == recarga_id).first()
            if recarga:
                db.delete(recarga)
                db.commit()
                total = db.query(cls).filter(cls.extintor_id==id_extintor).count()
                if total>0:
                    return True
                from .extintor import Extintor
                extintor = db.query(Extintor).filter_by(id=id_extintor).first()
                if extintor:
                    extintor.impreso=True
                    db.commit()
                    return True 
            return False
        except Exception as e:
            print(f"Error al eliminar la recarga: {e}")
            db.rollback()
            return False
        finally:
            db.close()