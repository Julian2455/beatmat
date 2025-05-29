from db import engine, Base
from .cliente import Cliente
from .extintor import Extintor
from .recarga import Recarga
from .caja import Caja
from .detcaja import DetCaja
from .tareas import Tareas
from .lists import *
from .precios import Precios
from .gastos import Gastos

Base.metadata.create_all(bind=engine)