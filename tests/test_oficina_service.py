import tempfile
import unittest
from pathlib import Path

from app.database.database import Database
from app.services.oficina_service import OficinaService
from app.models.ordem_de_servico import StatusOrdem


class TestOficinaService(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.temp.name) / 'teste.db')
        self.service = OficinaService(self.db)

    def tearDown(self):
        self.db.fechar()
        self.temp.cleanup()

    def test_cadastra_cliente_veiculo_e_abre_ordem(self):
        cliente = self.service.cadastrar_cliente('Maria Silva', '(31) 99999-0000')
        veiculo = self.service.cadastrar_veiculo('ABC1D23', 'Fiat', 'Uno', 2020, cliente.id)
        mecanico = self.service.cadastrar_mecanico('João', 'Mecânica geral')
        servico = self.service.cadastrar_servico('Revisão', 180.0)
        peca = self.service.cadastrar_peca('Filtro', 35.0, 4)

        ordem = self.service.criar_ordem(
            cliente.id, veiculo.id, mecanico.id,
            'Revisão periódica', [servico.id], peca.id, 2,
        )

        self.assertEqual(ordem.status, StatusOrdem.ABERTA)
        self.assertAlmostEqual(ordem.calcular_total(), 250.0)
        self.assertEqual(self.service.ordens.buscar_por_id(ordem.id).calcular_total(), 250.0)

    def test_impede_veiculo_de_outro_cliente_na_ordem(self):
        cliente_a = self.service.cadastrar_cliente('Maria', '111')
        cliente_b = self.service.cadastrar_cliente('Pedro', '222')
        veiculo_b = self.service.cadastrar_veiculo('XYZ9Z99', 'Ford', 'Ka', 2019, cliente_b.id)

        with self.assertRaisesRegex(ValueError, 'não pertence ao cliente'):
            self.service.criar_ordem(cliente_a.id, veiculo_b.id)

    def test_transicao_de_status_da_ordem(self):
        cliente = self.service.cadastrar_cliente('Ana', '333')
        veiculo = self.service.cadastrar_veiculo('AAA1A11', 'Honda', 'Fit', 2021, cliente.id)
        ordem = self.service.criar_ordem(cliente.id, veiculo.id)

        ordem = self.service.alterar_status_ordem(ordem.id, StatusOrdem.EM_ANDAMENTO)
        self.assertEqual(ordem.status, StatusOrdem.EM_ANDAMENTO)
        ordem = self.service.alterar_status_ordem(ordem.id, StatusOrdem.CONCLUIDA)
        self.assertEqual(ordem.status, StatusOrdem.CONCLUIDA)


if __name__ == '__main__':
    unittest.main()
