from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PlanoTurnoMutacion(Base):
    __tablename__ = "planos_turnos_mutaciones"

    id_tabla = Column(Integer, primary_key=True, index=True)
    id_radicacion = Column(Text)
    id_zre = Column(Text)
    id_1 = Column(Text)
    id_2 = Column(Text)
    id_matricula = Column(Text)
    cod_catastral = Column(Text)
    cod_naturaleza_juridica = Column(Text)
    naturaleza_juridica = Column(Text)
    mes = Column(Integer, index=True)
    ano = Column(Integer, index=True)
    fecha_procesado = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)


class LogCargaPlanoMutacion(Base):
    __tablename__ = "log_cargaplano_mutaciones"

    id_log = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(Text, nullable=False, index=True)
    ruta_archivo = Column(Text)
    registros_leidos = Column(Text)  # Se deja como texto como en la definición
    estado = Column(Integer, index=True)
    mensaje_error = Column(Text)
    fecha_registro_log = Column(TIMESTAMP, server_default=func.now(), index=True)
