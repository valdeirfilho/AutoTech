# AutoTech — Oficina mecânica

Projeto didático de POO II com Python e SQLite. Inclui modelos, repositórios, uma camada de serviços compartilhada, uma interface web inicial com NiceGUI e um ponto de entrada inicial para a interface desktop com Tkinter.

## Requisitos

- Python 3.10 ou superior.
- Para a interface web, conexão à internet apenas durante a instalação do NiceGUI, se ele ainda não estiver instalado.
- A versão desktop utiliza Tkinter, normalmente incluído na instalação padrão do Python para Windows.

## Executar os testes

Na pasta do projeto:

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

## Interface web (NiceGUI)

1. Crie e ative um ambiente virtual (recomendado):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale a dependência da interface web:

```powershell
py -m pip install -r requirements.txt
```

3. Inicie a aplicação:

```powershell
py -m app.interfaces.web.main
```

4. Abra no navegador o endereço informado pelo NiceGUI; por padrão, a aplicação usa `http://127.0.0.1:8080`.

A interface inicial permite cadastrar clientes, veículos, mecânicos, serviços e peças, abrir ordens de serviço, consultar os totais e alterar o status das ordens. As regras de negócio ficam na classe `OficinaService`, e não diretamente nos repositórios nem na tela.

### Acesso pela rede local

Para disponibilizar a interface a outros computadores da rede, altere o parâmetro `host` de `ui.run` em `app/interfaces/web/main.py` para `0.0.0.0`, configure o firewall conforme a política da instituição e informe aos usuários o endereço IP do computador servidor com a porta `8080`. Faça isso apenas em uma rede confiável. Nesta primeira versão, o sistema ainda não tem autenticação nem controle de permissões.

## Interface desktop (Tkinter)

A versão desktop tem somente uma janela inicial de estrutura. A implementação das telas de cadastro e ordens de serviço será feita após validar os casos de uso na interface web.

```powershell
py -m app.interfaces.desktop.main
```

## Arquitetura

```text
app/
├── database/       # conexão e esquema SQLite
├── models/         # entidades e regras de domínio
├── repositories/   # persistência e consultas
├── services/       # casos de uso e regras compartilhadas
└── interfaces/
    ├── web/        # NiceGUI
    └── desktop/    # Tkinter (estrutura inicial)
```

## Observações importantes

- O arquivo `oficina.db` é criado na pasta do projeto na primeira execução da interface web.
- O banco local não deve ser colocado no Git; ele está no `.gitignore`.
- A interface inicial valida se o veículo pertence ao cliente selecionado e verifica a disponibilidade de estoque para as peças incluídas na ordem.
- A quantidade em estoque ainda não é descontada automaticamente ao abrir uma ordem. Essa regra deverá ser definida e implementada separadamente para evitar descontos duplicados quando uma ordem for editada ou cancelada.
- Esta versão ainda não inclui login, permissões, edição/exclusão por tela, relatórios ou impressão.
