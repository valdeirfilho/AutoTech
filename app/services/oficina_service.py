"""Casos de uso compartilhados pelas interfaces do AutoTech."""
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


class OficinaService:
    """Fachada de aplicação para não colocar regras de negócio nas telas."""

    def __init__(self, database):
        self.database = database
        self.clientes = ClienteRepository(database)
        self.veiculos = VeiculoRepository(database)
        self.mecanicos = MecanicoRepository(database)
        self.servicos = ServicoRepository(database)
        self.pecas = PecaRepository(database)
        self.ordens = OrdemDeServicoRepository(database)
        self.database.criar_tabelas()

    def cadastrar_cliente(self, nome, telefone, id=None):
        return self.clientes.salvar(Cliente(nome, telefone, id))

    def cadastrar_veiculo(self, placa, marca, modelo, ano, cliente_id, id=None):
        cliente = self.clientes.buscar_por_id(int(cliente_id))
        if cliente is None:
            raise ValueError("Selecione um cliente existente.")
        veiculo = Veiculo(placa, marca, modelo, int(ano), cliente.id, id)
        return self.veiculos.salvar(veiculo)

    def cadastrar_mecanico(self, nome, especialidade, id=None):
        return self.mecanicos.salvar(Mecanico(nome, especialidade, id))

    def cadastrar_servico(self, descricao, valor, id=None):
        return self.servicos.salvar(Servico(descricao, float(valor), id))

    def cadastrar_peca(self, nome, valor, quantidade_estoque, id=None):
        return self.pecas.salvar(Peca(nome, float(valor), int(quantidade_estoque), id))

    def criar_ordem(self, cliente_id, veiculo_id, mecanico_id=None,
                    observacoes="", servico_ids=None, peca_id=None,
                    quantidade_peca=1):
        cliente_id, veiculo_id = int(cliente_id), int(veiculo_id)
        veiculo = self.veiculos.buscar_por_id(veiculo_id)
        if veiculo is None:
            raise ValueError("Selecione um veículo existente.")
        if veiculo.cliente_id != cliente_id:
            raise ValueError("O veículo selecionado não pertence ao cliente escolhido.")
        mecanico_id = int(mecanico_id) if mecanico_id not in (None, "") else None
        if mecanico_id is not None and self.mecanicos.buscar_por_id(mecanico_id) is None:
            raise ValueError("O mecânico selecionado não existe.")

        ordem = OrdemDeServico(cliente_id, veiculo_id, mecanico_id,
                               observacoes=observacoes)
        for servico_id in (servico_ids or []):
            servico = self.servicos.buscar_por_id(int(servico_id))
            if servico is None:
                raise ValueError(f"Serviço {servico_id} não encontrado.")
            ordem.adicionar_servico(servico)
        if peca_id not in (None, ""):
            peca = self.pecas.buscar_por_id(int(peca_id))
            if peca is None:
                raise ValueError("A peça selecionada não existe.")
            quantidade_peca = int(quantidade_peca)
            if quantidade_peca > peca.quantidade_estoque:
                raise ValueError("Quantidade solicitada maior que o estoque disponível.")
            ordem.adicionar_peca(peca, quantidade_peca)
        return self.ordens.salvar(ordem)

    def alterar_status_ordem(self, ordem_id, novo_status):
        ordem = self.ordens.buscar_por_id(int(ordem_id))
        if ordem is None:
            raise ValueError("Ordem de serviço não encontrada.")
        acoes = {
            StatusOrdem.EM_ANDAMENTO: ordem.iniciar,
            StatusOrdem.CONCLUIDA: ordem.concluir,
            StatusOrdem.CANCELADA: ordem.cancelar,
        }
        status = novo_status if isinstance(novo_status, StatusOrdem) else StatusOrdem(novo_status)
        if status not in acoes:
            raise ValueError("Transição de status não permitida.")
        acoes[status]()
        return self.ordens.salvar(ordem)

    def resumo(self):
        ordens = self.ordens.buscar_todos()
        return {
            "clientes": len(self.clientes.buscar_todos()),
            "veiculos": len(self.veiculos.buscar_todos()),
            "mecanicos": len(self.mecanicos.buscar_todos()),
            "pecas": len(self.pecas.buscar_todos()),
            "ordens_abertas": sum(o.status in (StatusOrdem.ABERTA, StatusOrdem.EM_ANDAMENTO) for o in ordens),
            "ordens": len(ordens),
        }
