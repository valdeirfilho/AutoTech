from app.models import Cliente
from .base_repository import BaseRepository


class ClienteRepository(BaseRepository):
    def __init__(self, arquivo_dados="data/clientes.json"):
        super().__init__(arquivo_dados)
    
    def salvar(self, cliente):
        """Salva ou atualiza um cliente"""
        dados = self._carregar()
        cliente_dict = {
            'id': cliente.id,
            'nome': cliente.nome,
            'telefone': cliente.telefone,
            'veiculos_ids': [v.id for v in cliente.veiculos]
        }
        dados[str(cliente.id)] = cliente_dict
        self._salvar(dados)
    
    def obter_por_id(self, id):
        """Obtém um cliente por ID"""
        dados = self._carregar()
        if str(id) in dados:
            d = dados[str(id)]
            cliente = Cliente(id=d['id'], nome=d['nome'], telefone=d['telefone'])
            return cliente
        return None
    
    def listar_todos(self):
        """Lista todos os clientes"""
        dados = self._carregar()
        clientes = []
        for d in dados.values():
            cliente = Cliente(id=d['id'], nome=d['nome'], telefone=d['telefone'])
            clientes.append(cliente)
        return clientes
    
    def atualizar(self, cliente):
        """Atualiza um cliente existente"""
        if self.obter_por_id(cliente.id) is None:
            raise ValueError(f"Cliente com ID {cliente.id} não encontrado")
        self.salvar(cliente)
    
    def deletar(self, id):
        """Deleta um cliente"""
        dados = self._carregar()
        if str(id) in dados:
            del dados[str(id)]
            self._salvar(dados)
        else:
            raise ValueError(f"Cliente com ID {id} não encontrado")
