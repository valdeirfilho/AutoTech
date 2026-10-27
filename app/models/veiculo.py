from datetime import date


class Veiculo:
    def __init__(self, placa, marca, modelo, ano, cliente_id, id=None):
        if not placa or not marca or not modelo:
            raise ValueError("Placa, marca e modelo são obrigatórios.")
        if not isinstance(ano, int) or not 1900 <= ano <= date.today().year + 1:
            raise ValueError("Ano do veículo inválido.")
        if cliente_id is None:
            raise ValueError("O veículo deve pertencer a um cliente.")
        self.id = id
        self.placa = placa.strip().upper()
        self.marca = marca.strip()
        self.modelo = modelo.strip()
        self.ano = ano
        self.cliente_id = cliente_id

    def __str__(self):
        return f"{self.placa} — {self.marca} {self.modelo} ({self.ano})"
