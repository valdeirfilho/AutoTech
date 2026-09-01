#!/usr/bin/env python
# Script de teste automático do sistema

from app.services import (
    ClienteService,
    VeiculoService,
    ServicoService,
    PecaService,
    FuncionarioService,
    OrdemServicoService,
)


def test_sistema():
    print("=" * 70)
    print("OficinaTech - Teste Automatico do Sistema Completo")
    print("=" * 70)
    
    # Inicializar serviços
    cliente_service = ClienteService()
    veiculo_service = VeiculoService()
    servico_service = ServicoService()
    peca_service = PecaService()
    funcionario_service = FuncionarioService()
    ordem_service = OrdemServicoService()
    
    print("\n[TESTE 1] Criando Clientes...")
    cliente1 = cliente_service.criar_cliente(1, "Joao Silva", "34 99999-9999")
    cliente2 = cliente_service.criar_cliente(2, "Maria Santos", "34 98888-8888")
    print(f"  OK - {cliente1}")
    print(f"  OK - {cliente2}")
    
    print("\n[TESTE 2] Criando Veiculos...")
    veiculo1 = veiculo_service.criar_veiculo(1, "ABC-1234", "Toyota Corolla", 2020, cliente1.id)
    veiculo2 = veiculo_service.criar_veiculo(2, "DEF-5678", "Honda Civic", 2022, cliente2.id)
    print(f"  OK - {veiculo1}")
    print(f"  OK - {veiculo2}")
    
    print("\n[TESTE 3] Criando Servicos...")
    servico1 = servico_service.criar_servico(1, "Troca de oleo", "Troca de oleo", 150.00)
    servico2 = servico_service.criar_servico(2, "Alinhamento", "Alinhamento", 200.00)
    print(f"  OK - {servico1}")
    print(f"  OK - {servico2}")
    
    print("\n[TESTE 4] Criando Pecas...")
    peca1 = peca_service.criar_peca(1, "Filtro de oleo", "Filtro original", 50.00, 10)
    peca2 = peca_service.criar_peca(2, "Pastilha de freio", "Pastilha traseira", 120.00, 5)
    print(f"  OK - {peca1}")
    print(f"  OK - {peca2}")
    
    print("\n[TESTE 5] Criando Funcionarios...")
    func1 = funcionario_service.criar_funcionario(1, "Carlos", "Mecanico", "34 98888-7777")
    func2 = funcionario_service.criar_funcionario(2, "Ana", "Assistente", "34 97777-7777")
    print(f"  OK - {func1}")
    print(f"  OK - {func2}")
    
    print("\n[TESTE 6] Criando Ordem de Servico...")
    ordem1 = ordem_service.criar_ordem(1, veiculo1.id, cliente1.id)
    print(f"  OK - {ordem1}")
    
    print("\n[TESTE 7] Adicionando Servicos a Ordem...")
    ordem1 = ordem_service.adicionar_servico(ordem1.id, servico1.id)
    ordem1 = ordem_service.adicionar_servico(ordem1.id, servico2.id)
    print(f"  OK - Servicos adicionados")
    
    print("\n[TESTE 8] Adicionando Pecas a Ordem...")
    ordem1 = ordem_service.adicionar_peca(ordem1.id, peca1.id)
    print(f"  OK - Peca adicionada")
    
    print("\n[TESTE 9] Fluxo de Status...")
    ordem1 = ordem_service.iniciar_ordem(ordem1.id)
    print(f"  OK - Status: {ordem1.status.value}")
    
    ordem1 = ordem_service.concluir_ordem(ordem1.id)
    print(f"  OK - Status: {ordem1.status.value}")
    
    print("\n[TESTE 10] Recuperando Dados Persistidos...")
    ordem_recuperada = ordem_service.obter_ordem(ordem1.id)
    print(f"  OK - Ordem recuperada do disco")
    print(f"      ID: {ordem_recuperada.id}")
    print(f"      Status: {ordem_recuperada.status.value}")
    print(f"      Valor total: R$ {ordem_service.calcular_valor_total(ordem_recuperada.id):.2f}")
    
    print("\n[TESTE 11] Verificando Persistencia de Dados...")
    clientes = cliente_service.listar_clientes()
    print(f"  OK - {len(clientes)} cliente(s) em disco")
    
    veiculos = veiculo_service.listar_veiculos()
    print(f"  OK - {len(veiculos)} veiculo(s) em disco")
    
    ordens = ordem_service.listar_ordens()
    print(f"  OK - {len(ordens)} ordem(s) em disco")
    
    print("\n[TESTE 12] Consultando Estoque...")
    pecas = peca_service.listar_pecas()
    print(f"  OK - {len(pecas)} peca(s) cadastrada(s)")
    for peca in pecas:
        print(f"      {peca.nome}: {peca.quantidade_estoque} unidades")
    
    print("\n" + "=" * 70)
    print("Todos os testes completados com sucesso!")
    print("=" * 70)
    
    print("\nArquivos de dados criados em:")
    print("  - data/clientes.json")
    print("  - data/veiculos.json")
    print("  - data/servicos.json")
    print("  - data/pecas.json")
    print("  - data/funcionarios.json")
    print("  - data/ordens_servico.json")


if __name__ == "__main__":
    test_sistema()
