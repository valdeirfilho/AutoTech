from app.models import Funcionario
from app.repositories import FuncionarioRepository


class FuncionarioService:
    def __init__(self):
        self.repository = FuncionarioRepository()
    
    def criar_funcionario(self, id, nome, cargo, telefone):
        """Cria um novo funcionário"""
        try:
            funcionario = Funcionario(id=id, nome=nome, cargo=cargo, telefone=telefone)
            self.repository.salvar(funcionario)
            return funcionario
        except ValueError as e:
            raise ValueError(f"Erro ao criar funcionário: {e}")
    
    def obter_funcionario(self, id):
        """Obtém um funcionário por ID"""
        funcionario = self.repository.obter_por_id(id)
        if not funcionario:
            raise ValueError(f"Funcionário com ID {id} não encontrado")
        return funcionario
    
    def listar_funcionarios(self):
        """Lista todos os funcionários"""
        return self.repository.listar_todos()
    
    def listar_mecanicos(self):
        """Lista todos os mecânicos"""
        return self.repository.listar_por_cargo("Mecânico")
    
    def listar_por_cargo(self, cargo):
        """Lista funcionários por cargo"""
        return self.repository.listar_por_cargo(cargo)
    
    def atualizar_funcionario(self, id, nome=None, cargo=None, telefone=None):
        """Atualiza dados de um funcionário"""
        funcionario = self.obter_funcionario(id)
        
        if nome:
            funcionario._nome = nome
        if cargo:
            funcionario._cargo = cargo
        if telefone:
            funcionario._telefone = telefone
        
        funcionario._validar()
        self.repository.atualizar(funcionario)
        return funcionario
    
    def deletar_funcionario(self, id):
        """Deleta um funcionário"""
        self.obter_funcionario(id)  # Valida se existe
        self.repository.deletar(id)
    
    def contar_funcionarios(self):
        """Conta o número total de funcionários"""
        return len(self.listar_funcionarios())
