from app.models import Peca
from .base_repository import BaseRepository


class PecaRepository(BaseRepository):
    def __init__(self, arquivo_dados="data/pecas.json"):
        super().__init__(arquivo_dados)
    
    def salvar(self, peca):
        """Salva ou atualiza uma peça"""
        dados = self._carregar()
        peca_dict = {
            'id': peca.id,
            'nome': peca.nome,
            'descricao': peca.descricao,
            'valor': peca.valor,
            'quantidade_estoque': peca.quantidade_estoque
        }
        dados[str(peca.id)] = peca_dict
        self._salvar(dados)
    
    def obter_por_id(self, id):
        """Obtém uma peça por ID"""
        dados = self._carregar()
        if str(id) in dados:
            d = dados[str(id)]
            peca = Peca(
                id=d['id'],
                nome=d['nome'],
                descricao=d['descricao'],
                valor=d['valor'],
                quantidade_estoque=d['quantidade_estoque']
            )
            return peca
        return None
    
    def listar_todos(self):
        """Lista todas as peças"""
        dados = self._carregar()
        pecas = []
        for d in dados.values():
            peca = Peca(
                id=d['id'],
                nome=d['nome'],
                descricao=d['descricao'],
                valor=d['valor'],
                quantidade_estoque=d['quantidade_estoque']
            )
            pecas.append(peca)
        return pecas
    
    def listar_com_estoque_baixo(self, minimo=5):
        """Lista peças com estoque abaixo do mínimo"""
        pecas = self.listar_todos()
        return [p for p in pecas if p.quantidade_estoque < minimo]
    
    def atualizar(self, peca):
        """Atualiza uma peça existente"""
        if self.obter_por_id(peca.id) is None:
            raise ValueError(f"Peça com ID {peca.id} não encontrada")
        self.salvar(peca)
    
    def deletar(self, id):
        """Deleta uma peça"""
        dados = self._carregar()
        if str(id) in dados:
            del dados[str(id)]
            self._salvar(dados)
        else:
            raise ValueError(f"Peça com ID {id} não encontrada")
