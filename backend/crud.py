"""Operaciones CRUD — cada función realiza una única instrucción."""

from datetime import date
from decimal import Decimal

from sqlalchemy import func, not_
from sqlalchemy.orm import Session, Query

from .models import Pais, Moneda, Coleccion, ListaDeseos, Intercambio


# ── País ──────────────────────────────────────────────────────

def obtener_todos_paises(db: Session) -> list[Pais]:
    """Devuelve todos los países."""
    return db.query(Pais).order_by(Pais.nombre).all()


# ── Moneda — Filtros individuales ─────────────────────────────

def consulta_base_monedas(db: Session) -> Query:
    """Crea la consulta base de monedas con join a pais."""
    return db.query(Moneda).join(Pais)


def filtrar_por_tipo(query: Query, tipo: str | None) -> Query:
    """Aplica filtro por tipo si se proporciona."""
    return query.filter(Moneda.tipo == tipo) if tipo else query


def filtrar_por_pais(query: Query, id_pais: int | None) -> Query:
    """Aplica filtro por país si se proporciona."""
    return query.filter(Moneda.id_pais == id_pais) if id_pais else query


def filtrar_por_anyo(query: Query, anyo: int | None) -> Query:
    """Aplica filtro por año si se proporciona."""
    return query.filter(Moneda.anyo == anyo) if anyo else query


def ejecutar_consulta_monedas(query: Query) -> list[Moneda]:
    """Ejecuta la consulta de monedas ordenada por año descendente."""
    return query.order_by(Moneda.anyo.desc()).all()


def buscar_monedas(db: Session, tipo: str | None, id_pais: int | None, anyo: int | None) -> list[Moneda]:
    """Busca monedas aplicando todos los filtros encadenados."""
    return ejecutar_consulta_monedas(
        filtrar_por_anyo(
            filtrar_por_pais(
                filtrar_por_tipo(
                    consulta_base_monedas(db), tipo
                ), id_pais
            ), anyo
        )
    )


def buscar_moneda_por_id(db: Session, id_moneda: int) -> Moneda | None:
    """Busca una moneda por su ID."""
    return db.query(Moneda).filter(Moneda.id_moneda == id_moneda).first()


# ── Colección ─────────────────────────────────────────────────




def obtener_coleccion_por_pais(db: Session, id_pais: int | None) -> list[Coleccion]:
    """Devuelve las entradas de la colección filtradas opcionalmente por país."""
    query = db.query(Coleccion).join(Moneda).filter(Coleccion.cantidad > 0)
    return query.filter(Moneda.id_pais == id_pais).all() if id_pais else query.all()


def obtener_monedas_faltantes(db: Session, id_pais: int | None) -> list[Moneda]:
    """Devuelve las monedas del catálogo que NO están en la colección."""
    ids_poseidas = db.query(Coleccion.id_moneda).filter(Coleccion.cantidad > 0).subquery()
    query = db.query(Moneda).join(Pais).filter(not_(Moneda.id_moneda.in_(ids_poseidas)))
    return query.filter(Moneda.id_pais == id_pais).order_by(Moneda.anyo.desc()).all() if id_pais else query.order_by(Moneda.anyo.desc()).all()


def buscar_entrada_coleccion(db: Session, id_moneda: int) -> Coleccion | None:
    """Busca una entrada de colección por id_moneda."""
    return db.query(Coleccion).filter(Coleccion.id_moneda == id_moneda).first()


def crear_entrada_coleccion(db: Session, id_moneda: int, cantidad: int, fecha: date | None, notas: str | None) -> Coleccion:
    """Crea una nueva entrada en la colección."""
    return guardar_en_db(db, Coleccion(id_moneda=id_moneda, cantidad=cantidad, fecha=fecha, notas=notas))


def actualizar_campos_coleccion(entrada: Coleccion, cantidad: int, fecha: date | None, notas: str | None) -> Coleccion:
    """Actualiza los campos de una entrada de colección existente."""
    entrada.cantidad = cantidad
    entrada.fecha = fecha
    entrada.notas = notas
    return entrada


def eliminar_entrada_coleccion(db: Session, entrada: Coleccion) -> None:
    """Elimina una entrada de la colección."""
    return eliminar_de_db(db, entrada)


# ── Lista de Deseos ───────────────────────────────────────────

def obtener_lista_deseos(db: Session) -> list[ListaDeseos]:
    """Devuelve toda la lista de deseos."""
    return db.query(ListaDeseos).all()


def buscar_deseo_por_moneda(db: Session, id_moneda: int) -> ListaDeseos | None:
    """Busca un deseo por id_moneda."""
    return db.query(ListaDeseos).filter(ListaDeseos.id_moneda == id_moneda).first()


def crear_deseo(db: Session, id_moneda: int, prioridad: str, notas: str | None) -> ListaDeseos:
    """Crea un nuevo deseo en la lista."""
    return guardar_en_db(db, ListaDeseos(id_moneda=id_moneda, prioridad=prioridad, notas=notas))


def eliminar_deseo(db: Session, deseo: ListaDeseos) -> None:
    """Elimina un deseo de la lista."""
    return eliminar_de_db(db, deseo)


# ── Estadísticas ──────────────────────────────────────────────

def contar_total_catalogo(db: Session) -> int:
    """Cuenta el total de monedas en el catálogo."""
    return db.query(func.count(Moneda.id_moneda)).scalar()


def contar_monedas_poseidas(db: Session) -> int:
    """Cuenta monedas distintas poseídas (cantidad > 0)."""
    return db.query(func.count(Coleccion.id_coleccion)).filter(Coleccion.cantidad > 0).scalar()


def sumar_total_cantidad(db: Session) -> int:
    """Suma total de unidades en la colección."""
    return db.query(func.coalesce(func.sum(Coleccion.cantidad), 0)).scalar()


def calcular_valor_estimado(db: Session) -> Decimal:
    """Calcula el valor total estimado de las monedas poseídas."""
    return db.query(
        func.coalesce(func.sum(Moneda.precio_mercado * Coleccion.cantidad), 0)
    ).join(Coleccion).filter(Coleccion.cantidad > 0).scalar()


def calcular_porcentaje(poseidas: int, total: int) -> float:
    """Calcula el porcentaje de la colección completada."""
    return round((poseidas / total) * 100, 2) if total > 0 else 0.0


# ── Intercambios ──────────────────────────────────────────────

def obtener_intercambios_activos(db: Session) -> list[Intercambio]:
    """Devuelve todos los intercambios con estado activo."""
    return db.query(Intercambio).filter(Intercambio.estado == "activo").order_by(Intercambio.fecha_publicacion.desc()).all()


def obtener_todos_intercambios(db: Session) -> list[Intercambio]:
    """Devuelve todos los intercambios ordenados por fecha."""
    return db.query(Intercambio).order_by(Intercambio.fecha_publicacion.desc()).all()


def buscar_intercambio_por_id(db: Session, id_intercambio: int) -> Intercambio | None:
    """Busca un intercambio por su ID."""
    return db.query(Intercambio).filter(Intercambio.id_intercambio == id_intercambio).first()


def crear_intercambio(db: Session, nombre_usuario: str, id_moneda_ofrecida: int, id_moneda_buscada: int | None, descripcion: str | None, contacto: str) -> Intercambio:
    """Crea un nuevo intercambio."""
    return guardar_en_db(db, Intercambio(
        nombre_usuario=nombre_usuario,
        id_moneda_ofrecida=id_moneda_ofrecida,
        id_moneda_buscada=id_moneda_buscada,
        descripcion=descripcion,
        contacto=contacto,
    ))


def cerrar_intercambio(intercambio: Intercambio) -> Intercambio:
    """Marca un intercambio como cerrado."""
    intercambio.estado = "cerrado"
    return intercambio


def eliminar_intercambio(db: Session, intercambio: Intercambio) -> None:
    """Elimina un intercambio."""
    return eliminar_de_db(db, intercambio)


# ── Exportar ──────────────────────────────────────────────────

def obtener_datos_exportacion(db: Session) -> list[Moneda]:
    """Obtiene todas las monedas con sus relaciones para exportar."""
    return db.query(Moneda).join(Pais).order_by(Pais.nombre, Moneda.anyo).all()


# ── Utilidades de DB ──────────────────────────────────────────

def guardar_en_db(db: Session, objeto):
    """Guarda un objeto en la base de datos y lo refresca."""
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto


def eliminar_de_db(db: Session, objeto) -> None:
    """Elimina un objeto de la base de datos."""
    db.delete(objeto)
    db.commit()
