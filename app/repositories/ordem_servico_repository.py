from datetime import datetime
from app.models import OrdemDeServico, StatusOrdem
from .base_repository import BaseRepository


class OrdemServicoRepository(BaseRepository):
    def __init__(self, arquivo_dados="data/ordens_servico.json"):
        super().__init__(arquivo_dados, "ordens_servico")
    
    def salvar(self, ordem):
        """Salva ou atualiza uma ordem de serviço"""
        dados = self._carregar()
        ordem_dict = {
            'id': ordem.id,
            'veiculo_id': ordem.veiculo_id,
            'cliente_id': ordem.cliente_id,
            'data_abertura': ordem.data_abertura.isoformat(),
            'data_conclusao': ordem.data_conclusao.isoformat() if ordem.data_conclusao else None,
            'status': ordem.status.value,
            'servicos_ids': [s.id for s in ordem.servicos],
            'pecas_ids': [p.id for p in ordem.pecas],
            'funcionario_id': ordem.funcionario_id,
            'observacoes': ordem.observacoes
        }
        dados[str(ordem.id)] = ordem_dict
        self._salvar(dados)
    
    def obter_por_id(self, id):
        """Obtém uma ordem de serviço por ID"""
        dados = self._carregar()
        if str(id) in dados:
            d = dados[str(id)]
            ordem = OrdemDeServico(
                id=d['id'],
                veiculo_id=d['veiculo_id'],
                cliente_id=d['cliente_id'],
                data_abertura=datetime.fromisoformat(d['data_abertura'])
            )
            
            # Restaurar status
            ordem._status = StatusOrdem(d['status'])
            
            # Restaurar data de conclusão
            if d['data_conclusao']:
                ordem._data_conclusao = datetime.fromisoformat(d['data_conclusao'])
            
            # Restaurar outros atributos
            ordem._funcionario_id = d.get('funcionario_id')
            ordem._observacoes = d.get('observacoes', '')
            
            return ordem
        return None
    
    def listar_todos(self):
        """Lista todas as ordens de serviço"""
        dados = self._carregar()
        ordens = []
        for d in dados.values():
            ordem = OrdemDeServico(
                id=d['id'],
                veiculo_id=d['veiculo_id'],
                cliente_id=d['cliente_id'],
                data_abertura=datetime.fromisoformat(d['data_abertura'])
            )
            
            # Restaurar status
            ordem._status = StatusOrdem(d['status'])
            
            # Restaurar data de conclusão
            if d['data_conclusao']:
                ordem._data_conclusao = datetime.fromisoformat(d['data_conclusao'])
            
            # Restaurar outros atributos
            ordem._funcionario_id = d.get('funcionario_id')
            ordem._observacoes = d.get('observacoes', '')
            
            ordens.append(ordem)
        return ordens
    
    def listar_por_cliente(self, cliente_id):
        """Lista todas as ordens de um cliente"""
        ordens = self.listar_todos()
        return [o for o in ordens if o.cliente_id == cliente_id]
    
    def listar_por_veiculo(self, veiculo_id):
        """Lista todas as ordens de um veículo"""
        ordens = self.listar_todos()
        return [o for o in ordens if o.veiculo_id == veiculo_id]
    
    def listar_por_status(self, status):
        """Lista todas as ordens com um status específico"""
        ordens = self.listar_todos()
        if isinstance(status, str):
            status = StatusOrdem(status)
        return [o for o in ordens if o.status == status]
    
    def listar_por_funcionario(self, funcionario_id):
        """Lista todas as ordens de um funcionário"""
        ordens = self.listar_todos()
        return [o for o in ordens if o.funcionario_id == funcionario_id]
    
    def atualizar(self, ordem):
        """Atualiza uma ordem de serviço existente"""
        if self.obter_por_id(ordem.id) is None:
            raise ValueError(f"Ordem com ID {ordem.id} não encontrada")
        self.salvar(ordem)
    
    def deletar(self, id):
        """Deleta uma ordem de serviço"""
        dados = self._carregar()
        if str(id) in dados:
            del dados[str(id)]
            self._salvar(dados)
        else:
            raise ValueError(f"Ordem com ID {id} não encontrada")
