from app.models import Servico
from app.repositories import ServicoRepository


class ServicoService:
    def __init__(self):
        self.repository = ServicoRepository()
    
    def criar_servico(self, id, nome, descricao, valor):
        """Cria um novo serviço"""
        try:
            servico = Servico(id=id, nome=nome, descricao=descricao, valor=valor)
            self.repository.salvar(servico)
            return servico
        except ValueError as e:
            raise ValueError(f"Erro ao criar serviço: {e}")
    
    def obter_servico(self, id):
        """Obtém um serviço por ID"""
        servico = self.repository.obter_por_id(id)
        if not servico:
            raise ValueError(f"Serviço com ID {id} não encontrado")
        return servico
    
    def listar_servicos(self):
        """Lista todos os serviços"""
        return self.repository.listar_todos()
    
    def atualizar_servico(self, id, nome=None, descricao=None, valor=None):
        """Atualiza dados de um serviço"""
        servico = self.obter_servico(id)
        
        if nome:
            servico._nome = nome
        if descricao:
            servico._descricao = descricao
        if valor is not None:
            servico._valor = valor
        
        servico._validar()
        self.repository.atualizar(servico)
        return servico
    
    def deletar_servico(self, id):
        """Deleta um serviço"""
        self.obter_servico(id)  # Valida se existe
        self.repository.deletar(id)
    
    def contar_servicos(self):
        """Conta o número total de serviços"""
        return len(self.listar_servicos())
