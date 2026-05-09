"""Punto de entrada de la aplicación EuroCoinCollector."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes import paises, monedas, coleccion, lista_deseos, estadisticas, exportar, intercambios


def crear_app() -> FastAPI:
    """Crea y configura la instancia de FastAPI."""
    app = FastAPI(
        title="EuroCoinCollector v4",
        description="API para gestionar una colección personal de monedas de 2€",
        version="4.0.0",
    )
    _configurar_cors(app)
    _registrar_rutas(app)
    _montar_frontend(app)
    return app


def _configurar_cors(app: FastAPI) -> None:
    """Configura CORS para permitir peticiones del frontend."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _registrar_rutas(app: FastAPI) -> None:
    """Registra todos los routers de la API."""
    app.include_router(paises.router)
    app.include_router(monedas.router)
    app.include_router(coleccion.router)
    app.include_router(lista_deseos.router)
    app.include_router(estadisticas.router)
    app.include_router(exportar.router)
    app.include_router(intercambios.router)


def _montar_frontend(app: FastAPI) -> None:
    """Monta el directorio del frontend como archivos estáticos."""
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


app = crear_app()
