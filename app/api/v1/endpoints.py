from fastapi import APIRouter, Depends, Query, Header, HTTPException, Security
from app.core.security import validate_api_key
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from app.services.distribuir_mutaciones import distribuir_registros
from app.services.post_distribucion import generar_csvs_y_enviar
from app.schemas.registro import UsuarioUUID

from app.db.session import get_db
from app.models.registro import PlanoTurnoMutacion, DistribucionMutacion, vw_distribucion_aplicados, vw_aplicados_agrupados, ConsultaDistriMutaciones
from app.schemas.registro import PlanoTurnoMutacionOut, VWComparaMutacionesBase, PaginatedComparaMutaciones, UsuarioList, DistribucionMutacionOut, vw_distribucion_aplicadosOut, vw_aplicados_agrupadosOut, ConsultaDistriMutacionesOut
from app.crud.registro import get_compara_mutaciones
from app.crud import registro
#from app.schemas.paginacion import CustomParams

#from fastapi_pagination import Page
from app.schemas.paginacion import CustomPage, CustomParams
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate

router = APIRouter()

@router.get("/consulta_aplicados_agrupados", response_model=CustomPage[vw_aplicados_agrupadosOut])
def consulta_aplicados_agrupados(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(vw_aplicados_agrupados)
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit else 1
    pages = (total + limit - 1) // limit if limit else 1

    return {
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages,
        "items": items
    }

@router.get("/consulta_aplicados", response_model=CustomPage[vw_distribucion_aplicadosOut])
def consulta_aplicados(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(vw_distribucion_aplicados)
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit else 1
    pages = (total + limit - 1) // limit if limit else 1

    return {
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages,
        "items": items
    }

@router.get("/consulta_distribucion_mutaciones", response_model=CustomPage[ConsultaDistriMutacionesOut])
def consultar_distribucion_mutaciones(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(ConsultaDistriMutaciones)
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit else 1
    pages = (total + limit - 1) // limit if limit else 1

    return {
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages,
        "items": items
    }

# 👇 Llamado al SP de la BD para distribuir las mutaciones a los usuarios
@router.post("/distribuir_mutaciones")
def distribuir_mutaciones(payload: List[UsuarioUUID]):
    try:
        id_usuarios = [str(u.id_user) for u in payload]
        distribuir_registros(id_usuarios)  # Ejecuta el SP
        generar_csvs_y_enviar(id_usuarios)  # Genera y envía CSVs
        return {"msg": "Registros distribuidos y correos enviados correctamente"}
    except Exception as e:
        print("ERROR EJECUCIÓN:", e)              # DEBUG CONCRETO
        raise HTTPException(status_code=500, detail=str(e))



# 👇 Llamado de la API con token de seguridad
#@router.get("/consulta_cruce_mutaciones", response_model=PaginatedComparaMutaciones, dependencies=[Depends(validate_api_key)])
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

