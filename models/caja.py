from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, desc, func, case
from sqlalchemy.orm import relationship,sessionmaker,joinedload
from db import Base, engine, SessionLocal
from datetime import date
from .cliente import Cliente
from .lists import CatPagos

class Caja(Base):
    __tablename__='caja'

    id=Column(Integer,primary_key=True,autoincrement=True)
    fecha=Column(Date,nullable=False)
    cobro=Column(Float)
    adeudado=Column(Float)
    total=Column(Float)
    descripcion=Column(String(255))
    medio_pago=Column(Integer, ForeignKey('catpagos.id'))
    cliente_id=Column(Integer, ForeignKey('cliente.id'))

    cliente=relationship('Cliente',back_populates='caja')
    detcaja=relationship('DetCaja',back_populates='caja', cascade="all, delete-orphan")
    catpagos=relationship('CatPagos',back_populates='caja')

    @property
    def fecha_formateado(self):
        if self.fecha:
            return self.fecha.strftime("%d-%m-%Y")
        return ""

    @classmethod
    def confirmar_compra(cls,id,fecha,total,cobro,deuda,totales,recargas,nuevos,adicionales,medio_pago,descripcion=None):
        datos=cls(fecha=fecha,cliente_id=id,cobro=cobro,adeudado=deuda,total=total,medio_pago=medio_pago,descripcion=descripcion)
        db=SessionLocal()
        try:
            db.add(datos)
            db.flush()
            extintores_ids=set()
            from .detcaja import DetCaja
            for extintor_id in set(list(totales.keys()) + list(recargas.keys()) + list(nuevos.keys()) + list(adicionales.keys())):
                extintores_ids.add(extintor_id)
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
    
    @classmethod
    def show_all(cls, page=1, per_page=10):
        db = SessionLocal()
        try:
            ventas = (
                db.query(
                    cls, 
                    Cliente.nombre.label('nombre'),
                    CatPagos.nombre.label('nombre_metodo')
                )
                .join(Cliente, cls.cliente_id == Cliente.id)
                .join(CatPagos, cls.medio_pago == CatPagos.id)
                .order_by(desc(cls.fecha))
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return ventas
        finally:
            db.close()
    
    @classmethod
    def contar_ventas(cls):
        db = SessionLocal()
        total = db.query(cls).count()
        db.close()
        return total

    @classmethod
    def eliminar_compra(cls, compra_id):
        db = SessionLocal()
        try:
            compra = db.query(cls).filter(cls.id == compra_id).first()
            if compra:
                db.delete(compra)
                db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar la compra: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    @classmethod
    def obtener_fecha_minima(cls):
        db = SessionLocal()
        try:
            resultado = db.query(cls.fecha).order_by(cls.fecha.asc()).first()
            if resultado:
                return resultado[0]
            else:
                return date(2000, 1, 1) 
        finally:
            db.close()
    
    @classmethod
    def buscar(cls, cliente, fecha, page=1, per_page=10):
        try:
            db = SessionLocal()
            query = (
                db.query(
                    cls,
                    Cliente.nombre.label('nombre_cliente'),
                    CatPagos.nombre.label('nombre_metodo')
                )
                .join(Cliente, cls.cliente_id == Cliente.id)
                .join(CatPagos, cls.medio_pago == CatPagos.id)
            )
            if cliente:
                query = query.filter(cls.cliente_id == cliente)
            if fecha:
                query = query.filter(cls.fecha == fecha)
            resultado = (
                query
                .order_by(desc(cls.fecha))
                .offset((page - 1) * per_page)
                .limit(per_page)
                .all()
            )
            return resultado
        except Exception as e:
            print(f"Error al buscar: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def contar_buscar(cls, cliente, fecha):
        try:
            db = SessionLocal()
            query = db.query(cls)
            if cliente:
                query = query.filter(cls.cliente_id == cliente)
            if fecha:
                query = query.filter(cls.fecha == fecha)
            total = query.count()
            return total
        except Exception as e:
            print(f"Error al contar resultados: {e}")
            return 0
        finally:
            db.close()

    @classmethod
    def obtener_detalle_venta(cls, id_caja):
        from .detcaja import DetCaja
        from .extintor import Extintor
        from .lists import Capacidad, Marca, Tipo
        db = SessionLocal()
        try:
            caja_info = (
                db.query(
                    cls.id,
                    cls.fecha,
                    cls.cobro,
                    cls.adeudado,
                    cls.total,
                    cls.descripcion,
                    Cliente.nombre.label('cliente_nombre'),
                    Cliente.direccion.label('cliente_direccion'),
                    Cliente.telefono.label('cliente_telefono')
                )
                .join(Cliente, cls.cliente_id == Cliente.id)
                .filter(cls.id == id_caja)
                .first()
            )
            detalles = (
                db.query(
                    DetCaja.recarga,
                    DetCaja.nuevo,
                    DetCaja.extras,
                    DetCaja.total,
                    Extintor.numeracion,
                    Marca.nombre.label('marca_nombre'),
                    Capacidad.nombre.label('capacidad_nombre'),
                    Tipo.nombre.label('tipo_nombre')
                )
                .join(Extintor, DetCaja.id_extintor == Extintor.id)
                .join(Marca, Extintor.marca_id == Marca.id)
                .join(Capacidad, Extintor.capacidad_id == Capacidad.id)
                .join(Tipo, Extintor.tipo_id == Tipo.id)
                .filter(DetCaja.id_caja == id_caja)
                .all()
            )
            resultado = {
                'id': caja_info.id,
                'fecha': caja_info.fecha,
                'cobro': caja_info.cobro,
                'adeudado': caja_info.adeudado,
                'total': caja_info.total,
                'descripcion': caja_info.descripcion,
                'cliente': caja_info.cliente_nombre,
                'direccion': caja_info.cliente_direccion,
                'telefono': caja_info.cliente_telefono,
                'detalles': []
            }
            for detalle in detalles:
                resultado['detalles'].append({
                    'numeracion': detalle.numeracion,
                    'marca': detalle.marca_nombre,
                    'capacidad': detalle.capacidad_nombre,
                    'tipo': detalle.tipo_nombre,
                    'recarga': detalle.recarga,
                    'nuevo': detalle.nuevo,
                    'extras': detalle.extras,
                    'total': detalle.total
                })   
            return resultado
        except Exception as e:
            print(f"Error al obtener detalles de venta: {e}")
            return None
        finally:
            db.close()
    
    @classmethod
    def obtener_estado_cliente(cls, cliente_id):
        db = SessionLocal()
        try:
            resultado = (
                db.query(
                    func.sum(cls.total).label('total_compras'),
                    func.sum(cls.cobro).label('total_cobrado'),
                    func.sum(cls.adeudado).label('total_adeudado')
                )
                .filter(cls.cliente_id == cliente_id)
                .filter(Cliente.estado==True)
                .first()
            )
            
            if resultado:
                total_compras = resultado.total_compras or 0
                total_cobrado = resultado.total_cobrado or 0
                total_adeudado = resultado.total_adeudado or 0
                saldo = total_cobrado - total_compras
                return {
                    'cliente_id': cliente_id,
                    'total_compras': total_compras,
                    'total_cobrado': total_cobrado,
                    'total_adeudado': total_adeudado,
                    'saldo': saldo,
                    'estado': 'DEBE' if saldo < 0 else 'A FAVOR' if saldo > 0 else 'AL DIA'
                }
        finally:
            db.close()
    
    @classmethod
    def clientes_con_deuda(cls):
        db = SessionLocal()
        try:
            subquery = (
                db.query(
                    cls.cliente_id,
                    (func.sum(cls.total) - func.sum(cls.cobro)).label('deuda')
                )
                .group_by(cls.cliente_id)
                .having(func.sum(cls.total) - func.sum(cls.cobro) > 0)
                .subquery()
            )
            resultado = (
                db.query(Cliente.nombre, subquery.c.deuda)
                .join(subquery, Cliente.id == subquery.c.cliente_id)
                .filter(Cliente.estado==True)
                .order_by(desc(subquery.c.deuda))
                .all()
            )
            return resultado
        finally:
            db.close()

    @classmethod
    def clientes_saldo_favor(cls):
        db = SessionLocal()
        try:
            subquery = (
                db.query(
                    cls.cliente_id,
                    (func.sum(cls.cobro) - func.sum(cls.total)).label('saldo_favor')
                )
                .group_by(cls.cliente_id)
                .having(func.sum(cls.cobro) - func.sum(cls.total) > 0)
                .subquery()
            )
            resultado = (
                db.query(Cliente.nombre, subquery.c.saldo_favor)
                .join(subquery, Cliente.id == subquery.c.cliente_id)
                .filter(Cliente.estado==True)
                .order_by(desc(subquery.c.saldo_favor))
                .all()
            )
            return resultado
        finally:
            db.close()
    
    @classmethod
    def estado_financiero(cls):
        db = SessionLocal()
        try:
            totales = db.query(
                func.sum(cls.total).label('total_ventas'),
                func.sum(cls.cobro).label('total_cobros'),
                func.sum(cls.adeudado).label('total_adeudado'),
                func.count(func.distinct(cls.cliente_id)).label('clientes_activos')
            ).join(Cliente, cls.cliente_id == Cliente.id).filter(Cliente.estado==True).first()
            subquery = (
                db.query(
                    cls.cliente_id,
                    (func.sum(cls.cobro) - func.sum(cls.total)).label('saldo')
                )
                .group_by(cls.cliente_id)
                .join(Cliente, cls.cliente_id == Cliente.id)
                .filter(Cliente.estado==True)
                .subquery()
            )
            estados = db.query(
                func.sum(case((subquery.c.saldo < 0, 1), else_=0)).label('clientes_deben'),
                func.sum(case((subquery.c.saldo > 0, 1), else_=0)).label('clientes_favor'),
                func.sum(case((subquery.c.saldo == 0, 1), else_=0)).label('clientes_al_dia')
            ).select_from(subquery).first()
            return {
                'totales': {
                    'total_ventas': totales.total_ventas or 0,
                    'total_cobros': totales.total_cobros or 0,
                    'total_adeudado': totales.total_adeudado or 0,
                    'clientes_activos': totales.clientes_activos or 0
                },
                'estados': {
                    'clientes_deben': estados.clientes_deben or 0,
                    'clientes_favor': estados.clientes_favor or 0,
                    'clientes_al_dia': estados.clientes_al_dia or 0
                }
            }
        finally:
            db.close()
    
    @classmethod
    def ventas_por_mes_anual(cls, año):
        db = SessionLocal()
        try:
            resultado = (
                db.query(
                    func.strftime('%Y-%m', cls.fecha).label('mes'),
                    func.sum(cls.total).label('total_ventas_mes'),
                    func.sum(cls.cobro).label('total_cobros_mes'),
                    func.sum(cls.adeudado).label('total_adeudado_mes')
                )
                .filter(func.strftime('%Y', cls.fecha) == str(año))
                .group_by(func.strftime('%Y-%m', cls.fecha))
                .order_by(func.strftime('%Y-%m', cls.fecha))
                .all()
            )
            estadisticas_mensuales = []
            for row in resultado:
                estadisticas_mensuales.append({
                    'mes': row.mes,
                    'total_ventas': row.total_ventas_mes or 0,
                    'total_cobros': row.total_cobros_mes or 0,
                    'total_adeudado': row.total_adeudado_mes or 0
                })
            return estadisticas_mensuales
        except Exception as e:
            print(f"Error al obtener ventas por mes y año: {e}")
            return []
        finally:
            db.close()
    
    @classmethod
    def obtener_años_disponibles(cls):
        db = SessionLocal()
        try:
            resultado = (
                db.query(func.strftime('%Y', cls.fecha).label('año'))
                .distinct()
                .order_by(func.strftime('%Y', cls.fecha).desc())
                .all()
            )
            return [int(row.año) for row in resultado] if resultado else []
        except Exception as e:
            print(f"Error al obtener años disponibles: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def obtener_resumen_mensual_detallado(cls, año):
        db = SessionLocal()
        try:
            meses_completos = []
            for mes in range(1, 13):
                meses_completos.append({
                    'mes_num': mes,
                    'mes_nombre': [
                        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
                    ][mes-1],
                    'total_ventas': 0,
                    'total_cobros': 0,
                    'total_adeudado': 0,
                    'diferencia': 0,
                    'num_transacciones': 0
                })
            resultado = (
                db.query(
                    func.strftime('%m', cls.fecha).label('mes'),
                    func.sum(cls.total).label('total_ventas_mes'),
                    func.sum(cls.cobro).label('total_cobros_mes'),
                    func.sum(cls.adeudado).label('total_adeudado_mes'),
                    func.count(cls.id).label('num_transacciones')
                )
                .filter(func.strftime('%Y', cls.fecha) == str(año))
                .group_by(func.strftime('%m', cls.fecha))
                .all()
            )
            for row in resultado:
                mes_idx = int(row.mes) - 1
                if 0 <= mes_idx < 12:
                    meses_completos[mes_idx].update({
                        'total_ventas': float(row.total_ventas_mes or 0),
                        'total_cobros': float(row.total_cobros_mes or 0),
                        'total_adeudado': float(row.total_adeudado_mes or 0),
                        'diferencia': float((row.total_cobros_mes or 0) - (row.total_ventas_mes or 0)),
                        'num_transacciones': int(row.num_transacciones or 0)
                    })
            return meses_completos
        except Exception as e:
            print(f"Error al obtener resumen mensual detallado: {e}")
            return []
        finally:
            db.close()

    @classmethod
    def obtener_estadisticas_generales(cls):
        db = SessionLocal()
        try:
            totales = db.query(
                func.sum(cls.total).label('total_ventas'),
                func.sum(cls.cobro).label('total_cobros'),
                func.sum(cls.adeudado).label('total_adeudado'),
                func.count(cls.id).label('total_transacciones'),
                func.count(func.distinct(cls.cliente_id)).label('clientes_activos'),
                func.min(cls.fecha).label('fecha_primera_venta'),
                func.max(cls.fecha).label('fecha_ultima_venta')
            ).first()
            promedio_venta = (totales.total_ventas / totales.total_transacciones) if totales.total_transacciones > 0 else 0
            porcentaje_cobro = ((totales.total_cobros / totales.total_ventas) * 100) if totales.total_ventas > 0 else 0
            return {
                'total_ventas': float(totales.total_ventas or 0),
                'total_cobros': float(totales.total_cobros or 0),
                'total_adeudado': float(totales.total_adeudado or 0),
                'total_transacciones': int(totales.total_transacciones or 0),
                'clientes_activos': int(totales.clientes_activos or 0),
                'promedio_venta': float(promedio_venta),
                'porcentaje_cobro': float(porcentaje_cobro),
                'fecha_primera_venta': totales.fecha_primera_venta,
                'fecha_ultima_venta': totales.fecha_ultima_venta,
                'saldo_pendiente': float((totales.total_ventas or 0) - (totales.total_cobros or 0))
            }
        except Exception as e:
            print(f"Error al obtener estadísticas generales: {e}")
            return {}
        finally:
            db.close()

    @classmethod
    def obtener_datos_grafico_mensual(cls, año):
        datos_mensuales = cls.ventas_por_mes_anual(año)
        meses_nombres = [
            'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
            'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
        ]
        
        datos_grafico = []
        for i in range(1, 13):
            mes_str = f"{año}-{i:02d}"
            datos_mes = next((d for d in datos_mensuales if d['mes'] == mes_str), None)
            
            if datos_mes:
                datos_grafico.append({
                    'mes': meses_nombres[i-1],
                    'mes_completo': f"{meses_nombres[i-1]} {año}",
                    'ventas': datos_mes['total_ventas'],
                    'cobros': datos_mes['total_cobros'],
                    'adeudado': datos_mes['total_adeudado']
                })
            else:
                datos_grafico.append({
                    'mes': meses_nombres[i-1],
                    'mes_completo': f"{meses_nombres[i-1]} {año}",
                    'ventas': 0,
                    'cobros': 0,
                    'adeudado': 0
                })
        return datos_grafico

    @classmethod
    def obtener_comparacion_cobros_gastos(cls, año, mes=None):
        try:
            from .gastos import Gastos
            ventas_data = cls.ventas_por_mes_anual(año)
            total_cobros = 0
            if mes is None:
                for v in ventas_data:
                    total_cobros += v['total_cobros']
            else:
                mes_str = f"{año}-{mes:02d}"
                for v in ventas_data:
                    if v['mes'] == mes_str:
                        total_cobros += v['total_cobros']
                        break
            gastos_data = Gastos.gastos_por_categoria_mes(año, mes)
            total_gastos = sum(g['total_gasto'] for g in gastos_data)
            return {
                'cobros': float(total_cobros),
                'gastos': float(total_gastos)
            }
        except Exception as e:
            print(f"Error al obtener la comparación de cobros y gastos: {e}")
            return {'cobros': 0, 'gastos': 0}
    
    @classmethod
    def obtener_ingresos_por_metodo_pago(cls, año, mes=None):
        db = SessionLocal()
        try:
            query = db.query(
                CatPagos.nombre.label('medio_pago'),
                func.sum(cls.cobro).label('total_cobrado')
            ).join(CatPagos, cls.medio_pago == CatPagos.id)
            if año:
                query = query.filter(func.strftime('%Y', cls.fecha) == str(año))
            if mes:
                query = query.filter(func.strftime('%m', cls.fecha) == f"{mes:02d}")
            resultado = (
                query
                .group_by(CatPagos.nombre)
                .order_by(func.sum(cls.cobro).desc())
                .all()
            )
            ingresos_por_metodo = []
            for row in resultado:
                ingresos_por_metodo.append({
                    'medio_pago': row.medio_pago,
                    'total_cobrado': float(row.total_cobrado or 0)
                })
            return ingresos_por_metodo
        except Exception as e:
            print(f"Error al obtener ingresos por método de pago: {e}")
            return []
        finally:
            db.close()
    
    @classmethod
    def total_fecha(cls, fecha):
        db = SessionLocal()
        try:
            resultado = (
                db.query(
                    func.sum(cls.total).label('total_ventas'),
                    func.sum(cls.cobro).label('total_cobrado'),
                    func.sum(cls.adeudado).label('total_adeudado')
                )
                .filter(cls.fecha == fecha)
                .first()
            )
            if resultado.total_ventas:
                return resultado
            else:
                return None
        finally:
            db.close()