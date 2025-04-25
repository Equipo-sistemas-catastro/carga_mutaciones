from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import List, Optional, Tuple
from datetime import date

from app.models.registro import PlanoTurnoMutacion, LogCargaPlanoMutacion,VWComparaMutaciones
from app.schemas.registro import (
    PlanoTurnoMutacionCreate,
    LogCargaPlanoMutacionCreate
)

def get_compara_mutaciones(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    order: str = "asc",
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    cod_matricula: Optional[int] = None,
    cod_naturaleza_juridica: Optional[str] = None,
    naturaleza_juridica: Optional[str] = None,
) -> Tuple[int, List[VWComparaMutaciones]]:

    query = db.query(VWComparaMutaciones)

    if fecha_desde:
        query = query.filter(VWComparaMutaciones.max_fecha_plano >= fecha_desde)
    if fecha_hasta:
        query = query.filter(VWComparaMutaciones.max_fecha_plano <= fecha_hasta)
    if cod_matricula:
        query = query.filter(VWComparaMutaciones.cod_matricula == cod_matricula)
    if cod_naturaleza_juridica:
        query = query.filter(VWComparaMutaciones.cod_naturaleza_juridica == cod_naturaleza_juridica)
    if naturaleza_juridica:
        query = query.filter(VWComparaMutaciones.naturaleza_juridica == naturaleza_juridica)

    total = query.count()

    ordering = asc(VWComparaMutaciones.max_fecha_plano) if order == "asc" else desc(VWComparaMutaciones.max_fecha_plano)
    items = query.order_by(ordering).offset(skip).limit(limit).all()

    return total, items

def crear_plano_turno_mutacion(db: Session, datos: PlanoTurnoMutacionCreate) -> PlanoTurnoMutacion:
    nuevo_registro = PlanoTurnoMutacion(**datos.model_dump())
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

def obtener_planos_por_mes_anio(db: Session, mes: int, anio: int):
    return db.query(PlanoTurnoMutacion).filter(
        PlanoTurnoMutacion.mes == mes,
        PlanoTurnoMutacion.anio == anio
    ).all()

def crear_log_carga(db: Session, log_data: LogCargaPlanoMutacionCreate) -> LogCargaPlanoMutacion:
    nuevo_log = LogCargaPlanoMutacion(**log_data.model_dump())
    db.add(nuevo_log)
    db.commit()
    db.refresh(nuevo_log)
    return nuevo_log

def obtener_logs_por_estado(db: Session, estado: int):
    return db.query(LogCargaPlanoMutacion).filter(
        LogCargaPlanoMutacion.estado == estado
    ).all()
