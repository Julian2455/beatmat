from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from db import Base, engine, SessionLocal

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)

    caja=relationship('caja',back_populates='cliente')