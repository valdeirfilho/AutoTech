from app.models import Peca
from app.repositories import PecaRepository


class PecaService:
    def __init__(self):
        self.repository = PecaRepository()
    
    def criar_peca(self, id, nome, descricao, valor, quantidade_estoque):
        """Cria uma nova peça"""
        try:
            peca = Peca(id=id, nome=nome, descricao=descricao, valor=valor, quantidade_estoque=quantidade_estoque)
            self.repository.salvar(peca)
            return peca
        except ValueError as e:
            raise ValueError(f"Erro ao criar peça: {e}")
    
    def obter_peca(self, id):
        """Obtém uma peça por ID"""
        peca = self.repository.obter_por_id(id)
        if not peca:
            raise ValueError(f"Peça com ID {id} não encontrada")
        return peca
    
    def listar_pecas(self):
        """Lista todas as peças"""
        return self.repository.listar_todos()
    
    def atualizar_peca(self, id, nome=None, descricao=None, valor=None):
        """Atualiza dados de uma peça"""
        peca = self.obter_peca(id)
        
        if nome:
            peca._nome = nome
        if descricao:
            peca._descricao = descricao
        if valor is not None:
            peca._valor = valor
        
        peca._validar()
        self.repository.atualizar(peca)
        return peca
    
    def adicionar_estoque(self, id, quantidade):
        """Adiciona quantidade ao estoque de uma peça"""
        peca = self.obter_peca(id)
        peca.adicionar_ao_estoque(quantidade)
        self.repository.salvar(peca)
        return peca
    
    def remover_estoque(self, id, quantidade):
        """Remove quantidade do estoque de uma peça"""
        peca = self.obter_peca(id)
        peca.remover_do_estoque(quantidade)
        self.repository.salvar(peca)
        return peca
    
    def listar_com_estoque_baixo(self, minimo=5):
        """Lista peças com estoque abaixo do mínimo"""
        return self.repository.listar_com_estoque_baixo(minimo)
    
    def deletar_peca(self, id):
        """Deleta uma peça"""
        self.obter_peca(id)  # Valida se existe
        self.repository.deletar(id)
    
    def contar_pecas(self):
        """Conta o número total de peças"""
        return len(self.listar_pecas())
