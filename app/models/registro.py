from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, func
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from app.core.config import settings

Base = declarative_base()

SCHEMA=settings.PG_SCHEMA

class DistribucionMutacion(Base):
    __tablename__ = "tbl_distri_mutaciones"
    __table_args__ = {"schema": SCHEMA}

    cod_matricula = Column(Integer, primary_key=True)
    max_fecha_plano = Column(Date)
    max_fecha_sap = Column(Date)
    id_zre = Column(Text)
    cod_naturaleza_juridica = Column(Text)
    naturaleza_juridica = Column(String(100))
    anio = Column(Integer)
    mes = Column(Integer)
    id_usuario = Column(Integer)
    sap_user = Column(Text)
    fecha_distribucion = Column(Date)

class VWComparaMutaciones(Base):
    __tablename__ = "vw_compara_mutaciones"
    __table_args__ = {"schema": SCHEMA}

    cod_matricula = Column(Integer, primary_key=True)
    max_fecha_plano = Column(Date)
    max_fecha_sap = Column(Date)
    id_zre = Column(String)
    cod_naturaleza_juridica = Column(String)
    naturaleza_juridica = Column(String)
    anio = Column(Integer)
    mes = Column(Integer)

class PlanoTurnoMutacion(Base):
    __tablename__ = "planos_turnos_mutaciones"
    __table_args__ = {"schema": SCHEMA}

    id_tabla = Column(Integer, primary_key=True, index=True)
    id_radicacion = Column(Text)
    id_zre = Column(Text)
    id_1 = Column(Text)
    id_2 = Column(Text)
    id_matricula = Column(Integer)
    cod_catastral = Column(Text)
    cod_naturaleza_juridica = Column(Text)
    naturaleza_juridica = Column(Text)
    mes = Column(Integer, index=True)
    anio = Column(Integer, index=True)
    fecha_calculada = Column(Date)
    fecha_procesado = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)


class LogCargaPlanoMutacion(Base):
    __tablename__ = "log_cargaplano_mutaciones"
    __table_args__ = {"schema": SCHEMA}

    id_log = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(Text, nullable=False, index=True)
    ruta_archivo = Column(Text)
    registros_leidos = Column(Text)  # Se deja como texto como en la definición
    estado = Column(Integer, index=True)
    mensaje_error = Column(Text)
    fecha_registro_log = Column(TIMESTAMP, server_default=func.now(), index=True)
