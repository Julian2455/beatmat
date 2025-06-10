from sqlalchemy import Column, Integer, String, ForeignKey, func, and_, Boolean
from sqlalchemy.orm import relationship, joinedload
from db import Base, engine, SessionLocal
from .cliente import Cliente
from .lists import *
from .recarga import Recarga
from .tareas import Tareas
from .precios import Precios
from datetime import datetime, timedelta

class Extintor(Base):
    __tablename__='extintor'

    id=Column(Integer,primary_key=True,autoincrement=True)
    numeracion=Column(Integer,nullable=False,unique=True)
    marca_id=Column(Integer, ForeignKey('marca.id'), nullable=False)
    ubicacion=Column(String(70),nullable=False)
    tipo_id=Column(Integer, ForeignKey('tipo.id'), nullable=False)
    capacidad_id=Column(Integer, ForeignKey('capacidad.id'), nullable=False)
    nuevo = Column(Boolean, nullable=True)
    impreso=Column(Boolean, nullable=False)
    estado=Column(Boolean, default=True)

    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('Cliente',back_populates='extintor')
    marca=relationship('Marca', back_populates='extintores')
    tipo=relationship('Tipo', back_populates='extintores')
    capacidad=relationship('Capacidad', back_populates='extintores')
    recarga=relationship('Recarga',back_populates='extintor')
    detcaja=relationship('DetCaja',back_populates='extintor')
    tareas=relationship('Tareas',back_populates='extintor')

    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.nombre.label('capacidad_nombre'),
                Extintor.impreso
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.estado==True)
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return extintores
        finally:
            db.close()
        
    @classmethod
    def show_all_card(cls):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.nombre.label('marca_nombre'),
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.nombre.label('capacidad_nombre'),
                Extintor.impreso
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.impreso==False)
                .filter(cls.estado==True)
                .all()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def show_all_client(cls, client_id):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.nombre.label('capacidad_nombre')
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.cliente_id == client_id)
                .filter(cls.estado==True)
                .all()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def contar_extintores(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total
    
    @classmethod
    def registrar(cls,numeracion,marca,ubicacion,tipo,capacidad):
        datos=cls(numeracion=numeracion,marca_id=marca,ubicacion=ubicacion,tipo_id=tipo,capacidad_id=capacidad,nuevo=True,impreso=True)
        try:
            db = SessionLocal()
            db.add(datos)
            db.commit()
            from .precios import Precios  # Esto se importa aca para evitar la importación circular con la relacion de la tabla
            Precios.verificar_y_agregar_precio(marca, tipo, capacidad)
            return True
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def actualizar(cls, id_extintor, numeracion, marca, ubicacion, tipo, capacidad):
        try:
            db = SessionLocal()
            extintor = db.query(cls).filter_by(id=id_extintor).first()
            if extintor:
                extintor.numeracion = numeracion
                extintor.marca_id = marca
                extintor.ubicacion = ubicacion
                extintor.tipo_id = tipo
                extintor.capacidad_id = capacidad
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al actualizar extintor: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    @classmethod
    def eliminar_extintor(cls,extintor_id):
        try:
            db=SessionLocal()
            extintor = db.query(cls).filter_by(id=extintor_id).first()
            if extintor:
                extintor.estado = False
                db.commit()
                return True
            return False
        except Exception as e:
            print(e)
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def get_by_id(cls, id_extintor):
        try:
            db = SessionLocal()
            extintor = (db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.id.label('marca_id'),
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.id.label('tipo_id'),
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.id.label('capacidad_id'),
                Capacidad.nombre.label('capacidad_nombre')
            )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.id == id_extintor).first())
            return extintor
        except Exception as e:
            print(f"Error al obtener id: {e}")
            return None
        
    @classmethod
    def extintor_asociado_cliente(cls, id_cliente):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                    Extintor.id,
                    Extintor.numeracion,
                    Extintor.ubicacion,
                    Marca.nombre.label("marca"),
                    Tipo.nombre.label("tipo"),
                    Capacidad.nombre.label("capacidad"),
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(Extintor.cliente_id == id_cliente)
                .filter(cls.estado==True)
                .all()
            )
            resultado = []
            for ext in extintores:
                ext_id = ext.id
                ultima_recarga = (
                    db.query(Recarga)
                    .filter(Recarga.extintor_id == ext_id)
                    .order_by(Recarga.nuevo_control_recarga.desc())
                    .first()
                )
                ultima_tarea = (
                    db.query(Tareas)
                    .filter(Tareas.extintor_id == ext_id)
                    .order_by(Tareas.fecha.desc())
                    .first()
                )
                resultado.append({
                    "id": ext.id,
                    "numeracion": ext.numeracion,
                    "ubicacion": ext.ubicacion,
                    "marca": ext.marca,
                    "tipo": ext.tipo,
                    "capacidad": ext.capacidad,
                    "ultima_recarga": ultima_recarga,
                    "ultima_tarea": ultima_tarea
                })
            return resultado       
        except Exception as e:
            print(f"Error en consulta: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def buscar(cls, numeracion, marca_filter, tipo_filter, capacidad_filter, page=1, per_page=10, disponible=None):
        try:
            db = SessionLocal()
            query = (
                db.query(
                    Extintor.id,
                    Extintor.numeracion,
                    Marca.nombre.label('marca_nombre'),
                    Extintor.ubicacion,
                    Tipo.nombre.label('tipo_nombre'),
                    Capacidad.nombre.label('capacidad_nombre'),
                    Extintor.impreso
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.estado==True) ##############ACA CAMBIE
            )
            if numeracion:
                query = query.filter(Extintor.numeracion.like(f"{numeracion}%"))
            if marca_filter:
                query = query.filter(Extintor.marca_id == marca_filter)
            if tipo_filter:
                query = query.filter(Extintor.tipo_id == tipo_filter)
            if capacidad_filter:
                query = query.filter(Extintor.capacidad_id == capacidad_filter)
            if disponible:
                query = query.filter(Extintor.cliente_id.is_(None))
            extintores = (
                query
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return extintores
        except Exception as e:
            print(f"Error al buscar: {e}")
            return []
        finally:
            db.close()
    
    @classmethod
    def buscar_card(cls, numeracion, marca_filter, tipo_filter, capacidad_filter, impreso_filter=True,disponible=None):
        try:
            db = SessionLocal()
            query = (
                db.query(
                    Extintor.id,
                    Extintor.numeracion,
                    Marca.nombre.label('marca_nombre'),
                    Tipo.nombre.label('tipo_nombre'),
                    Capacidad.nombre.label('capacidad_nombre'),
                    Extintor.impreso
                )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.estado==True)
            )
            if numeracion:
                query = query.filter(Extintor.numeracion.like(f"{numeracion}%"))
            if marca_filter:
                query = query.filter(Extintor.marca_id == marca_filter)
            if tipo_filter:
                query = query.filter(Extintor.tipo_id == tipo_filter)
            if capacidad_filter:
                query = query.filter(Extintor.capacidad_id == capacidad_filter)
            if disponible:
                query = query.filter(Extintor.cliente_id.is_(None))
            if impreso_filter:
                query = query.filter(cls.impreso==False)
            extintores = (
                query
                .all()
            )
            return extintores
        except Exception as e:
            print(f"Error al buscar: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def contar_buscar(cls, numeracion, marca_filter, tipo_filter, capacidad_filter, disponible=None):
        try:
            db = SessionLocal()
            query = db.query(cls)
            if numeracion:
                query = query.filter(cls.numeracion.like(f"{numeracion}%"))
            if marca_filter:
                query = query.filter(cls.marca_id == marca_filter)
            if tipo_filter:
                query = query.filter(cls.tipo_id == tipo_filter)
            if capacidad_filter:
                query = query.filter(cls.capacidad_id == capacidad_filter)
            if disponible:
                query = query.filter(Extintor.cliente_id.is_(None))
            total = query.count()
            return total
        except Exception as e:
            print(f"Error al contar resultados: {e}")
            return 0
        finally:
            db.close()
    
    @classmethod
    def disponibles(cls):
        try:
            db = SessionLocal()
            extintor = (db.query(
                Extintor.id,
                Extintor.numeracion,
                Marca.id.label('marca_id'),
                Marca.nombre.label('marca_nombre'),
                Extintor.ubicacion,
                Tipo.id.label('tipo_id'),
                Tipo.nombre.label('tipo_nombre'),
                Capacidad.id.label('capacidad_id'),
                Capacidad.nombre.label('capacidad_nombre')
            )
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(Extintor.cliente_id.is_(None))
                .all()
            )
            return extintor
        except Exception as e:
            print(f"Error al obtener id: {e}")
            return None
    
    @classmethod
    def asignar_cliente(cls, lista_extintores, id_cliente):
        db = SessionLocal()
        try:
            for id_extintor in lista_extintores:
                extintor = db.query(cls).filter_by(id=id_extintor).first()
                if extintor:
                    extintor.cliente_id = id_cliente
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db.close()
    
    @classmethod
    def liberar_extintor(cls, id_extintor):
        db = SessionLocal()
        try:
            extintor = db.query(cls).filter_by(id=id_extintor).first()
            if extintor:
                extintor.cliente_id = None
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db.close()
    
    @classmethod
    def show_all_client_pay(cls, client_id):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.numeracion,
                Capacidad.nombre.label('capacidad_nombre'),
                Extintor.nuevo
                )
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.cliente_id == client_id)
                .all()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def recharge_prices(cls, extintor_id):
        db = SessionLocal()
        try:
            extintores = (
                db.query(
                Extintor.id,
                Extintor.capacidad_id,
                Precios.valor.label("valor_num")
                )
                .join(Precios, Extintor.capacidad_id == Precios.capacidad_id)
                .filter(cls.id == extintor_id)
                .filter(Precios.nuevo==False)
                .first()
            )
            return extintores
        finally:
            db.close()
    
    @classmethod
    def new_prices(cls, extintor_id):
        db = SessionLocal()
        try:
            extintor = (
                db.query(
                cls.id,
                cls.marca_id,
                cls.tipo_id,
                cls.capacidad_id
                )
                .filter(Precios.nuevo==True)
                .filter(cls.id == extintor_id).first()
            )
            precio=(
                db.query(
                    Precios.valor.label("valor_num")
                )
                .filter(Precios.marca_id == extintor.marca_id, Precios.tipo_id==extintor.tipo_id, Precios.capacidad_id==extintor.capacidad_id).first()
            )
            return precio
        finally:
            db.close()

    @classmethod
    def vencimientos_proximos(cls, dias=30, page=1, per_page=10):
        db = SessionLocal()
        try:
            fecha_actual = datetime.today().date()
            fecha_limite = fecha_actual + timedelta(days=dias)
            subconsulta = (
                db.query(
                    Recarga.extintor_id,
                    func.max(Recarga.nuevo_control_recarga).label("ultima_fecha")
                )
                .group_by(Recarga.extintor_id)
                .subquery()
            )
            recargas_ids = (
                db.query(Recarga.id)
                .join(subconsulta, (subconsulta.c.extintor_id == Recarga.extintor_id) &
                                (subconsulta.c.ultima_fecha == Recarga.nuevo_control_recarga))
                .filter(Recarga.nuevo_control_recarga <= fecha_limite)
                .filter(cls.estado==True)
                .order_by(Recarga.nuevo_control_recarga)
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return [r.id for r in recargas_ids]
        except Exception as e:
            print(f"Error al obtener IDs de vencimientos paginados: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def contar_vencimientos_proximos(cls, dias=30):
        db = SessionLocal()
        try:
            fecha_actual = datetime.today().date()
            fecha_limite = fecha_actual + timedelta(days=dias)
            subconsulta = (
                db.query(
                    Recarga.extintor_id,
                    func.max(Recarga.nuevo_control_recarga).label("ultima_fecha")
                )
                .group_by(Recarga.extintor_id)
                .subquery()
            )
            total = (
                db.query(func.count())
                .select_from(Recarga)
                .join(subconsulta, (subconsulta.c.extintor_id == Recarga.extintor_id) &
                                (subconsulta.c.ultima_fecha == Recarga.nuevo_control_recarga))
                .filter(Recarga.nuevo_control_recarga <= fecha_limite)
                .filter(cls.estado==True)
                .scalar()
            )
            return total
        except Exception as e:
            print(f"Error al contar vencimientos: {e}")
            return 0
        finally:
            db.close()
    
            
    @classmethod
    def print_vencimientos(cls, dias):
        db = SessionLocal()
        try:
            fecha_actual = datetime.today().date()
            fecha_limite = fecha_actual + timedelta(days=dias)
            subconsulta = (
                db.query(
                    Recarga.extintor_id,
                    func.max(Recarga.nuevo_control_recarga).label("ultima_fecha")
                )
                .group_by(Recarga.extintor_id)
                .subquery()
            )
            recargas_ids = (
                db.query(Recarga.id)
                .join(subconsulta, (subconsulta.c.extintor_id == Recarga.extintor_id) &
                                (subconsulta.c.ultima_fecha == Recarga.nuevo_control_recarga))
                .filter(Recarga.nuevo_control_recarga <= fecha_limite)
                .order_by(Recarga.nuevo_control_recarga)
                .all()
            )
            return [r.id for r in recargas_ids]
        except Exception as e:
            print(f"Error al obtener IDs de vencimientos paginados: {e}")
            return []
        finally:
            db.close()
    
    @classmethod
    def detalles_vencimientos_por_ids(cls, ids):
        if not ids:
            return []
        db = SessionLocal()
        try:
            resultados = (
                db.query(
                    Cliente.nombre.label("cliente"),
                    Cliente.direccion.label("ubicacion"),
                    Extintor.numeracion,
                    Marca.nombre.label("marca"),
                    Recarga.nuevo_control_recarga.label("vto_recarga"),
                    Recarga.vto_ph.label("vto_ph")
                )
                .join(Extintor, Extintor.id == Recarga.extintor_id)
                .join(Cliente, Cliente.id == Extintor.cliente_id)
                .join(Marca, Marca.id == Extintor.marca_id)
                .filter(Recarga.id.in_(ids))
                .filter(cls.estado==True)
                .order_by(Recarga.nuevo_control_recarga)
                .all()
            )
            return resultados
        except Exception as e:
            print(f"Error al obtener detalles por IDs: {e}")
            return []
        finally:
            db.close()
        
    @classmethod
    def tipos(cls): #buscar forma de usar esta consulta para automatizar el registro en la tabla precios
        db = SessionLocal()
        try:
            precios = (
                db.query(
                    Marca.nombre.label('marca'),
                    Tipo.nombre.label('tipo'),
                    Capacidad.nombre.label('capacidad')
                )
                .join(Extintor, Extintor.marca_id == Marca.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(cls.cliente_id.is_(None))
                .distinct()
                .order_by(Marca.nombre, Tipo.nombre, Capacidad.nombre) #ver si cambiar el tipo de dato en capacidad para solo poner numeros y no la unidad de medida
            )
            return precios
        finally:
            db.close()
    
    @classmethod
    def actualizar_nuevo(cls, nuevos):
        try:
            db = SessionLocal()
            for id_extintor in nuevos.keys():
                extintor = db.query(cls).filter_by(id=id_extintor).first()
                if extintor:
                    extintor.nuevo=False 
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar extintor: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def actualizar_impreso(cls, extintor_ids):
        try:
            db = SessionLocal()
            for id_extintor in extintor_ids:
                extintor = db.query(cls).filter_by(id=id_extintor).first()
                if extintor:
                    extintor.impreso=False 
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar extintor: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def marcar_como_impresos(cls, extintor_ids):
        try:
            db = SessionLocal()
            for id_extintor in extintor_ids:
                extintor = db.query(cls).filter_by(id=id_extintor).first()
                if extintor:
                    extintor.impreso=True
            db.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar extintor: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def obtener_datos_para_tarjeta(cls, extintor_id):
        db = SessionLocal()
        try:
            extintor_query = (
                db.query(
                    Extintor.id,
                    Extintor.numeracion,
                    Cliente.nombre.label('cliente_nombre'),
                    Tipo.nombre.label('tipo_nombre'),
                    Capacidad.nombre.label('capacidad_nombre')
                )
                .outerjoin(Cliente, Extintor.cliente_id == Cliente.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .filter(Extintor.id == extintor_id)
                .first()
            )
            ultima_recarga = (
                db.query(Recarga)
                .filter(Recarga.extintor_id == extintor_id)
                .order_by(Recarga.nuevo_control_recarga.desc())
                .first()
            )
            if ultima_recarga:
                if ultima_recarga.vto_ph:
                    vto_ph = str(ultima_recarga.vto_ph)
                if ultima_recarga.nuevo_control_recarga:
                    fecha_vencimiento = ultima_recarga.nuevo_control_recarga.strftime("%d/%m/%Y")
            resultado = {
                'propietario': extintor_query.cliente_nombre or '',
                'clase': extintor_query.tipo_nombre or '',
                'capacidad': extintor_query.capacidad_nombre or '',
                'vto_prueba_hidraulica': vto_ph,
                'fecha_vencimiento': fecha_vencimiento,
                'numero': str(extintor_query.numeracion) if extintor_query.numeracion else ''
            }
            return resultado
        except Exception as e:
            print(f"Error al obtener información completa del extintor: {e}")
            return None
        finally:
            db.close()