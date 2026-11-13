import logging
import pyodbc
from config import Config

logger = logging.getLogger(__name__)


def get_db_connection():
    try:
        conn = pyodbc.connect(Config.SQLALCHEMY_DATABASE_URI)
        return conn
    except Exception as e:
        logger.error("Error al conectar con la base de datos: %s", e)
        return None
