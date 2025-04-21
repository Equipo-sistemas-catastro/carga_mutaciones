from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime


class PlanoTurnoMutacionBase(BaseModel):
    id_radicacion: str
    id_zre: str
    id_1: str
    id_2: str
    id_matricula: str
    cod_catastral: str
    cod_naturaleza_juridica: str
    naturaleza_juridica: str
    mes: int
    ano: int


class PlanoTurnoMutacionCreate(PlanoTurnoMutacionBase):
    pass


class PlanoTurnoMutacionOut(PlanoTurnoMutacionBase):
    id_tabla: int
    fecha_procesado: datetime

    model_config = ConfigDict(from_attributes=True)


class LogCargaPlanoMutacionBase(BaseModel):
    nombre_archivo: str
    ruta_archivo: Optional[str] = None
    registros_leidos: str
    estado: int
    mensaje_error: Optional[str] = None


class LogCargaPlanoMutacionCreate(LogCargaPlanoMutacionBase):
    pass


class LogCargaPlanoMutacionOut(LogCargaPlanoMutacionBase):
    id_log: int
    fecha_registro_log: datetime

    #class Config:
    #    from_attributes = True
    model_config = ConfigDict(from_attributes=True)
