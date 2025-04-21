# backend/tests/test_cargar_txt.py

from app.services.cargar_txt import procesar_archivos_mutaciones
from app.db.session import SessionLocal

def test_procesar_archivos():
    db = SessionLocal()
    try:
        procesar_archivos_mutaciones(db)
    except Exception as e:
        assert False, f"Error al procesar archivos: {e}"
    finally:
        db.close()
