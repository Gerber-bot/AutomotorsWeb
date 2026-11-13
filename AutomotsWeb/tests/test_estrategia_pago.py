import unittest

from app.strategies.estrategia_pago import (
    PagoContado,
    PagoFinanciado,
    ValidacionPagoException,
)
from app.strategies.pago_strategy_resolver import PagoStrategyResolver


class TestEstrategiaPago(unittest.TestCase):

    def test_pago_contado_valido(self):
        estrategia = PagoContado()
        data = {
            'total_venta': 15000000.0,
            'plan_cuotas': []
        }
        # No debe lanzar excepción
        estrategia.validar(data, 15000000.0)

    def test_pago_contado_monto_difiere(self):
        estrategia = PagoContado()
        data = {
            'total_venta': 14000000.0,
            'plan_cuotas': []
        }
        with self.assertRaises(ValidacionPagoException) as ctx:
            estrategia.validar(data, 15000000.0)
        self.assertIn('difiere del valor oficial', str(ctx.exception))

    def test_pago_contado_con_cuotas_invalido(self):
        estrategia = PagoContado()
        data = {
            'total_venta': 15000000.0,
            'plan_cuotas': [{'numero': 1, 'total': 15000000.0}]
        }
        with self.assertRaises(ValidacionPagoException) as ctx:
            estrategia.validar(data, 15000000.0)
        self.assertIn('No se puede registrar un plan de cuotas', str(ctx.exception))

    def test_pago_financiado_valido(self):
        estrategia = PagoFinanciado()
        data = {
            'total_venta': 20000000.0,
            'cuotas': 12,
            'entrega_inicial': 5000000.0,
            'monto_financiado': 15000000.0,
            'valor_cuota': 1500000.0,
            'tasa_interes': 20.0,
            'plan_cuotas': [{'numero': i, 'total': 1500000.0} for i in range(1, 13)]
        }
        estrategia.validar(data, 20000000.0)

    def test_pago_financiado_cuotas_invalidas(self):
        estrategia = PagoFinanciado()
        data = {
            'total_venta': 20000000.0,
            'cuotas': 1,
            'entrega_inicial': 5000000.0,
            'monto_financiado': 15000000.0,
            'valor_cuota': 1500000.0,
            'tasa_interes': 20.0,
            'plan_cuotas': [{'numero': 1}]
        }
        with self.assertRaises(ValidacionPagoException) as ctx:
            estrategia.validar(data, 20000000.0)
        self.assertIn('las cuotas deben estar entre 2 y 60', str(ctx.exception))

    def test_pago_financiado_entrega_inicial_excesiva(self):
        estrategia = PagoFinanciado()
        data = {
            'total_venta': 20000000.0,
            'cuotas': 12,
            'entrega_inicial': 25000000.0,
            'monto_financiado': 0,
            'valor_cuota': 1000.0,
            'tasa_interes': 10.0,
            'plan_cuotas': [{'numero': 1}]
        }
        with self.assertRaises(ValidacionPagoException) as ctx:
            estrategia.validar(data, 20000000.0)
        self.assertIn('no puede superar el total', str(ctx.exception))

    def test_resolver_estrategia_valida_e_invalida(self):
        resolver = PagoStrategyResolver()
        contado = resolver.obtener_estrategia('Contado')
        self.assertIsInstance(contado, PagoContado)

        financiado = resolver.obtener_estrategia('Financiado')
        self.assertIsInstance(financiado, PagoFinanciado)

        with self.assertRaises(ValueError):
            resolver.obtener_estrategia('Cripto')


if __name__ == '__main__':
    unittest.main(verbosity=2)
