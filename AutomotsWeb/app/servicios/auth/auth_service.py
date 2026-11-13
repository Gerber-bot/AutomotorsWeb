import hashlib
import logging
import os
from app.db import get_db_connection
from app.repositorios.auth.auth_repository import AuthRepository

logger = logging.getLogger(__name__)


class AuthService:

    def autenticar(self, usuario_input, password):
        # Acceso de desarrollo solo si está explícitamente habilitado por variables de entorno
        dev_admin_enabled = os.environ.get('ENABLE_DEV_ADMIN', 'false').lower() in ('true', '1', 't')
        dev_admin_user = os.environ.get('DEV_ADMIN_USER', 'admin')
        dev_admin_pass = os.environ.get('DEV_ADMIN_PASSWORD')

        if dev_admin_enabled and dev_admin_pass and usuario_input == dev_admin_user and password == dev_admin_pass:
            return {
                'success': True,
                'user': {
                    'id_usuario': 0,
                    'nombre': 'Admin',
                    'apellido': 'Desarrollo',
                    'rol': 'Administrador',
                },
            }

        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Error de conexión a la base de datos.'}

        try:
            repo = AuthRepository(conn)
            user = repo.buscar_usuario_activo(usuario_input)

            if user:
                password_hasheada = hashlib.sha256(password.encode('utf-8')).digest()

                if user['password_hash'] == password_hasheada:
                    return {'success': True, 'user': user}
                else:
                    return {'success': False, 'message': 'Contraseña incorrecta.'}
            else:
                return {'success': False, 'message': 'Usuario no encontrado o inactivo.'}

        except Exception as e:
            logger.error("Error al autenticar usuario %s: %s", usuario_input, e)
            return {'success': False, 'message': 'Error interno al validar credenciales.'}
        finally:
            conn.close()
