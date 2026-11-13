import os
import secrets


class Config:
    # Clave secreta para sesiones seguras. Se toma de la variable de entorno SECRET_KEY.
    # En desarrollo local sin variable definida, se genera una clave efímera para no usar valores fijos en el código.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # Configuración de conexión a SQL Server
    _db_driver = os.environ.get('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    _db_server = os.environ.get('DB_SERVER', r'localhost\SQLEXPRESS')
    _db_name = os.environ.get('DB_NAME', 'Automotors')
    _db_trusted = os.environ.get('DB_TRUSTED_CONNECTION', 'yes')
    _db_user = os.environ.get('DB_USER')
    _db_password = os.environ.get('DB_PASSWORD')

    if os.environ.get('DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    elif os.environ.get('SQLALCHEMY_DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    elif _db_user and _db_password:
        SQLALCHEMY_DATABASE_URI = (
            f"Driver={{{_db_driver}}};"
            f"Server={_db_server};"
            f"Database={_db_name};"
            f"Uid={_db_user};"
            f"Pwd={_db_password};"
        )
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"Driver={{{_db_driver}}};"
            f"Server={_db_server};"
            f"Database={_db_name};"
            f"Trusted_Connection={_db_trusted};"
        )
