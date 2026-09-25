class Veiculo:
    def __init__(self, id, placa, modelo, ano, cliente_id):
        self._id = id
        self._placa = placa
        self._modelo = modelo
        self._ano = ano
        self._cliente_id = cliente_id
        self._ordens = []
        self._validar()
    
    def _validar(self):
        if not self._placa or len(self._placa) < 3:
            raise ValueError("Placa inválida")
        if not self._modelo or len(self._modelo.strip()) < 2:
            raise ValueError("Modelo deve ter pelo menos 2 caracteres")
        ano_atual = 2026
        if self._ano < 1900 or self._ano > ano_atual:
            raise ValueError(f"Ano deve estar entre 1900 e {ano_atual}")
    
    @property
    def id(self):
        return self._id
    
    @property
    def placa(self):
        return self._placa
    
    @placa.setter
    def placa(self, valor):
        self._placa = valor
        self._validar()
    
    @property
    def modelo(self):
        return self._modelo
    
    @modelo.setter
    def modelo(self, valor):
        self._modelo = valor
        self._validar()
    
    @property
    def ano(self):
        return self._ano
    
    @ano.setter
    def ano(self, valor):
        self._ano = valor
        self._validar()
    
    @property
    def cliente_id(self):
        return self._cliente_id
    
    @property
    def ordens(self):
        return self._ordens.copy()
    
    def adicionar_ordem(self, ordem):
        if ordem not in self._ordens:
            self._ordens.append(ordem)
    
    def __repr__(self):
        return f"Veiculo(id={self._id}, placa='{self._placa}', modelo='{self._modelo}', ano={self._ano})"
    
    def __str__(self):
        return f"{self._modelo} ({self._placa}) - {self._ano}"
