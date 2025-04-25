from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from app.db.session import get_db
from app.models.registro import PlanoTurnoMutacion
from app.schemas.registro import PlanoTurnoMutacionOut, VWComparaMutacionesBase, PaginatedComparaMutaciones
from app.crud.registro import get_compara_mutaciones
from app.crud import registro
#from app.schemas.paginacion import CustomParams

#from fastapi_pagination import Page
from app.schemas.paginacion import CustomPage, CustomParams
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

router = APIRouter()

@router.get("/consulta_cruce_mutaciones", response_model=PaginatedComparaMutaciones)
def consultar_compara_mutaciones(
    skip: int = 0,
    limit: int = 10,
    order: str = Query("asc", regex="^(asc|desc)$"),
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    cod_matricula: Optional[int] = None,
    cod_naturaleza_juridica: Optional[str] = None,
    naturaleza_juridica: Optional[str] = None,
    db: Session = Depends(get_db),
):
    total, items = registro.get_compara_mutaciones(
        db=db,
        skip=skip,
        limit=limit,
        order=order,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        cod_matricula=cod_matricula,
        cod_naturaleza_juridica=cod_naturaleza_juridica,
        naturaleza_juridica=naturaleza_juridica 
    )   

    page = (skip // limit) + 1 if limit else 1
    pages = (total + limit - 1) // limit if limit else 1

    return {
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages,
        "items": items
    }


#@router.get("/cargamutaciones/", response_model=CustomPage[PlanoTurnoMutacionOut])
@router.get("/consulta_mutaciones/", response_model=CustomPage[PlanoTurnoMutacionOut])
def obtener_mutaciones(
    anio: Optional[int] = Query(None, description="Filtrar por año"),
    mes: Optional[int] = Query(None, description="Filtrar por mes"),
    cod_naturaleza: Optional[str] = Query(None, description="Filtrar por código de naturaleza jurídica"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$", description="Orden por año y mes"),
    params: CustomParams = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(PlanoTurnoMutacion)

    if anio:
        query = query.filter(PlanoTurnoMutacion.anio == anio)
    if mes:
        query = query.filter(PlanoTurnoMutacion.mes == mes)
    if cod_naturaleza:
        query = query.filter(PlanoTurnoMutacion.cod_naturaleza_juridica == cod_naturaleza)

    if order == "asc":
        query = query.order_by(PlanoTurnoMutacion.anio.asc(), PlanoTurnoMutacion.mes.asc())
    else:
        query = query.order_by(PlanoTurnoMutacion.anio.desc(), PlanoTurnoMutacion.mes.desc())

    return sqlalchemy_paginate(query, params)
