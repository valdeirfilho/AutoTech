from app.services import ClienteService


class ClienteController:
    def __init__(self):
        self.service = ClienteService()
    
    def cadastrar_cliente(self, id, nome, telefone):
        """Cadastra um novo cliente"""
        try:
            cliente = self.service.criar_cliente(id, nome, telefone)
            return True, f"Cliente {cliente.nome} cadastrado com sucesso (ID: {cliente.id})"
        except ValueError as e:
            return False, str(e)
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        clientes = self.service.listar_clientes()
        return clientes
    
    def obter_cliente(self, id):
        """Obtém detalhes de um cliente"""
        try:
            return self.service.obter_cliente(id)
        except ValueError as e:
            return None
    
    def atualizar_cliente(self, id, nome=None, telefone=None):
        """Atualiza dados de um cliente"""
        try:
            cliente = self.service.atualizar_cliente(id, nome, telefone)
            return True, f"Cliente atualizado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def deletar_cliente(self, id):
        """Deleta um cliente"""
        try:
            nome = self.service.obter_cliente(id).nome
            self.service.deletar_cliente(id)
            return True, f"Cliente {nome} deletado com sucesso"
        except ValueError as e:
            return False, str(e)
    
    def exibir_resumo_cliente(self, id):
        """Exibe um resumo dos dados do cliente"""
        try:
            cliente = self.service.obter_cliente(id)
            linhas = []
            linhas.append(f"ID: {cliente.id}")
            linhas.append(f"Nome: {cliente.nome}")
            linhas.append(f"Telefone: {cliente.telefone}")
            linhas.append(f"Veiculos: {len(cliente.veiculos)}")
            return True, "\n".join(linhas)
        except ValueError as e:
            return False, str(e)
