# backend/app/test/test_db.py

import os
import sys
import pytest

# Añade "app/" al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from sqlalchemy import text  # <--- ¡Importante!

def test_db_connection():
    """
    Prueba que verifica que se puede abrir una conexión a la base de datos.
    """
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1;"))  # <--- Aquí usamos `text()`
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"No se pudo conectar a la base de datos: {e}")
    finally:
        db.close()
