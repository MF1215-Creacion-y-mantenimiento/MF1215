from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSeguimientoCliente(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cliente = cls.env["res.partner"].create({"name": "E1 Cliente Prueba"})
        cls.Seguimiento = cls.env["seguimiento.cliente"]

    def _crear(self, nombre):
        return self.Seguimiento.create({"name": nombre, "cliente_id": self.cliente.id})

    def test_valores_por_defecto(self):
        s = self._crear("Llamada inicial")
        self.assertEqual(s.estado, "pendiente")
        self.assertTrue(s.fecha)

    def test_boton_marcar_realizado(self):
        s = self._crear("Visita comercial")
        s.action_marcar_realizado()
        self.assertEqual(s.estado, "realizado")

    def test_no_repetir_realizado(self):
        s = self._crear("Correo de oferta")
        s.action_marcar_realizado()
        with self.assertRaises(UserError):
            s.action_marcar_realizado()

    def test_filtro_pendientes(self):
        a = self._crear("Pendiente A")
        b = self._crear("Pendiente B")
        b.action_marcar_realizado()
        pendientes = self.Seguimiento.search(
            [("cliente_id", "=", self.cliente.id), ("estado", "=", "pendiente")]
        )
        self.assertEqual(pendientes, a)
