# carga_mutaciones/tests/_test_db.py

import os
import sys
from dotenv import load_dotenv
import pytest

# Cargar variables desde el archivo .env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

# Añade "app/" al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from sqlalchemy import text

# Conexión a la base de datos.
def test_db_connection():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1;"))
        assert result.scalar() == 1
        print("✅ Conexión a la base de datos exitosa luego de ejecutar el test.")
    except Exception as e:
        print("❌ Fallo de conexión.")
        pytest.fail(f"No se pudo conectar a la base de datos: {e}")
    finally:
        db.close()
