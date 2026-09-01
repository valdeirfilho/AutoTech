class Funcionario:
    def __init__(self, id, nome, cargo, telefone):
        self._id = id
        self._nome = nome
        self._cargo = cargo
        self._telefone = telefone
        self._validar()
    
    def _validar(self):
        if not self._nome or len(self._nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        if not self._cargo or len(self._cargo.strip()) < 2:
            raise ValueError("Cargo deve ter pelo menos 2 caracteres")
        if not self._telefone or len(self._telefone) < 10:
            raise ValueError("Telefone inválido")
    
    @property
    def id(self):
        return self._id
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, valor):
        self._nome = valor
        self._validar()
    
    @property
    def cargo(self):
        return self._cargo
    
    @cargo.setter
    def cargo(self, valor):
        self._cargo = valor
        self._validar()
    
    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone(self, valor):
        self._telefone = valor
        self._validar()
    
    def __repr__(self):
        return f"Funcionario(id={self._id}, nome='{self._nome}', cargo='{self._cargo}')"
    
    def __str__(self):
        return f"{self._nome} - {self._cargo}"
