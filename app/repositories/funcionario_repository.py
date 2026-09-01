from app.models import Funcionario
from .base_repository import BaseRepository


class FuncionarioRepository(BaseRepository):
    def __init__(self, arquivo_dados="data/funcionarios.json"):
        super().__init__(arquivo_dados, "funcionarios")
    
    def salvar(self, funcionario):
        """Salva ou atualiza um funcionário"""
        dados = self._carregar()
        funcionario_dict = {
            'id': funcionario.id,
            'nome': funcionario.nome,
            'cargo': funcionario.cargo,
            'telefone': funcionario.telefone
        }
        dados[str(funcionario.id)] = funcionario_dict
        self._salvar(dados)
    
    def obter_por_id(self, id):
        """Obtém um funcionário por ID"""
        dados = self._carregar()
        if str(id) in dados:
            d = dados[str(id)]
            funcionario = Funcionario(
                id=d['id'],
                nome=d['nome'],
                cargo=d['cargo'],
                telefone=d['telefone']
            )
            return funcionario
        return None
    
    def listar_todos(self):
        """Lista todos os funcionários"""
        dados = self._carregar()
        funcionarios = []
        for d in dados.values():
            funcionario = Funcionario(
                id=d['id'],
                nome=d['nome'],
                cargo=d['cargo'],
                telefone=d['telefone']
            )
            funcionarios.append(funcionario)
        return funcionarios
    
    def listar_por_cargo(self, cargo):
        """Lista todos os funcionários de um cargo específico"""
        dados = self._carregar()
        funcionarios = []
        for d in dados.values():
            if d['cargo'].lower() == cargo.lower():
                funcionario = Funcionario(
                    id=d['id'],
                    nome=d['nome'],
                    cargo=d['cargo'],
                    telefone=d['telefone']
                )
                funcionarios.append(funcionario)
        return funcionarios
    
    def atualizar(self, funcionario):
        """Atualiza um funcionário existente"""
        if self.obter_por_id(funcionario.id) is None:
            raise ValueError(f"Funcionário com ID {funcionario.id} não encontrado")
        self.salvar(funcionario)
    
    def deletar(self, id):
        """Deleta um funcionário"""
        dados = self._carregar()
        if str(id) in dados:
            del dados[str(id)]
            self._salvar(dados)
        else:
            raise ValueError(f"Funcionário com ID {id} não encontrado")
