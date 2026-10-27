class Mecanico:
    def __init__(self, nome, especialidade, id=None):
        if not nome or not nome.strip() or not especialidade or not especialidade.strip():
            raise ValueError("Nome e especialidade são obrigatórios.")
        self.id = id
        self.nome = nome.strip()
        self.especialidade = especialidade.strip()

    def __str__(self):
        return f"{self.nome} — {self.especialidade}"
