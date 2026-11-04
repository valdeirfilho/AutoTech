# Trabalho: cinco interfaces gráficas para o AutoTech

## Objetivo

Desenvolver cinco interfaces gráficas distintas para o mesmo sistema AutoTech. Todos os grupos utilizarão a mesma base de domínio, persistência e regras de negócio. O objetivo é comparar diferentes tecnologias de interface sem duplicar a lógica da aplicação.

## Base fornecida

A branch contém:
- modelos em `app/models/`;
- conexão, esquema e criação das tabelas SQLite em `app/database/database.py`;
- persistência em `app/repositories/`;
- casos de uso compartilhados em `app/services/oficina_service.py`;
- testes automatizados em `tests/`.

A classe `OficinaService` é a fachada recomendada para as interfaces. Ela instancia os repositórios e oferece operações como:
- `cadastrar_cliente(nome, telefone)`;
- `cadastrar_veiculo(placa, marca, modelo, ano, cliente_id)`;
- `cadastrar_mecanico(nome, especialidade)`;
- `cadastrar_servico(descricao, valor)`;
- `cadastrar_peca(nome, valor, quantidade_estoque)`;
- `criar_ordem(cliente_id, veiculo_id, mecanico_id=None, observacoes="", servico_ids=None, peca_id=None, quantidade_peca=1)`;
- `alterar_status_ordem(ordem_id, novo_status)`;
- `resumo()`.

Os repositórios também estão disponíveis por meio dos atributos do serviço: `service.clientes`, `service.veiculos`, `service.mecanicos`, `service.servicos`, `service.pecas` e `service.ordens`. Seus métodos de consulta podem ser utilizados para alimentar tabelas e listas.

## Organização dos grupos

Cada equipe deve trabalhar exclusivamente em sua pasta:
- Grupo 1: `app/interfaces/grupo_1/`
- Grupo 2: `app/interfaces/grupo_2/`
- Grupo 3: `app/interfaces/grupo_3/`
- Grupo 4: `app/interfaces/grupo_4/`
- Grupo 5: `app/interfaces/grupo_5/`

Tecnologias sugeridas para distribuição:
1. NiceGUI — aplicação web em Python.
2. Tkinter — aplicação desktop com biblioteca padrão.
3. CustomTkinter — aplicação desktop com componentes modernos.
4. Flet — interface multiplataforma usando Python.
5. PySide6 — aplicação desktop baseada em Qt.

O professor definirá qual tecnologia cabe a cada equipe. Não instalem todas as bibliotecas no ambiente compartilhado: cada grupo deve documentar e instalar apenas a dependência da sua interface.

## Regras obrigatórias de integração

1. Não alterar `app/models/`, `app/repositories/`, `app/services/` ou `app/database/` para implementar telas.
2. Não criar outro banco de dados nem outro conjunto de classes para representar clientes, veículos, peças ou ordens.
3. Não escrever SQL diretamente nos arquivos da interface.
4. Instanciar `Database` e `OficinaService` e chamar os métodos do serviço.
5. Utilizar o mesmo arquivo local `oficina.db` durante a execução da equipe.
6. Tratar erros de validação e regras de negócio, exibindo mensagens compreensíveis.
7. Manter todos os arquivos do grupo dentro da pasta designada.
8. Não versionar `oficina.db`, ambientes virtuais, arquivos temporários ou credenciais.
9. Antes de enviar alterações, executar os testes: `py -m unittest discover -s tests -v`.
10. Não modificar a interface de outro grupo.

## Inicialização compartilhada

Exemplo de composição da aplicação (ajuste o caminho conforme o arquivo da equipe):

```python
from pathlib import Path

from app.database.database import Database
from app.services.oficina_service import OficinaService

ROOT = Path(__file__).resolve().parents[3]
database = Database(ROOT / "oficina.db")
service = OficinaService(database)
```

A partir daí, a interface chama, por exemplo:

```python
cliente = service.cadastrar_cliente("Maria Silva", "(31) 99999-0000")
clientes = service.clientes.buscar_todos()
ordens = service.ordens.buscar_todos()
```

Atenção: o índice de `parents` depende da localização real do arquivo. Confiram o caminho no projeto de vocês.

## Requisitos funcionais mínimos

Cada interface deverá oferecer, no mínimo:
- painel inicial com resumo da oficina;
- cadastro e consulta de clientes;
- cadastro e consulta de veículos;
- cadastro e consulta de mecânicos;
- cadastro e consulta de serviços;
- cadastro e consulta de peças;
- abertura de ordem de serviço;
- consulta de ordens e seus totais;
- alteração de status respeitando as regras existentes.

A equipe poderá acrescentar edição, pesquisa, filtros, diálogos, relatórios e melhorias de usabilidade, desde que não altere a camada central sem autorização.

## Entregáveis

- código-fonte dentro da pasta do grupo;
- arquivo `README.md` com tecnologia, instalação e execução;
- imagens ou vídeo curto demonstrando os fluxos;
- breve relatório explicando a organização da interface e como ela consome `OficinaService`;
- histórico de commits identificável por equipe.

## Critérios sugeridos de avaliação

| Critério | Peso |
|---|---:|
| Funcionalidade e cobertura dos requisitos | 30% |
| Integração correta com serviços e banco | 25% |
| Usabilidade e organização visual | 20% |
| Organização do código e modularização | 15% |
| Documentação e apresentação | 10% |

## Execução dos testes da base

Na raiz do repositório:

```powershell
py -m unittest discover -s tests -v
```

A base de domínio é compartilhada. A interface de cada equipe deve ser uma camada de apresentação, não uma segunda implementação do sistema.
