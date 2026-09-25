from .cliente_controller import ClienteController
from .veiculo_controller import VeiculoController
from .ordem_servico_controller import OrdemServicoController
from .outros_controllers import ServicoController, PecaController, FuncionarioController

__all__ = [
    'ClienteController',
    'VeiculoController',
    'OrdemServicoController',
    'ServicoController',
    'PecaController',
    'FuncionarioController',
]
