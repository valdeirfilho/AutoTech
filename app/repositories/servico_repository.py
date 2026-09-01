from app.models import Servico
from .base_repository import BaseRepository


class ServicoRepository(BaseRepository):
    def __init__(self, arquivo_dados="data/servicos.json"):
        super().__init__(arquivo_dados)
    
    def salvar(self, servico):
        """Salva ou atualiza um serviço"""
        dados = self._carregar()
        servico_dict = {
            'id': servico.id,
            'nome': servico.nome,
            'descricao': servico.descricao,
            'valor': servico.valor
        }
        dados[str(servico.id)] = servico_dict
        self._salvar(dados)
    
    def obter_por_id(self, id):
        """Obtém um serviço por ID"""
        dados = self._carregar()
        if str(id) in dados:
            d = dados[str(id)]
            servico = Servico(
                id=d['id'],
                nome=d['nome'],
                descricao=d['descricao'],
                valor=d['valor']
            )
            return servico
        return None
    
    def listar_todos(self):
        """Lista todos os serviços"""
        dados = self._carregar()
        servicos = []
        for d in dados.values():
            servico = Servico(
                id=d['id'],
                nome=d['nome'],
                descricao=d['descricao'],
                valor=d['valor']
            )
            servicos.append(servico)
        return servicos
    
    def atualizar(self, servico):
        """Atualiza um serviço existente"""
        if self.obter_por_id(servico.id) is None:
            raise ValueError(f"Serviço com ID {servico.id} não encontrado")
        self.salvar(servico)
    
    def deletar(self, id):
        """Deleta um serviço"""
        dados = self._carregar()
        if str(id) in dados:
            del dados[str(id)]
            self._salvar(dados)
        else:
            raise ValueError(f"Serviço com ID {id} não encontrado")
