import os
import shutil
import calendar
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import text

from app.schemas.registro import PlanoTurnoMutacionCreate, LogCargaPlanoMutacionCreate
from app.crud.registro import crear_plano_turno_mutacion, crear_log_carga
from app.models.registro import LogCargaPlanoMutacion, PlanoTurnoMutacion
from app.core.config import settings

CARPETA_ORIGEN = settings.CARPETA_ORIGEN_MUTACIONES
CARPETA_EXITOSO = settings.CARPETA_EXITOSO_MUTACIONES
CARPETA_FALLIDO = settings.CARPETA_FALLIDO_MUTACIONES

def extraer_mes_anio(nombre_archivo: str):
    sin_ext = os.path.splitext(nombre_archivo)[0]  # quita ".txt"
    partes = sin_ext.split('_')
    fecha_str = partes[-1]  # obtiene la parte "01-2024"
    mes_str, anio_str = fecha_str.split('-')
    return int(mes_str), int(anio_str)

def procesar_archivos_mutaciones(db: Session):
    archivos = [f for f in os.listdir(CARPETA_ORIGEN) if f.endswith(".txt")]

    for archivo in archivos:
        ruta_completa = os.path.join(CARPETA_ORIGEN, archivo)

        # Verificar si el archivo ya fue cargado exitosamente
        logs_existentes = db.query(LogCargaPlanoMutacion).filter(
            LogCargaPlanoMutacion.nombre_archivo == archivo,
            LogCargaPlanoMutacion.mensaje_error == "CARGA EXITOSA"
        ).first()

        if logs_existentes:
            # Archivo duplicado
            shutil.move(ruta_completa, os.path.join(CARPETA_FALLIDO, archivo))
            crear_log_carga(db, LogCargaPlanoMutacionCreate(
                nombre_archivo=archivo,
                ruta_archivo=ruta_completa,
                registros_leidos="0",
                estado=0,
                mensaje_error="ARCHIVO DUPLICADO"
            ))
            continue

        try:
            with open(ruta_completa, encoding="utf-8") as f:
                lineas = f.readlines()[3:]  # Omitir las primeras 3 líneas

            mes, anio = extraer_mes_anio(archivo)
            #registros_creados = 0
            registros = []

            """
            for linea in lineas:
                campos = {
                    "id_radicacion": linea[0:15].strip(),
                    "id_zre": linea[16:22].strip(),
                    "id_1": linea[23:26].strip(),
                    "id_2": linea[27:29].strip(),
                    "id_matricula": linea[30:45].strip(),
                    "cod_catastral": linea[46:76].strip(),
                }
                split_nat = linea[77:398].split('-', 1)
                campos["cod_naturaleza_juridica"] = split_nat[0].strip()
                campos["naturaleza_juridica"] = split_nat[1].strip() if len(split_nat) > 1 else ""
                campos["mes"] = mes
                campos["ano"] = ano
                """
            
            for linea in lineas:
                campos = {
                    "id_radicacion": linea[0:15].strip(),
                    "id_zre": linea[16:22].strip(),
                    "id_1": linea[23:26].strip(),
                    "id_2": linea[27:29].strip(),
                }
                split_matricula = linea[30:45].split('-', 1)
                campos["id_matricula"] = split_matricula[1].strip() if len(split_matricula) > 1 else ""
                campos["cod_catastral"] = linea[46:76].strip()
                split_nat = linea[77:398].split('-', 1)
                campos["cod_naturaleza_juridica"] = split_nat[0].strip()
                campos["naturaleza_juridica"] = split_nat[1].strip() if len(split_nat) > 1 else ""
                campos["mes"] = mes
                campos["anio"] = anio

                # Calcular último día del mes
                ultimo_dia = calendar.monthrange(int(anio), int(mes))[1]
                fecha_calculada = datetime(int(anio), int(mes), ultimo_dia).date()
                campos["fecha_calculada"] = fecha_calculada

                #crear_plano_turno_mutacion(db, PlanoTurnoMutacionCreate(**campos))
                #registros_creados += 1
                registros.append(PlanoTurnoMutacion(**campos))

            db.bulk_save_objects(registros)
            db.commit()

            # 🔄 Refrescar la vista materializada
            db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY vw_compara_mutaciones;"))
            db.commit()
            
            shutil.move(ruta_completa, os.path.join(CARPETA_EXITOSO, archivo))
            crear_log_carga(db, LogCargaPlanoMutacionCreate(
                nombre_archivo=archivo,
                ruta_archivo=ruta_completa,
                #registros_leidos=str(registros_creados),
                registros_leidos=str(len(registros)),
                estado=1,
                mensaje_error="CARGA EXITOSA"
            ))

        except Exception as e:
            shutil.move(ruta_completa, os.path.join(CARPETA_FALLIDO, archivo))
            crear_log_carga(db, LogCargaPlanoMutacionCreate(
                nombre_archivo=archivo,
                ruta_archivo=ruta_completa,
                registros_leidos="0",
                estado=0,
                mensaje_error=f"ERROR DE CARGA: {str(e)}"
            ))