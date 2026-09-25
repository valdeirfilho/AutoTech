from app.models import Veiculo
from .base_repository import BaseRepository


class VeiculoRepository(BaseRepository):
    def __init__(self, arquivo_dados="data/veiculos.json"):
        super().__init__(arquivo_dados, "veiculos")
    
    def salvar(self, veiculo):
        """Salva ou atualiza um veículo"""
        dados = self._carregar()
        veiculo_dict = {
            'id': veiculo.id,
            'placa': veiculo.placa,
            'modelo': veiculo.modelo,
            'ano': veiculo.ano,
            'cliente_id': veiculo.cliente_id,
            'ordens_ids': [o.id for o in veiculo.ordens]
        }
        dados[str(veiculo.id)] = veiculo_dict
        self._salvar(dados)
    
    def obter_por_id(self, id):
        """Obtém um veículo por ID"""
        dados = self._carregar()
        if str(id) in dados:
            d = dados[str(id)]
            veiculo = Veiculo(
                id=d['id'],
                placa=d['placa'],
                modelo=d['modelo'],
                ano=d['ano'],
                cliente_id=d['cliente_id']
            )
            return veiculo
        return None
    
    def obter_por_cliente_id(self, cliente_id):
        """Obtém todos os veículos de um cliente"""
        dados = self._carregar()
        veiculos = []
        for d in dados.values():
            if d['cliente_id'] == cliente_id:
                veiculo = Veiculo(
                    id=d['id'],
                    placa=d['placa'],
                    modelo=d['modelo'],
                    ano=d['ano'],
                    cliente_id=d['cliente_id']
                )
                veiculos.append(veiculo)
        return veiculos
    
    def listar_todos(self):
        """Lista todos os veículos"""
        dados = self._carregar()
        veiculos = []
        for d in dados.values():
            veiculo = Veiculo(
                id=d['id'],
                placa=d['placa'],
                modelo=d['modelo'],
                ano=d['ano'],
                cliente_id=d['cliente_id']
            )
            veiculos.append(veiculo)
        return veiculos
    
    def obter_por_placa(self, placa):
        """Obtém um veículo pela placa"""
        dados = self._carregar()
        for d in dados.values():
            if d['placa'] == placa:
                veiculo = Veiculo(
                    id=d['id'],
                    placa=d['placa'],
                    modelo=d['modelo'],
                    ano=d['ano'],
                    cliente_id=d['cliente_id']
                )
                return veiculo
        return None
    
    def atualizar(self, veiculo):
        """Atualiza um veículo existente"""
        if self.obter_por_id(veiculo.id) is None:
            raise ValueError(f"Veículo com ID {veiculo.id} não encontrado")
        self.salvar(veiculo)
    
    def deletar(self, id):
        """Deleta um veículo"""
        dados = self._carregar()
        if str(id) in dados:
            del dados[str(id)]
            self._salvar(dados)
        else:
            raise ValueError(f"Veículo com ID {id} não encontrado")
