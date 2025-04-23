from app.db.session import SessionLocal
from app.services.cargar_txt import procesar_archivos_mutaciones

#main
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