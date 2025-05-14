from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional, List
from datetime import datetime, date


class DistribucionMutacionOut(BaseModel):
    cod_matricula: int
    max_fecha_plano: Optional[date]
    max_fecha_sap: Optional[date]
    id_zre: Optional[str]
    cod_naturaleza_juridica: Optional[str]
    naturaleza_juridica: Optional[str]
    anio: Optional[int]
    mes: Optional[int]
    id_usuario: int
    fecha_distribucion: Optional[date]

    class Config:
        model_config = ConfigDict(from_attributes=True)

class UsuarioInput(BaseModel):
    id_usuario: int

class UsuarioList(BaseModel):
    usuarios: List[UsuarioInput]

class VWComparaMutacionesBase(BaseModel):
    cod_matricula: int
    max_fecha_plano: Optional[date]
    max_fecha_sap: Optional[date]
    id_zre: Optional[str]
    cod_naturaleza_juridica: Optional[str]
    naturaleza_juridica: Optional[str]
    anio: Optional[int]
    mes: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class PaginatedComparaMutaciones(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    items: List[VWComparaMutacionesBase]

class PlanoTurnoMutacionBase(BaseModel):
    id_radicacion: str
    id_zre: str
    id_1: str
    id_2: str
    id_matricula: int
    cod_catastral: str
    cod_naturaleza_juridica: str
    naturaleza_juridica: str
    mes: int
    anio: int
    fecha_calculada: datetime


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
