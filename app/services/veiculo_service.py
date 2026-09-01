from app.models import Veiculo
from app.repositories import VeiculoRepository, ClienteRepository


class VeiculoService:
    def __init__(self):
        self.repository = VeiculoRepository()
        self.cliente_repository = ClienteRepository()
    
    def criar_veiculo(self, id, placa, modelo, ano, cliente_id):
        """Cria um novo veículo e associa a um cliente"""
        try:
            # Valida se o cliente existe
            cliente = self.cliente_repository.obter_por_id(cliente_id)
            if not cliente:
                raise ValueError(f"Cliente com ID {cliente_id} não encontrado")
            
            # Valida se já existe veículo com essa placa
            existente = self.repository.obter_por_placa(placa)
            if existente:
                raise ValueError(f"Já existe um veículo com placa {placa}")
            
            veiculo = Veiculo(id=id, placa=placa, modelo=modelo, ano=ano, cliente_id=cliente_id)
            self.repository.salvar(veiculo)
            
            # Associa veículo ao cliente
            cliente.adicionar_veiculo(veiculo)
            self.cliente_repository.salvar(cliente)
            
            return veiculo
        except ValueError as e:
            raise ValueError(f"Erro ao criar veículo: {e}")
    
    def obter_veiculo(self, id):
        """Obtém um veículo por ID"""
        veiculo = self.repository.obter_por_id(id)
        if not veiculo:
            raise ValueError(f"Veículo com ID {id} não encontrado")
        return veiculo
    
    def obter_por_placa(self, placa):
        """Obtém um veículo pela placa"""
        veiculo = self.repository.obter_por_placa(placa)
        if not veiculo:
            raise ValueError(f"Veículo com placa {placa} não encontrado")
        return veiculo
    
    def listar_veiculos(self):
        """Lista todos os veículos"""
        return self.repository.listar_todos()
    
    def listar_veiculos_cliente(self, cliente_id):
        """Lista todos os veículos de um cliente"""
        cliente = self.cliente_repository.obter_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente com ID {cliente_id} não encontrado")
        return self.repository.obter_por_cliente_id(cliente_id)
    
    def atualizar_veiculo(self, id, placa=None, modelo=None, ano=None):
        """Atualiza dados de um veículo"""
        veiculo = self.obter_veiculo(id)
        
        if placa:
            veiculo._placa = placa
        if modelo:
            veiculo._modelo = modelo
        if ano:
            veiculo._ano = ano
        
        veiculo._validar()
        self.repository.atualizar(veiculo)
        return veiculo
    
    def deletar_veiculo(self, id):
        """Deleta um veículo"""
        veiculo = self.obter_veiculo(id)
        
        # Remove veículo do cliente
        cliente = self.cliente_repository.obter_por_id(veiculo.cliente_id)
        if cliente:
            cliente.remover_veiculo(veiculo)
            self.cliente_repository.salvar(cliente)
        
        self.repository.deletar(id)
    
    def contar_veiculos(self):
        """Conta o número total de veículos"""
        return len(self.listar_veiculos())
