# OficinaTech / AutoTech — projeto integrado

Projeto didático de POO II: models, seis repositories, SQLite e demonstração pelo terminal.

## Requisitos
Python 3.10+. Não requer pacotes externos.

## Executar
`python main.py` abre o menu.
`python main.py --demo` executa uma demonstração e grava uma nova OS.
`python -m unittest discover -s tests -v` executa os testes.

O banco `oficina.db` é criado na pasta do projeto. O arquivo está no `.gitignore`.

## Arquitetura
`Models → Repositories → Database → SQLite`

A OS guarda os IDs do cliente, veículo e mecânico, além de serviços e peças associados. Os valores praticados ficam nas tabelas associativas para preservar o histórico. O estoque não é baixado automaticamente nesta versão.
