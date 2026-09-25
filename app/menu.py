from app.controllers import (
    ClienteController,
    VeiculoController,
    ServicoController,
    PecaController,
    FuncionarioController,
    OrdemServicoController,
)


class Menu:
    def __init__(self):
        self.cliente_controller = ClienteController()
        self.veiculo_controller = VeiculoController()
        self.servico_controller = ServicoController()
        self.peca_controller = PecaController()
        self.funcionario_controller = FuncionarioController()
        self.ordem_controller = OrdemServicoController()
        self.running = True
    
    def limpar_tela(self):
        """Limpa a tela"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_menu_principal(self):
        """Exibe o menu principal"""
        self.limpar_tela()
        print("=" * 60)
        print("OficinaTech - Sistema de Gerenciamento de Oficina")
        print("=" * 60)
        print("\n[1] Gerenciar Clientes")
        print("[2] Gerenciar Veiculos")
        print("[3] Gerenciar Servicos")
        print("[4] Gerenciar Pecas")
        print("[5] Gerenciar Funcionarios")
        print("[6] Gerenciar Ordens de Servico")
        print("[0] Sair")
        print("\n" + "-" * 60)
    
    def exibir_menu_clientes(self):
        """Submenu de clientes"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("GERENCIAR CLIENTES")
            print("=" * 60)
            print("\n[1] Cadastrar cliente")
            print("[2] Listar clientes")
            print("[3] Ver detalhes de cliente")
            print("[4] Voltar")
            print("\n" + "-" * 60)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.limpar_tela()
                print("--- Cadastro de Cliente ---\n")
                try:
                    id_cliente = int(input("ID: "))
                    nome = input("Nome: ").strip()
                    telefone = input("Telefone: ").strip()
                    
                    sucesso, mensagem = self.cliente_controller.cadastrar_cliente(id_cliente, nome, telefone)
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "2":
                self.limpar_tela()
                print("--- Lista de Clientes ---\n")
                clientes = self.cliente_controller.listar_clientes()
                if clientes:
                    for cliente in clientes:
                        print(f"ID: {cliente.id} | Nome: {cliente.nome} | Telefone: {cliente.telefone}")
                else:
                    print("Nenhum cliente cadastrado.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "3":
                self.limpar_tela()
                print("--- Detalhes do Cliente ---\n")
                try:
                    id_cliente = int(input("ID do cliente: "))
                    sucesso, mensagem = self.cliente_controller.exibir_resumo_cliente(id_cliente)
                    print(f"\n{mensagem}\n")
                except ValueError:
                    print("ID inválido\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "4":
                break
            
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
    
    def exibir_menu_veiculos(self):
        """Submenu de veículos"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("GERENCIAR VEICULOS")
            print("=" * 60)
            print("\n[1] Cadastrar veiculo")
            print("[2] Listar veiculos")
            print("[3] Ver detalhes de veiculo")
            print("[4] Voltar")
            print("\n" + "-" * 60)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.limpar_tela()
                print("--- Cadastro de Veiculo ---\n")
                try:
                    id_veiculo = int(input("ID: "))
                    placa = input("Placa (ex: ABC-1234): ").strip().upper()
                    modelo = input("Modelo: ").strip()
                    ano = int(input("Ano: "))
                    cliente_id = int(input("ID do cliente: "))
                    
                    sucesso, mensagem = self.veiculo_controller.cadastrar_veiculo(
                        id_veiculo, placa, modelo, ano, cliente_id
                    )
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "2":
                self.limpar_tela()
                print("--- Lista de Veiculos ---\n")
                veiculos = self.veiculo_controller.listar_veiculos()
                if veiculos:
                    for veiculo in veiculos:
                        print(f"ID: {veiculo.id} | Placa: {veiculo.placa} | {veiculo.modelo} ({veiculo.ano})")
                else:
                    print("Nenhum veiculo cadastrado.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "3":
                self.limpar_tela()
                print("--- Detalhes do Veiculo ---\n")
                try:
                    id_veiculo = int(input("ID do veiculo: "))
                    sucesso, mensagem = self.veiculo_controller.exibir_resumo_veiculo(id_veiculo)
                    print(f"\n{mensagem}\n")
                except ValueError:
                    print("ID inválido\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "4":
                break
            
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
    
    def exibir_menu_servicos(self):
        """Submenu de serviços"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("GERENCIAR SERVICOS")
            print("=" * 60)
            print("\n[1] Cadastrar servico")
            print("[2] Listar servicos")
            print("[3] Voltar")
            print("\n" + "-" * 60)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.limpar_tela()
                print("--- Cadastro de Servico ---\n")
                try:
                    id_servico = int(input("ID: "))
                    nome = input("Nome: ").strip()
                    descricao = input("Descricao: ").strip()
                    valor = float(input("Valor (R$): "))
                    
                    sucesso, mensagem = self.servico_controller.cadastrar_servico(
                        id_servico, nome, descricao, valor
                    )
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "2":
                self.limpar_tela()
                print("--- Lista de Servicos ---\n")
                servicos = self.servico_controller.listar_servicos()
                if servicos:
                    for servico in servicos:
                        print(f"ID: {servico.id} | {servico.nome} | R$ {servico.valor:.2f}")
                else:
                    print("Nenhum servico cadastrado.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "3":
                break
            
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
    
    def exibir_menu_pecas(self):
        """Submenu de peças"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("GERENCIAR PECAS")
            print("=" * 60)
            print("\n[1] Cadastrar peca")
            print("[2] Listar pecas")
            print("[3] Verificar estoque baixo")
            print("[4] Voltar")
            print("\n" + "-" * 60)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.limpar_tela()
                print("--- Cadastro de Peca ---\n")
                try:
                    id_peca = int(input("ID: "))
                    nome = input("Nome: ").strip()
                    descricao = input("Descricao: ").strip()
                    valor = float(input("Valor (R$): "))
                    estoque = int(input("Quantidade em estoque: "))
                    
                    sucesso, mensagem = self.peca_controller.cadastrar_peca(
                        id_peca, nome, descricao, valor, estoque
                    )
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "2":
                self.limpar_tela()
                print("--- Lista de Pecas ---\n")
                pecas = self.peca_controller.listar_pecas()
                if pecas:
                    for peca in pecas:
                        print(f"ID: {peca.id} | {peca.nome} | R$ {peca.valor:.2f} | Estoque: {peca.quantidade_estoque}")
                else:
                    print("Nenhuma peca cadastrada.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "3":
                self.limpar_tela()
                print("--- Pecas com Estoque Baixo ---\n")
                pecas = self.peca_controller.listar_com_estoque_baixo(5)
                if pecas:
                    for peca in pecas:
                        print(f"ID: {peca.id} | {peca.nome} | Estoque: {peca.quantidade_estoque} (CRITICO!)")
                else:
                    print("Todas as pecas possuem estoque adequado.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "4":
                break
            
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
    
    def exibir_menu_funcionarios(self):
        """Submenu de funcionários"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("GERENCIAR FUNCIONARIOS")
            print("=" * 60)
            print("\n[1] Cadastrar funcionario")
            print("[2] Listar funcionarios")
            print("[3] Listar mecanicos")
            print("[4] Voltar")
            print("\n" + "-" * 60)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.limpar_tela()
                print("--- Cadastro de Funcionario ---\n")
                try:
                    id_func = int(input("ID: "))
                    nome = input("Nome: ").strip()
                    cargo = input("Cargo (ex: Mecanico): ").strip()
                    telefone = input("Telefone: ").strip()
                    
                    sucesso, mensagem = self.funcionario_controller.cadastrar_funcionario(
                        id_func, nome, cargo, telefone
                    )
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "2":
                self.limpar_tela()
                print("--- Lista de Funcionarios ---\n")
                funcionarios = self.funcionario_controller.listar_funcionarios()
                if funcionarios:
                    for func in funcionarios:
                        print(f"ID: {func.id} | {func.nome} | {func.cargo}")
                else:
                    print("Nenhum funcionario cadastrado.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "3":
                self.limpar_tela()
                print("--- Mecanicos ---\n")
                mecanicos = self.funcionario_controller.listar_mecanicos()
                if mecanicos:
                    for mec in mecanicos:
                        print(f"ID: {mec.id} | {mec.nome}")
                else:
                    print("Nenhum mecanico cadastrado.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "4":
                break
            
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
    
    def exibir_menu_ordens(self):
        """Submenu de ordens de serviço"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("GERENCIAR ORDENS DE SERVICO")
            print("=" * 60)
            print("\n[1] Criar nova ordem")
            print("[2] Listar ordens")
            print("[3] Adicionar servico a ordem")
            print("[4] Adicionar peca a ordem")
            print("[5] Iniciar ordem")
            print("[6] Concluir ordem")
            print("[7] Ver detalhes de ordem")
            print("[8] Voltar")
            print("\n" + "-" * 60)
            
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.limpar_tela()
                print("--- Criar Ordem de Servico ---\n")
                try:
                    id_ordem = int(input("ID da ordem: "))
                    veiculo_id = int(input("ID do veiculo: "))
                    cliente_id = int(input("ID do cliente: "))
                    
                    sucesso, mensagem = self.ordem_controller.criar_ordem(id_ordem, veiculo_id, cliente_id)
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "2":
                self.limpar_tela()
                print("--- Lista de Ordens ---\n")
                ordens = self.ordem_controller.listar_ordens()
                if ordens:
                    for ordem in ordens:
                        print(f"ID: {ordem.id} | Status: {ordem.status.value} | Veiculo: {ordem.veiculo_id} | Cliente: {ordem.cliente_id}")
                else:
                    print("Nenhuma ordem cadastrada.")
                print()
                input("Pressione ENTER para continuar...")
            
            elif opcao == "3":
                self.limpar_tela()
                print("--- Adicionar Servico a Ordem ---\n")
                try:
                    ordem_id = int(input("ID da ordem: "))
                    servico_id = int(input("ID do servico: "))
                    
                    sucesso, mensagem = self.ordem_controller.adicionar_servico(ordem_id, servico_id)
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "4":
                self.limpar_tela()
                print("--- Adicionar Peca a Ordem ---\n")
                try:
                    ordem_id = int(input("ID da ordem: "))
                    peca_id = int(input("ID da peca: "))
                    
                    sucesso, mensagem = self.ordem_controller.adicionar_peca(ordem_id, peca_id)
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "5":
                self.limpar_tela()
                print("--- Iniciar Ordem ---\n")
                try:
                    ordem_id = int(input("ID da ordem: "))
                    sucesso, mensagem = self.ordem_controller.iniciar_ordem(ordem_id)
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "6":
                self.limpar_tela()
                print("--- Concluir Ordem ---\n")
                try:
                    ordem_id = int(input("ID da ordem: "))
                    sucesso, mensagem = self.ordem_controller.concluir_ordem(ordem_id)
                    print(f"\n{mensagem}\n")
                except ValueError as e:
                    print(f"Erro: {e}\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "7":
                self.limpar_tela()
                print("--- Detalhes da Ordem ---\n")
                try:
                    ordem_id = int(input("ID da ordem: "))
                    sucesso, mensagem = self.ordem_controller.exibir_resumo_ordem(ordem_id)
                    print(f"\n{mensagem}\n")
                except ValueError:
                    print("ID inválido\n")
                
                input("Pressione ENTER para continuar...")
            
            elif opcao == "8":
                break
            
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
    
    def executar(self):
        """Executa o menu principal"""
        while self.running:
            self.exibir_menu_principal()
            opcao = input("Escolha uma opcao: ").strip()
            
            if opcao == "1":
                self.exibir_menu_clientes()
            elif opcao == "2":
                self.exibir_menu_veiculos()
            elif opcao == "3":
                self.exibir_menu_servicos()
            elif opcao == "4":
                self.exibir_menu_pecas()
            elif opcao == "5":
                self.exibir_menu_funcionarios()
            elif opcao == "6":
                self.exibir_menu_ordens()
            elif opcao == "0":
                self.limpar_tela()
                print("Obrigado por usar OficinaTech!")
                print("Encerrando...")
                self.running = False
            else:
                print("Opcao inválida!")
                input("Pressione ENTER para continuar...")
