from sqlalchemy import text
from app.db.session import SessionLocal

def distribuir_registros(id_usuarios: list[int]):
    db = SessionLocal()
    try:
        db.execute(text("CALL sp_distribuir_mutaciones(:usuarios)"), {"usuarios": id_usuarios})
        db.commit()
    finally:
        db.close()
