from datetime import datetime
from enum import Enum


class StatusOrdem(Enum):
    ABERTA = "aberta"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class OrdemDeServico:
    def __init__(self, id, veiculo_id, cliente_id, data_abertura=None):
        self._id = id
        self._veiculo_id = veiculo_id
        self._cliente_id = cliente_id
        self._data_abertura = data_abertura or datetime.now()
        self._data_conclusao = None
        self._status = StatusOrdem.ABERTA
        self._servicos = []
        self._pecas = []
        self._funcionario_id = None
        self._observacoes = ""
    
    @property
    def id(self):
        return self._id
    
    @property
    def veiculo_id(self):
        return self._veiculo_id
    
    @property
    def cliente_id(self):
        return self._cliente_id
    
    @property
    def data_abertura(self):
        return self._data_abertura
    
    @property
    def data_conclusao(self):
        return self._data_conclusao
    
    @property
    def status(self):
        return self._status
    
    @property
    def funcionario_id(self):
        return self._funcionario_id
    
    @funcionario_id.setter
    def funcionario_id(self, valor):
        self._funcionario_id = valor
    
    @property
    def observacoes(self):
        return self._observacoes
    
    @observacoes.setter
    def observacoes(self, valor):
        self._observacoes = valor
    
    @property
    def servicos(self):
        return self._servicos.copy()
    
    @property
    def pecas(self):
        return self._pecas.copy()
    
    def adicionar_servico(self, servico):
        if servico not in self._servicos:
            self._servicos.append(servico)
    
    def remover_servico(self, servico):
        if servico in self._servicos:
            self._servicos.remove(servico)
    
    def adicionar_peca(self, peca):
        if peca not in self._pecas:
            self._pecas.append(peca)
    
    def remover_peca(self, peca):
        if peca in self._pecas:
            self._pecas.remove(peca)
    
    def iniciar(self):
        if self._status != StatusOrdem.ABERTA:
            raise ValueError("Apenas ordens abertas podem ser iniciadas")
        self._status = StatusOrdem.EM_ANDAMENTO
    
    def concluir(self):
        if self._status != StatusOrdem.EM_ANDAMENTO:
            raise ValueError("Apenas ordens em andamento podem ser concluídas")
        self._status = StatusOrdem.CONCLUIDA
        self._data_conclusao = datetime.now()
    
    def cancelar(self):
        if self._status == StatusOrdem.CONCLUIDA or self._status == StatusOrdem.CANCELADA:
            raise ValueError("Ordens concluídas ou canceladas não podem ser canceladas")
        self._status = StatusOrdem.CANCELADA
    
    def calcular_valor_total(self):
        valor_servicos = sum(s.valor for s in self._servicos)
        valor_pecas = sum(p.valor for p in self._pecas)
        return valor_servicos + valor_pecas
    
    def __repr__(self):
        return f"OrdemDeServico(id={self._id}, status={self._status.value}, total=R$ {self.calcular_valor_total():.2f})"
    
    def __str__(self):
        return f"Ordem #{self._id} - {self._status.value} - R$ {self.calcular_valor_total():.2f}"
