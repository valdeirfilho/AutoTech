from app.services import ServicoService, PecaService, FuncionarioService


class ServicoController:
    def __init__(self):
        self.service = ServicoService()
    
    def cadastrar_servico(self, id, nome, descricao, valor):
        try:
            self.service.criar_servico(id, nome, descricao, valor)
            return True, f"Servico {nome} cadastrado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def listar_servicos(self):
        return self.service.listar_servicos()
    
    def obter_servico(self, id):
        try:
            return self.service.obter_servico(id)
        except ValueError:
            return None


class PecaController:
    def __init__(self):
        self.service = PecaService()
    
    def cadastrar_peca(self, id, nome, descricao, valor, quantidade_estoque):
        try:
            self.service.criar_peca(id, nome, descricao, valor, quantidade_estoque)
            return True, f"Peca {nome} cadastrada com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def listar_pecas(self):
        return self.service.listar_pecas()
    
    def obter_peca(self, id):
        try:
            return self.service.obter_peca(id)
        except ValueError:
            return None
    
    def listar_com_estoque_baixo(self, minimo=5):
        return self.service.listar_com_estoque_baixo(minimo)


class FuncionarioController:
    def __init__(self):
        self.service = FuncionarioService()
    
    def cadastrar_funcionario(self, id, nome, cargo, telefone):
        try:
            self.service.criar_funcionario(id, nome, cargo, telefone)
            return True, f"Funcionario {nome} cadastrado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def listar_funcionarios(self):
        return self.service.listar_funcionarios()
    
    def listar_mecanicos(self):
        return self.service.listar_mecanicos()
    
    def obter_funcionario(self, id):
        try:
            return self.service.obter_funcionario(id)
        except ValueError:
            return None
