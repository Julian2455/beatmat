from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from db import Base, engine, SessionLocal

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(70), nullable=False)
    direccion = Column(String(70), nullable=False)

    caja=relationship('Caja',back_populates='cliente')

    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            clientes = (
                db.query(cls)
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return clientes
        finally:
            db.close()
    
    @classmethod
    def contar_clientes(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total