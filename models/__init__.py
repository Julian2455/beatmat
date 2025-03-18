from db import engine, Base
from .cliente import Cliente
from .extintor import Extintor
from .recarga import Recarga

Base.metadata.create_all(bind=engine)