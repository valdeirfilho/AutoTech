import tempfile
import unittest
from pathlib import Path

from app.database.database import Database
from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.mecanico import Mecanico
from app.models.servico import Servico
from app.models.peca import Peca
from app.models.ordem_de_servico import OrdemDeServico, StatusOrdem
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.veiculo_repository import VeiculoRepository
from app.repositories.mecanico_repository import MecanicoRepository
from app.repositories.servico_repository import ServicoRepository
from app.repositories.peca_repository import PecaRepository
from app.repositories.ordem_de_servico_repository import OrdemDeServicoRepository


class TesteOficinaTech(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Database(str(Path(self.temp.name) / "teste.db"))
        self.db.criar_tabelas()
        self.clientes = ClienteRepository(self.db)
        self.veiculos = VeiculoRepository(self.db)
        self.mecanicos = MecanicoRepository(self.db)
        self.servicos = ServicoRepository(self.db)
        self.pecas = PecaRepository(self.db)
        self.ordens = OrdemDeServicoRepository(self.db)
        self.cliente = self.clientes.salvar(Cliente("Ana Martins", "31988887777"))
        self.veiculo = self.veiculos.salvar(Veiculo("ABC1D23", "Honda", "Civic", 2020, self.cliente.id))
        self.mecanico = self.mecanicos.salvar(Mecanico("Carlos Souza", "Mecânica geral"))
        self.s1 = self.servicos.salvar(Servico("Troca de óleo", 150))
        self.s2 = self.servicos.salvar(Servico("Alinhamento", 120))
        self.peca = self.pecas.salvar(Peca("Filtro de óleo", 45, 10))

    def tearDown(self):
        self.db.fechar()
        self.temp.cleanup()

    def test_repositories_cadastram_e_consultam(self):
        self.assertEqual(self.clientes.buscar_por_id(self.cliente.id).nome, "Ana Martins")
        self.assertEqual(self.veiculos.buscar_por_placa("ABC1D23").modelo, "Civic")
        self.assertEqual(self.mecanicos.buscar_por_id(self.mecanico.id).nome, "Carlos Souza")
        self.assertEqual(len(self.servicos.buscar_todos()), 2)
        self.assertEqual(self.pecas.buscar_por_id(self.peca.id).quantidade_estoque, 10)

    def test_os_persiste_itens_e_total(self):
        os = OrdemDeServico(self.cliente.id, self.veiculo.id, self.mecanico.id,
                            observacoes="Revisão preventiva")
        os.adicionar_servico(self.s1)
        os.adicionar_servico(self.s2)
        os.adicionar_peca(self.peca, quantidade=2)
        self.ordens.salvar(os)
        recuperada = self.ordens.buscar_por_id(os.id)
        self.assertIsNotNone(recuperada)
        self.assertEqual(len(recuperada.servicos), 2)
        self.assertEqual(len(recuperada.pecas), 1)
        self.assertEqual(recuperada.quantidades_pecas, [2])
        self.assertAlmostEqual(recuperada.calcular_total(), 360.0)

    def test_historico_preserva_valor_aplicado(self):
        os = OrdemDeServico(self.cliente.id, self.veiculo.id, self.mecanico.id)
        os.adicionar_servico(self.s1)
        self.ordens.salvar(os)
        self.s1.valor = 200
        self.servicos.salvar(self.s1)
        recuperada = self.ordens.buscar_por_id(os.id)
        self.assertAlmostEqual(recuperada.calcular_total(), 150.0)

    def test_transicao_de_status(self):
        os = OrdemDeServico(self.cliente.id, self.veiculo.id)
        os.iniciar()
        os.concluir()
        self.assertEqual(os.status, StatusOrdem.CONCLUIDA)
        with self.assertRaises(ValueError):
            os.iniciar()

    def test_busca_inexistente(self):
        self.assertIsNone(self.clientes.buscar_por_id(999))
        self.assertIsNone(self.ordens.buscar_por_id(999))


if __name__ == "__main__":
    unittest.main()
