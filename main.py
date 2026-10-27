import argparse

from app.database.database import Database
from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.mecanico import Mecanico
from app.models.servico import Servico
from app.models.peca import Peca
from app.models.ordem_de_servico import OrdemDeServico
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.veiculo_repository import VeiculoRepository
from app.repositories.mecanico_repository import MecanicoRepository
from app.repositories.servico_repository import ServicoRepository
from app.repositories.peca_repository import PecaRepository
from app.repositories.ordem_de_servico_repository import OrdemDeServicoRepository


def criar_repositories(db):
    db.criar_tabelas()
    return {
        "clientes": ClienteRepository(db), "veiculos": VeiculoRepository(db),
        "mecanicos": MecanicoRepository(db), "servicos": ServicoRepository(db),
        "pecas": PecaRepository(db), "ordens": OrdemDeServicoRepository(db)
    }


def localizar_ou_criar(repo, lista, chave, novo):
    for obj in lista:
        if getattr(obj, chave) == getattr(novo, chave):
            return obj
    return repo.salvar(novo)


def demonstracao(r):
    cliente = r["clientes"].buscar_por_telefone("31988887777")
    if not cliente:
        cliente = r["clientes"].salvar(Cliente("Ana Martins", "31988887777"))

    veiculo = r["veiculos"].buscar_por_placa("ABC1D23")
    if not veiculo:
        veiculo = r["veiculos"].salvar(Veiculo("ABC1D23", "Honda", "Civic", 2020, cliente.id))

    mecanico = next((m for m in r["mecanicos"].buscar_todos()
                     if m.nome == "Carlos Souza"), None)
    if not mecanico:
        mecanico = r["mecanicos"].salvar(Mecanico("Carlos Souza", "Mecânica geral"))

    def servico(descricao, valor):
        existente = next((s for s in r["servicos"].buscar_todos()
                          if s.descricao == descricao), None)
        return existente or r["servicos"].salvar(Servico(descricao, valor))

    def peca(nome, valor, estoque):
        existente = next((p for p in r["pecas"].buscar_todos()
                          if p.nome == nome), None)
        return existente or r["pecas"].salvar(Peca(nome, valor, estoque))

    troca = servico("Troca de óleo", 150.00)
    alinhamento = servico("Alinhamento", 120.00)
    filtro = peca("Filtro de óleo", 45.00, 10)
    oleo = peca("Óleo de motor", 45.00, 20)

    os = OrdemDeServico(cliente.id, veiculo.id, mecanico.id,
                        observacoes="Revisão preventiva")
    os.adicionar_servico(troca)
    os.adicionar_servico(alinhamento)
    os.adicionar_peca(filtro)
    os.adicionar_peca(oleo)
    r["ordens"].salvar(os)
    imprimir_os(os, r, cliente, veiculo, mecanico)
    print("\nDemonstração concluída: OS persistida no SQLite.")


def imprimir_os(os, r, cliente=None, veiculo=None, mecanico=None):
    cliente = cliente or r["clientes"].buscar_por_id(os.cliente_id)
    veiculo = veiculo or r["veiculos"].buscar_por_id(os.veiculo_id)
    mecanico = mecanico or (r["mecanicos"].buscar_por_id(os.mecanico_id) if os.mecanico_id else None)
    print("\n" + "=" * 54)
    print(f"ORDEM DE SERVIÇO #{os.id}")
    print("=" * 54)
    print(f"Cliente: {cliente}")
    print(f"Veículo: {veiculo}")
    print(f"Mecânico: {mecanico or 'Não atribuído'}")
    print(f"Status: {os.status.value}")
    print(f"Observações: {os.observacoes}")
    print("\nServiços:")
    for s, valor in zip(os.servicos, os.valores_servicos):
        print(f"  {s.descricao}: R$ {valor:.2f}")
    print("\nPeças:")
    for p, qtd, valor in zip(os.pecas, os.quantidades_pecas, os.valores_pecas):
        print(f"  {p.nome} x {qtd}: R$ {valor*qtd:.2f}")
    print("-" * 54)
    print(f"TOTAL: R$ {os.calcular_total():.2f}")
    print("=" * 54)


def listar_os(r):
    ordens = r["ordens"].buscar_todos()
    if not ordens:
        print("Nenhuma OS cadastrada.")
    for os in ordens:
        imprimir_os(os, r)


def main():
    parser = argparse.ArgumentParser(description="OficinaTech — demonstração integrada")
    parser.add_argument("--demo", action="store_true", help="executa uma demonstração sem abrir o menu")
    args = parser.parse_args()
    db = Database("oficina.db")
    try:
        r = criar_repositories(db)
        if args.demo:
            demonstracao(r)
            return
        while True:
            print("\n=== OficinaTech ===")
            print("1. Executar demonstração integrada (cria nova OS)")
            print("2. Listar ordens de serviço")
            print("0. Sair")
            escolha = input("Opção: ").strip()
            if escolha == "1":
                try:
                    demonstracao(r)
                except Exception as erro:
                    print(f"Erro na demonstração: {erro}")
            elif escolha == "2":
                listar_os(r)
            elif escolha == "0":
                break
            else:
                print("Opção inválida.")
    finally:
        db.fechar()


if __name__ == "__main__":
    main()
