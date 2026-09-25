from app.models import OrdemDeServico, StatusOrdem
from app.repositories import OrdemServicoRepository, ServicoRepository, PecaRepository, VeiculoRepository, ClienteRepository


class OrdemServicoService:
    def __init__(self):
        self.repository = OrdemServicoRepository()
        self.servico_repository = ServicoRepository()
        self.peca_repository = PecaRepository()
        self.veiculo_repository = VeiculoRepository()
        self.cliente_repository = ClienteRepository()
    
    def criar_ordem(self, id, veiculo_id, cliente_id):
        """Cria uma nova ordem de serviço"""
        try:
            # Valida se cliente e veículo existem
            cliente = self.cliente_repository.obter_por_id(cliente_id)
            if not cliente:
                raise ValueError(f"Cliente com ID {cliente_id} não encontrado")
            
            veiculo = self.veiculo_repository.obter_por_id(veiculo_id)
            if not veiculo:
                raise ValueError(f"Veículo com ID {veiculo_id} não encontrado")
            
            # Valida se o veículo pertence ao cliente
            if veiculo.cliente_id != cliente_id:
                raise ValueError("Veículo não pertence ao cliente informado")
            
            ordem = OrdemDeServico(id=id, veiculo_id=veiculo_id, cliente_id=cliente_id)
            self.repository.salvar(ordem)
            return ordem
        except ValueError as e:
            raise ValueError(f"Erro ao criar ordem: {e}")
    
    def obter_ordem(self, id):
        """Obtém uma ordem por ID"""
        ordem = self.repository.obter_por_id(id)
        if not ordem:
            raise ValueError(f"Ordem com ID {id} não encontrada")
        return ordem
    
    def listar_ordens(self):
        """Lista todas as ordens"""
        return self.repository.listar_todos()
    
    def listar_ordens_cliente(self, cliente_id):
        """Lista todas as ordens de um cliente"""
        self.cliente_repository.obter_por_id(cliente_id)  # Valida
        return self.repository.listar_por_cliente(cliente_id)
    
    def listar_ordens_veiculo(self, veiculo_id):
        """Lista todas as ordens de um veículo"""
        self.veiculo_repository.obter_por_id(veiculo_id)  # Valida
        return self.repository.listar_por_veiculo(veiculo_id)
    
    def listar_ordens_status(self, status):
        """Lista ordens por status"""
        if isinstance(status, str):
            try:
                status = StatusOrdem(status)
            except ValueError:
                raise ValueError(f"Status inválido: {status}")
        return self.repository.listar_por_status(status)
    
    def listar_ordens_funcionario(self, funcionario_id):
        """Lista ordens de um funcionário"""
        return self.repository.listar_por_funcionario(funcionario_id)
    
    def adicionar_servico(self, ordem_id, servico_id):
        """Adiciona um serviço a uma ordem"""
        ordem = self.obter_ordem(ordem_id)
        servico = self.servico_repository.obter_por_id(servico_id)
        
        if not servico:
            raise ValueError(f"Serviço com ID {servico_id} não encontrado")
        
        ordem.adicionar_servico(servico)
        self.repository.salvar(ordem)
        return ordem
    
    def remover_servico(self, ordem_id, servico_id):
        """Remove um serviço de uma ordem"""
        ordem = self.obter_ordem(ordem_id)
        servico = self.servico_repository.obter_por_id(servico_id)
        
        if not servico:
            raise ValueError(f"Serviço com ID {servico_id} não encontrado")
        
        ordem.remover_servico(servico)
        self.repository.salvar(ordem)
        return ordem
    
    def adicionar_peca(self, ordem_id, peca_id):
        """Adiciona uma peça a uma ordem"""
        ordem = self.obter_ordem(ordem_id)
        peca = self.peca_repository.obter_por_id(peca_id)
        
        if not peca:
            raise ValueError(f"Peça com ID {peca_id} não encontrada")
        
        if peca.quantidade_estoque <= 0:
            raise ValueError(f"Peça {peca.nome} não possui estoque disponível")
        
        ordem.adicionar_peca(peca)
        peca.remover_do_estoque(1)
        self.peca_repository.salvar(peca)
        self.repository.salvar(ordem)
        return ordem
    
    def remover_peca(self, ordem_id, peca_id):
        """Remove uma peça de uma ordem"""
        ordem = self.obter_ordem(ordem_id)
        peca = self.peca_repository.obter_por_id(peca_id)
        
        if not peca:
            raise ValueError(f"Peça com ID {peca_id} não encontrada")
        
        ordem.remover_peca(peca)
        peca.adicionar_ao_estoque(1)
        self.peca_repository.salvar(peca)
        self.repository.salvar(ordem)
        return ordem
    
    def atribuir_funcionario(self, ordem_id, funcionario_id):
        """Atribui um funcionário a uma ordem"""
        ordem = self.obter_ordem(ordem_id)
        ordem.funcionario_id = funcionario_id
        self.repository.salvar(ordem)
        return ordem
    
    def adicionar_observacao(self, ordem_id, observacao):
        """Adiciona uma observação à ordem"""
        ordem = self.obter_ordem(ordem_id)
        ordem.observacoes = observacao
        self.repository.salvar(ordem)
        return ordem
    
    def iniciar_ordem(self, ordem_id):
        """Inicia uma ordem de serviço"""
        ordem = self.obter_ordem(ordem_id)
        try:
            ordem.iniciar()
            self.repository.salvar(ordem)
            return ordem
        except ValueError as e:
            raise ValueError(f"Erro ao iniciar ordem: {e}")
    
    def concluir_ordem(self, ordem_id):
        """Conclui uma ordem de serviço"""
        ordem = self.obter_ordem(ordem_id)
        try:
            ordem.concluir()
            self.repository.salvar(ordem)
            return ordem
        except ValueError as e:
            raise ValueError(f"Erro ao concluir ordem: {e}")
    
    def cancelar_ordem(self, ordem_id):
        """Cancela uma ordem de serviço"""
        ordem = self.obter_ordem(ordem_id)
        try:
            ordem.cancelar()
            self.repository.salvar(ordem)
            
            # Devolver peças ao estoque
            for peca in ordem.pecas:
                peca_db = self.peca_repository.obter_por_id(peca.id)
                if peca_db:
                    peca_db.adicionar_ao_estoque(1)
                    self.peca_repository.salvar(peca_db)
            
            return ordem
        except ValueError as e:
            raise ValueError(f"Erro ao cancelar ordem: {e}")
    
    def calcular_valor_total(self, ordem_id):
        """Calcula o valor total de uma ordem"""
        ordem = self.obter_ordem(ordem_id)
        return ordem.calcular_valor_total()
    
    def contar_ordens(self):
        """Conta o número total de ordens"""
        return len(self.listar_ordens())
