from enum import Enum


class StatusOrdem(Enum):
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"


class OrdemDeServico:
    def __init__(self, cliente_id, veiculo_id, mecanico_id=None, id=None,
                 status=StatusOrdem.ABERTA, observacoes=""):
        if cliente_id is None or veiculo_id is None:
            raise ValueError("A OS precisa de cliente e veículo.")
        self.id = id
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id
        self.mecanico_id = mecanico_id
        self.status = status if isinstance(status, StatusOrdem) else StatusOrdem(status)
        self.observacoes = observacoes or ""
        self.servicos, self.valores_servicos = [], []
        self.pecas, self.quantidades_pecas, self.valores_pecas = [], [], []

    def _validar_editavel(self):
        if self.status in (StatusOrdem.CONCLUIDA, StatusOrdem.CANCELADA):
            raise ValueError("OS concluída/cancelada não pode receber itens.")

    def adicionar_servico(self, servico, valor_aplicado=None):
        self._validar_editavel()
        if servico.id is None:
            raise ValueError("Salve o serviço antes de associá-lo à OS.")
        valor = servico.valor if valor_aplicado is None else float(valor_aplicado)
        if valor < 0:
            raise ValueError("Valor inválido.")
        self.servicos.append(servico)
        self.valores_servicos.append(valor)

    def adicionar_peca(self, peca, quantidade=1, valor_unitario=None):
        self._validar_editavel()
        if peca.id is None:
            raise ValueError("Salve a peça antes de associá-la à OS.")
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("A quantidade deve ser positiva.")
        valor = peca.valor if valor_unitario is None else float(valor_unitario)
        if valor < 0:
            raise ValueError("Valor unitário inválido.")
        self.pecas.append(peca)
        self.quantidades_pecas.append(quantidade)
        self.valores_pecas.append(valor)

    def calcular_total_servicos(self):
        return sum(self.valores_servicos)

    def calcular_total_pecas(self):
        return sum(v * q for v, q in zip(self.valores_pecas, self.quantidades_pecas))

    def calcular_total(self):
        return self.calcular_total_servicos() + self.calcular_total_pecas()

    def iniciar(self):
        if self.status != StatusOrdem.ABERTA:
            raise ValueError("Apenas OS aberta pode ser iniciada.")
        self.status = StatusOrdem.EM_ANDAMENTO

    def concluir(self):
        if self.status != StatusOrdem.EM_ANDAMENTO:
            raise ValueError("Apenas OS em andamento pode ser concluída.")
        self.status = StatusOrdem.CONCLUIDA

    def cancelar(self):
        if self.status not in (StatusOrdem.ABERTA, StatusOrdem.EM_ANDAMENTO):
            raise ValueError("Apenas OS aberta/em andamento pode ser cancelada.")
        self.status = StatusOrdem.CANCELADA

    def __str__(self):
        return f"OS {self.id or 'NOVA'} | Status: {self.status.value} | Total: R$ {self.calcular_total():.2f}"
