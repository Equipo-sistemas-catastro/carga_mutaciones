# 🗂️ Proyecto: Carga de Mutaciones - Catastro

Este proyecto está desarrollado con **Python** y **FastAPI**, y forma parte de la solución del área de sistemas de catastro para la carga y procesamiento de archivos `.txt` con información de mutaciones registrales.

## 🚀 Funcionalidades principales

- API REST con FastAPI para consultas y procesamiento.
- Procesamiento automático de archivos `.txt` con estructura fija.
- Carga de datos a base de datos PostgreSQL usando SQLAlchemy.
- Validación de datos con Pydantic.
- Pruebas automáticas con `pytest`.

## 🧱 Estructura del proyecto

carga_mutaciones/
│
├── app/                        # Todo el código fuente principal
│   ├── api/                    # Rutas y versiones de la API
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── registros.py
│   │       └── __init__.py
│   │
│   ├── core/                   # Configuraciones generales y utilidades
│   │   ├── config.py
│   │   └── __init__.py
│   │
│   ├── models/                 # Modelos SQLAlchemy (tablas de la BD)
│   │   ├── registro.py
│   │   └── __init__.py
│   │
│   ├── schemas/                # Pydantic: validaciones entrada/salida
│   │   ├── registro.py
│   │   └── __init__.py
│   │
│   ├── crud/                   # Funciones CRUD para la base de datos
│   │   ├── registro.py
│   │   └── __init__.py
│   │
│   ├── services/               # Lógica de negocio (ej: procesamiento de .txt)
│   │   ├── cargar_txt.py
│   │   └── __init__.py
│   │
│   ├── db/                     # Conexión y sesión de base de datos
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── __init__.py
│   │
│   ├── main.py                 # Punto de entrada de la app FastAPI
│   └── __init__.py
│
├── tests/                      # Pruebas automáticas
│   ├── conftest.py
│   ├── test_api.py
│   └── test_cargar_txt.py
│
├── .env                        # Variables de entorno (no subir a git)
├── requirements.txt            # Lista de dependencias
├── .gitignore
└── README.md
