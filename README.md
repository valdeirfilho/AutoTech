# AutoTech — Base para desenvolvimento de interfaces gráficas

Projeto didático de Programação Orientada a Objetos II com Python e SQLite.

Esta branch contém somente a base funcional do sistema: modelos, banco de dados, repositórios, serviços e testes automatizados. **Não há interface gráfica implementada.** Cada grupo deverá construir sua própria interface utilizando a mesma camada de negócio.

## Requisitos

- Python 3.10 ou superior.
- Nenhuma dependência externa para executar a base.
- SQLite, disponível na biblioteca padrão do Python.

## Preparação do ambiente (Windows)

Na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Não é necessário instalar bibliotecas externas para testar a base.

## Executar os testes

```powershell
py -m unittest discover -s tests -v
```

## Executar a demonstração no terminal

```powershell
py main.py --demo
```

Para abrir o menu de terminal:

```powershell
py main.py
```

## Arquitetura disponível

```text
app/
├── database/       # conexão, esquema e persistência SQLite
├── models/         # entidades e regras do domínio
├── repositories/   # operações de persistência e consultas
├── services/       # casos de uso e regras de negócio
└── interfaces/     # espaço reservado para as interfaces dos grupos
    ├── grupo_1/
    ├── grupo_2/
    ├── grupo_3/
    ├── grupo_4/
    └── grupo_5/

tests/              # testes automatizados da base
docs/               # documentação do trabalho
```

## Integração com a base

As interfaces devem utilizar a classe `Database` e a fachada `OficinaService`. Não implementem SQL diretamente nas telas e não dupliquem classes de domínio.

Exemplo de inicialização (ajuste o caminho conforme a localização do arquivo da interface):

```python
from pathlib import Path

from app.database.database import Database
from app.services.oficina_service import OficinaService

ROOT = Path(__file__).resolve().parents[3]
database = Database(ROOT / "oficina.db")
service = OficinaService(database)
```

A classe `OficinaService` oferece operações para cadastrar clientes, veículos, mecânicos, serviços e peças, abrir ordens de serviço, alterar seus status e consultar um resumo da oficina. Os repositórios também estão disponíveis por meio de atributos do serviço, como `service.clientes`, `service.veiculos` e `service.ordens`.

Consulte [docs/trabalho_interfaces_graficas.md](docs/trabalho_interfaces_graficas.md) para os requisitos e as regras de desenvolvimento.

## Banco de dados

- O arquivo `oficina.db` é criado automaticamente na primeira inicialização da base.
- O banco local está no `.gitignore` e não deve ser enviado ao Git.
- Cada instalação local terá seu próprio arquivo SQLite. Os grupos não compartilham um banco remoto.

## Regras de negócio já implementadas

- Associação de veículo ao cliente.
- Validação de que o veículo pertence ao cliente selecionado na abertura da ordem.
- Verificação da disponibilidade de estoque para peças incluídas na ordem.
- Cálculo do total da ordem de serviço.
- Preservação dos valores aplicados no momento da abertura da ordem.
- Transições de status controladas.
- Persistência das operações em SQLite.

A quantidade em estoque ainda não é descontada automaticamente ao abrir uma ordem. Essa regra deverá ser definida separadamente para evitar descontos duplicados em caso de edição ou cancelamento.
