from app.models import Cliente
from app.repositories import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()
    
    def criar_cliente(self, id, nome, telefone):
        """Cria um novo cliente"""
        try:
            cliente = Cliente(id=id, nome=nome, telefone=telefone)
            self.repository.salvar(cliente)
            return cliente
        except ValueError as e:
            raise ValueError(f"Erro ao criar cliente: {e}")
    
    def obter_cliente(self, id):
        """Obtém um cliente por ID"""
        cliente = self.repository.obter_por_id(id)
        if not cliente:
            raise ValueError(f"Cliente com ID {id} não encontrado")
        return cliente
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        return self.repository.listar_todos()
    
    def atualizar_cliente(self, id, nome=None, telefone=None):
        """Atualiza dados de um cliente"""
        cliente = self.obter_cliente(id)
        
        if nome:
            cliente._nome = nome
        if telefone:
            cliente._telefone = telefone
        
        cliente._validar()
        self.repository.atualizar(cliente)
        return cliente
    
    def deletar_cliente(self, id):
        """Deleta um cliente"""
        self.obter_cliente(id)  # Valida se existe
        self.repository.deletar(id)
    
    def contar_clientes(self):
        """Conta o número total de clientes"""
        return len(self.listar_clientes())
