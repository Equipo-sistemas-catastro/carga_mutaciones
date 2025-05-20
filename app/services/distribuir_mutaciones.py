from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.config import settings

schema = settings.PG_SCHEMA

def distribuir_registros(id_usuarios: list[str]):
    db = SessionLocal()
    try:
        procedure = f'CALL {schema}.sp_distribuir_mutaciones(:usuarios)'  # Formato dinámico con el esquema
        db.execute(text(procedure), {"usuarios": id_usuarios})
        db.commit()
    finally:
        db.close()
