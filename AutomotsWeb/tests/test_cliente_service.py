import unittest
from unittest.mock import patch, MagicMock

from app.servicios.clientes.cliente_service import ClienteService


class TestClienteService(unittest.TestCase):

    def setUp(self):
        self.servicio = ClienteService()

    @patch('app.servicios.clientes.cliente_service.ClienteRepository')
    @patch('app.servicios.clientes.cliente_service.get_db_connection')
    def test_guardar_cliente_nuevo(self, mock_get_db_connection, mock_cliente_repository):
        conn = MagicMock()
        mock_get_db_connection.return_value = conn
        repo = MagicMock()
        mock_cliente_repository.return_value = repo

        datos = {
            'dni': '35123456',
            'nombre': 'Juan',
            'apellido': 'Perez',
            'telefono': '1122334455',
            'email': 'juan.perez@example.com',
            'direccion': 'Av. Siempre Viva 742'
        }

        resultado = self.servicio.guardar_cliente(datos)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente guardado correctamente')

        repo.insertar.assert_called_once_with(datos)
        repo.actualizar.assert_not_called()
        conn.commit.assert_called_once()
        conn.close.assert_called_once()

    @patch('app.servicios.clientes.cliente_service.ClienteRepository')
    @patch('app.servicios.clientes.cliente_service.get_db_connection')
    def test_guardar_cliente_existente(self, mock_get_db_connection, mock_cliente_repository):
        conn = MagicMock()
        mock_get_db_connection.return_value = conn
        repo = MagicMock()
        mock_cliente_repository.return_value = repo

        datos = {
            'id_cliente': 5,
            'dni': '35123456',
            'nombre': 'Juan Carlos',
            'apellido': 'Perez',
            'telefono': '1122334455',
            'email': 'juan.perez@example.com',
            'direccion': 'Av. Siempre Viva 742'
        }

        resultado = self.servicio.guardar_cliente(datos)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente guardado correctamente')

        repo.actualizar.assert_called_once_with(datos)
        repo.insertar.assert_not_called()
        conn.commit.assert_called_once()
        conn.close.assert_called_once()

    @patch('app.servicios.clientes.cliente_service.ClienteRepository')
    @patch('app.servicios.clientes.cliente_service.get_db_connection')
    def test_eliminar_cliente_con_ventas_bloqueado(self, mock_get_db_connection, mock_cliente_repository):
        conn = MagicMock()
        mock_get_db_connection.return_value = conn
        repo = MagicMock()
        mock_cliente_repository.return_value = repo
        repo.contar_ventas.return_value = 2

        resultado = self.servicio.eliminar_cliente(10)
        self.assertFalse(resultado['success'])
        self.assertIn('tiene ventas registradas', resultado['message'])
        repo.eliminar.assert_not_called()
        conn.commit.assert_not_called()
        conn.close.assert_called_once()

    @patch('app.servicios.clientes.cliente_service.ClienteRepository')
    @patch('app.servicios.clientes.cliente_service.get_db_connection')
    def test_eliminar_cliente_sin_ventas_exitoso(self, mock_get_db_connection, mock_cliente_repository):
        conn = MagicMock()
        mock_get_db_connection.return_value = conn
        repo = MagicMock()
        mock_cliente_repository.return_value = repo
        repo.contar_ventas.return_value = 0

        resultado = self.servicio.eliminar_cliente(10)
        self.assertTrue(resultado['success'])
        self.assertEqual(resultado['message'], 'Cliente eliminado correctamente')
        repo.eliminar.assert_called_once_with(10)
        conn.commit.assert_called_once()
        conn.close.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
