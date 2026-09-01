# OficinaTech

Projeto da disciplina de Programação Orientada a Objetos II.

Sistema fictício para gerenciamento de uma oficina mecânica com arquitetura em camadas e conceitos avançados de POO.

## Estrutura

- `app/models` — Objetos do domínio com encapsulamento e validações
- `app/repositories` — Camada de persistência (JSON)
- `app/services` — Regras de negócio e orquestração
- `app/controllers` — Coordenação entre menu e serviços
- `app/menu.py` — Interface interativa em linha de comando

## Execução

### Menu Interativo (Principal)
```bash
python main.py
```

### Testes Automáticos
```bash
python test_system.py
```

## Funcionalidades

✓ Gerenciar Clientes (cadastro, listagem, edição)
✓ Gerenciar Veículos (cadastro, validação de placa, associação a cliente)
✓ Gerenciar Serviços (cadastro, listagem)
✓ Gerenciar Peças (cadastro, controle de estoque, alerta de estoque baixo)
✓ Gerenciar Funcionários (cadastro, filtro por cargo)
✓ Gerenciar Ordens de Serviço:
  - Criar ordem associada a cliente e veículo
  - Adicionar serviços e peças
  - Atribuir mecânico responsável
  - Fluxo de status (aberta → em_andamento → concluida)
  - Cálculo automático de valor total
  - Controle automático de estoque de peças

## Conceitos de POO Aplicados

### Encapsulamento
- Atributos privados com `_`
- Acesso controlado via properties
- Validação em construtores e setters

### Herança
- `BaseRepository` como classe base para todos os repositórios
- Interface comum entre repositórios

### Polimorfismo
- Implementação uniforme de `salvar`, `obter_por_id`, `listar_todos`, etc.

### Abstração
- Classes abstratas com `ABC` em `BaseRepository`
- Interfaces bem definidas

### Composição
- Cliente possui Lista[Veículo]
- Veículo possui Lista[OrdemDeServico]
- OrdemDeServico possui Lista[Serviço] e Lista[Peça]

### Single Responsibility Principle
- Models: representação de dados
- Repositories: persistência
- Services: lógica de negócio
- Controllers: coordenação
- Menu: interação com usuário

### Enums
- `StatusOrdem` para evitar strings mágicas

## Arquitetura em Camadas

```
┌─────────────────────────────────┐
│     MENU (CLI Interativo)       │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│        CONTROLLERS              │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│         SERVICES                │
│    (Lógica de Negócio)          │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│      REPOSITORIES               │
│    (Persistência em JSON)       │
└─────────────────────────────────┘
```

## Dados Persistentes

Os dados são salvos automaticamente em JSON:
- `data/clientes.json`
- `data/veiculos.json`
- `data/servicos.json`
- `data/pecas.json`
- `data/funcionarios.json`
- `data/ordens_servico.json`

## Próximas Melhorias

1. Banco de dados (SQLite/PostgreSQL)
2. API REST (Flask/FastAPI)
3. Testes unitários completos
4. Interface gráfica (Tkinter/Qt)
5. Autenticação de usuários
6. Geração de relatórios (PDF)
7. Dashboard com métricas
8. Sincronização multi-usuário
