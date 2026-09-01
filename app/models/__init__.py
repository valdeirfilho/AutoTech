from .cliente import Cliente
from .veiculo import Veiculo
from .servico import Servico
from .peca import Peca
from .funcionario import Funcionario
from .ordem_servico import OrdemDeServico, StatusOrdem

__all__ = [
    'Cliente',
    'Veiculo',
    'Servico',
    'Peca',
    'Funcionario',
    'OrdemDeServico',
    'StatusOrdem',
]
