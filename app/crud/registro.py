from sqlalchemy.orm import Session
from app.models.registro import PlanoTurnoMutacion, LogCargaPlanoMutacion
from app.schemas.registro import (
    PlanoTurnoMutacionCreate,
    LogCargaPlanoMutacionCreate
)

def crear_plano_turno_mutacion(db: Session, datos: PlanoTurnoMutacionCreate) -> PlanoTurnoMutacion:
    nuevo_registro = PlanoTurnoMutacion(**datos.model_dump())
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

def obtener_planos_por_mes_ano(db: Session, mes: int, ano: int):
    return db.query(PlanoTurnoMutacion).filter(
        PlanoTurnoMutacion.mes == mes,
        PlanoTurnoMutacion.ano == ano
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
