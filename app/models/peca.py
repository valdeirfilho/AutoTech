class Peca:
    def __init__(self, id, nome, descricao, valor, quantidade_estoque):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._valor = valor
        self._quantidade_estoque = quantidade_estoque
        self._validar()
    
    def _validar(self):
        if not self._nome or len(self._nome.strip()) < 2:
            raise ValueError("Nome da peça deve ter pelo menos 2 caracteres")
        if self._valor < 0:
            raise ValueError("Valor da peça não pode ser negativo")
        if self._quantidade_estoque < 0:
            raise ValueError("Quantidade em estoque não pode ser negativa")
    
    @property
    def id(self):
        return self._id
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def descricao(self):
        return self._descricao
    
    @property
    def valor(self):
        return self._valor
    
    @property
    def quantidade_estoque(self):
        return self._quantidade_estoque
    
    def adicionar_ao_estoque(self, quantidade):
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self._quantidade_estoque += quantidade
    
    def remover_do_estoque(self, quantidade):
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        if quantidade > self._quantidade_estoque:
            raise ValueError("Quantidade insuficiente em estoque")
        self._quantidade_estoque -= quantidade
    
    def __repr__(self):
        return f"Peca(id={self._id}, nome='{self._nome}', valor={self._valor}, estoque={self._quantidade_estoque})"
    
    def __str__(self):
        return f"{self._nome} - R$ {self._valor:.2f} (estoque: {self._quantidade_estoque})"
