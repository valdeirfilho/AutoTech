class Peca:
    def __init__(self, nome, valor, quantidade_estoque, id=None):
        if not nome or not nome.strip():
            raise ValueError("O nome da peça é obrigatório.")
        if valor < 0 or not isinstance(quantidade_estoque, int) or quantidade_estoque < 0:
            raise ValueError("Valor ou estoque inválido.")
        self.id = id
        self.nome = nome.strip()
        self.valor = float(valor)
        self.quantidade_estoque = quantidade_estoque

    @property
    def descricao(self):
        return self.nome

    def adicionar_ao_estoque(self, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Informe uma quantidade positiva.")
        self.quantidade_estoque += quantidade

    def remover_do_estoque(self, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Informe uma quantidade positiva.")
        if quantidade > self.quantidade_estoque:
            raise ValueError("Estoque insuficiente.")
        self.quantidade_estoque -= quantidade

    def __str__(self):
        return f"{self.nome} — R$ {self.valor:.2f} (estoque: {self.quantidade_estoque})"
