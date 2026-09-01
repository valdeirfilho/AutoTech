from .base_repository import BaseRepository
from .cliente_repository import ClienteRepository
from .veiculo_repository import VeiculoRepository
from .servico_repository import ServicoRepository
from .peca_repository import PecaRepository
from .funcionario_repository import FuncionarioRepository
from .ordem_servico_repository import OrdemServicoRepository

__all__ = [
    'BaseRepository',
    'ClienteRepository',
    'VeiculoRepository',
    'ServicoRepository',
    'PecaRepository',
    'FuncionarioRepository',
    'OrdemServicoRepository',
]
