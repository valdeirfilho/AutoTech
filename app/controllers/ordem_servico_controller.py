from app.services import OrdemServicoService


class OrdemServicoController:
    def __init__(self):
        self.service = OrdemServicoService()
    
    def criar_ordem(self, id, veiculo_id, cliente_id):
        """Cria uma nova ordem de serviço"""
        try:
            ordem = self.service.criar_ordem(id, veiculo_id, cliente_id)
            return True, f"Ordem {ordem.id} criada com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def listar_ordens(self):
        """Lista todas as ordens"""
        return self.service.listar_ordens()
    
    def listar_ordens_cliente(self, cliente_id):
        """Lista ordens de um cliente"""
        return self.service.listar_ordens_cliente(cliente_id)
    
    def listar_ordens_status(self, status):
        """Lista ordens por status"""
        try:
            return self.service.listar_ordens_status(status)
        except ValueError as e:
            return []
    
    def obter_ordem(self, id):
        """Obtém detalhes de uma ordem"""
        try:
            return self.service.obter_ordem(id)
        except ValueError as e:
            return None
    
    def adicionar_servico(self, ordem_id, servico_id):
        """Adiciona um serviço à ordem"""
        try:
            ordem = self.service.adicionar_servico(ordem_id, servico_id)
            return True, "Servico adicionado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def adicionar_peca(self, ordem_id, peca_id):
        """Adiciona uma peça à ordem"""
        try:
            ordem = self.service.adicionar_peca(ordem_id, peca_id)
            return True, "Peca adicionada com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def atribuir_funcionario(self, ordem_id, funcionario_id):
        """Atribui um funcionário à ordem"""
        try:
            self.service.atribuir_funcionario(ordem_id, funcionario_id)
            return True, "Funcionario atribuido com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def iniciar_ordem(self, ordem_id):
        """Inicia uma ordem"""
        try:
            self.service.iniciar_ordem(ordem_id)
            return True, "Ordem iniciada com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def concluir_ordem(self, ordem_id):
        """Conclui uma ordem"""
        try:
            self.service.concluir_ordem(ordem_id)
            return True, "Ordem concluida com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def cancelar_ordem(self, ordem_id):
        """Cancela uma ordem"""
        try:
            self.service.cancelar_ordem(ordem_id)
            return True, "Ordem cancelada com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def exibir_resumo_ordem(self, id):
        """Exibe um resumo da ordem"""
        try:
            ordem = self.service.obter_ordem(id)
            linhas = []
            linhas.append(f"ID: {ordem.id}")
            linhas.append(f"Status: {ordem.status.value}")
            linhas.append(f"Veiculo ID: {ordem.veiculo_id}")
            linhas.append(f"Cliente ID: {ordem.cliente_id}")
            linhas.append(f"Servicos: {len(ordem.servicos)}")
            linhas.append(f"Pecas: {len(ordem.pecas)}")
            linhas.append(f"Valor total: R$ {self.service.calcular_valor_total(id):.2f}")
            return True, "\n".join(linhas)
        except ValueError as e:
            return False, str(e)
