class Servico:
    def __init__(self, descricao, valor, id=None):
        if not descricao or not descricao.strip():
            raise ValueError("A descrição do serviço é obrigatória.")
        if valor < 0:
            raise ValueError("O valor não pode ser negativo.")
        self.id = id
        self.descricao = descricao.strip()
        self.valor = float(valor)

    def __str__(self):
        return f"{self.descricao} — R$ {self.valor:.2f}"
