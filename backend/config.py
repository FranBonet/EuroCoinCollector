"""Configuración de la aplicación."""

from os import getenv


def get_database_url() -> str:
    """Devuelve la URL de conexión a la base de datos."""
    return getenv(
        "DATABASE_URL",
        "mysql+pymysql://eurocoleccion_user:eurocoleccion_pass@db:3306/eurocoleccion?charset=utf8mb4"
    )
