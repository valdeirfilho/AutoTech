from app.services import VeiculoService


class VeiculoController:
    def __init__(self):
        self.service = VeiculoService()
    
    def cadastrar_veiculo(self, id, placa, modelo, ano, cliente_id):
        """Cadastra um novo veículo"""
        try:
            veiculo = self.service.criar_veiculo(id, placa, modelo, ano, cliente_id)
            return True, f"Veiculo {veiculo.modelo} ({veiculo.placa}) cadastrado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def listar_veiculos(self):
        """Lista todos os veículos"""
        return self.service.listar_veiculos()
    
    def listar_veiculos_cliente(self, cliente_id):
        """Lista veículos de um cliente"""
        try:
            return self.service.listar_veiculos_cliente(cliente_id)
        except ValueError as e:
            return []
    
    def obter_veiculo(self, id):
        """Obtém detalhes de um veículo"""
        try:
            return self.service.obter_veiculo(id)
        except ValueError as e:
            return None
    
    def obter_por_placa(self, placa):
        """Obtém um veículo pela placa"""
        try:
            return self.service.obter_por_placa(placa)
        except ValueError as e:
            return None
    
    def atualizar_veiculo(self, id, placa=None, modelo=None, ano=None):
        """Atualiza dados de um veículo"""
        try:
            veiculo = self.service.atualizar_veiculo(id, placa, modelo, ano)
            return True, "Veiculo atualizado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def deletar_veiculo(self, id):
        """Deleta um veículo"""
        try:
            veiculo = self.service.obter_veiculo(id)
            self.service.deletar_veiculo(id)
            return True, f"Veiculo {veiculo.modelo} deletado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def exibir_resumo_veiculo(self, id):
        """Exibe um resumo dos dados do veículo"""
        try:
            veiculo = self.service.obter_veiculo(id)
            linhas = []
            linhas.append(f"ID: {veiculo.id}")
            linhas.append(f"Placa: {veiculo.placa}")
            linhas.append(f"Modelo: {veiculo.modelo}")
            linhas.append(f"Ano: {veiculo.ano}")
            linhas.append(f"Ordensde servico: {len(veiculo.ordens)}")
            return True, "\n".join(linhas)
        except ValueError as e:
            return False, str(e)
