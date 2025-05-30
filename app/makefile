# Activa el entorno virtual (ajustar si usás otro nombre distinto a "venv")
VENV = venv/Scripts/activate

# Comando base para activar entorno en Windows CMD
ifeq ($(OS),Windows_NT)
	SHELL := cmd.exe
	.SHELLFLAGS := /C
endif

# Instalar dependencias desde requirements.txt
install:
	$(VENV) && pip install -r requirements.txt

# Ejecutar la app FastAPI con recarga automática
run:
	$(VENV) && uvicorn app.main:app --reload
	$(VENV) && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Ejecutar pruebas
test:
	$(VENV) && pytest -v

# Mostrar variables de entorno cargadas desde .env (debug)
env:
	$(VENV) && python -c "from app.core.config import settings; print(settings.model_dump())"

# Ejecutar carga de archivos .txt desde carpeta
cargar_txt:
	$(VENV) && python -c "from app.run_carga import main; main()"

# Ejecutar archivo principal run_carga.py
run_carga:
	$(VENV) python -m app.run_carga
