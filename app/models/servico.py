class Servico:
    def __init__(self, id, nome, descricao, valor):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._valor = valor
        self._validar()
    
    def _validar(self):
        if not self._nome or len(self._nome.strip()) < 2:
            raise ValueError("Nome do serviço deve ter pelo menos 2 caracteres")
        if self._valor < 0:
            raise ValueError("Valor do serviço não pode ser negativo")
    
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
    
    def __repr__(self):
        return f"Servico(id={self._id}, nome='{self._nome}', valor={self._valor})"
    
    def __str__(self):
        return f"{self._nome} - R$ {self._valor:.2f}"
