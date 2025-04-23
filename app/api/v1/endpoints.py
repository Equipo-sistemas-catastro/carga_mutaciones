from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models.registro import PlanoTurnoMutacion
from app.schemas.registro import PlanoTurnoMutacionOut
#from app.schemas.paginacion import CustomParams

#from fastapi_pagination import Page
from app.schemas.paginacion import CustomPage, CustomParams
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

router = APIRouter()

#@router.get("/cargamutaciones/", response_model=CustomPage[PlanoTurnoMutacionOut])
@router.get("/consulta_mutaciones/", response_model=CustomPage[PlanoTurnoMutacionOut])
def obtener_mutaciones(
    ano: Optional[int] = Query(None, description="Filtrar por año"),
    mes: Optional[int] = Query(None, description="Filtrar por mes"),
    cod_naturaleza: Optional[str] = Query(None, description="Filtrar por código de naturaleza jurídica"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$", description="Orden por año y mes"),
    params: CustomParams = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(PlanoTurnoMutacion)

    if ano:
        query = query.filter(PlanoTurnoMutacion.ano == ano)
    if mes:
        query = query.filter(PlanoTurnoMutacion.mes == mes)
    if cod_naturaleza:
        query = query.filter(PlanoTurnoMutacion.cod_naturaleza_juridica == cod_naturaleza)

    if order == "asc":
        query = query.order_by(PlanoTurnoMutacion.ano.asc(), PlanoTurnoMutacion.mes.asc())
    else:
        query = query.order_by(PlanoTurnoMutacion.ano.desc(), PlanoTurnoMutacion.mes.desc())

    return sqlalchemy_paginate(query, params)
