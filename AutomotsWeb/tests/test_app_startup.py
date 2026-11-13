import unittest
from app import create_app
from config import Config


class TestAppStartup(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_config_secret_key_present_and_not_hardcoded_default(self):
        self.assertIsNotNone(Config.SECRET_KEY)
        self.assertNotEqual(Config.SECRET_KEY, 'una_clave_secreta_muy_segura')
        self.assertGreater(len(Config.SECRET_KEY), 16)

    def test_inicio_redirige_a_login_sin_sesion(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers.get('Location', ''))

    def test_login_get_ok(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Automotors', response.data)

    def test_rutas_protegidas_requieren_sesion(self):
        rutas_protegidas = [
            '/inventario/',
            '/clientes/',
            '/operaciones/ventas',
            '/operaciones/ventas/nueva',
            '/reportes/'
        ]
        for ruta in rutas_protegidas:
            with self.subTest(ruta=ruta):
                res = self.client.get(ruta)
                self.assertEqual(res.status_code, 302)
                self.assertIn('/auth/login', res.headers.get('Location', ''))

    def test_logout_limpia_sesion(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Usuario Test'
            sess['user_role'] = 'Vendedor'

        res = self.client.get('/auth/logout')
        self.assertEqual(res.status_code, 302)

        with self.client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)


if __name__ == '__main__':
    unittest.main(verbosity=2)
