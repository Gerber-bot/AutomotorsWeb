import logging
import os
from datetime import datetime
from app.db import get_db_connection
from app.repositorios.admin.backup_repository import BackupRepository

logger = logging.getLogger(__name__)


class BackupService:
    def generar_backup(self):
        conn = get_db_connection()
        if not conn: 
            return {'success': False, 'message': 'No hay conexión a la base de datos.'}
        try:
            conn.autocommit = True 
            
            backup_dir = r"C:\Backups_Automotors"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_bak = f"{backup_dir}\\Automotors_Web_{fecha_str}.bak"

            BackupRepository(conn).ejecutar_backup(archivo_bak)
            
            return {'success': True, 'message': f'¡Copia de seguridad generada con éxito! Archivo guardado en: {archivo_bak}'}
        except Exception as e:
            logger.error("Error al generar backup: %s", e)
            return {'success': False, 'message': 'Error al generar el backup (Verifique permisos de escritura de SQL Server).'}
        finally:
            conn.close()
