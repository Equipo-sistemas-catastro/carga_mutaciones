# run_carga.py

import os
from dotenv import load_dotenv

# Cargar .env antes de importar cualquier cosa que dependa de variables de entorno
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

from app.db.session import SessionLocal
from app.services.cargar_txt import procesar_archivos_mutaciones

# Main
def main():
    db = SessionLocal()
    try:
        procesar_archivos_mutaciones(db)
        print("✅ Proceso de carga ejecutado correctamente.")
    except Exception as e:
        print(f"❌ Error en el proceso de carga: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
