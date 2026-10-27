class Cliente:
    def __init__(self, nome, telefone, id=None):
        if not nome or not nome.strip():
            raise ValueError("O nome do cliente é obrigatório.")
        if not telefone or not telefone.strip():
            raise ValueError("O telefone é obrigatório.")
        self.id = id
        self.nome = nome.strip()
        self.telefone = telefone.strip()

    def __str__(self):
        return f"{self.id or 'Novo'} - {self.nome} ({self.telefone})"
