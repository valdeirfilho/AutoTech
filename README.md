# OficinaTech

Projeto da disciplina de Programação Orientada a Objetos II.

Sistema fictício para gerenciamento de uma oficina mecânica.

## Estrutura

- `app/models` — objetos do domínio
- `app/repositories` — persistência dos dados
- `app/services` — regras e operações
- `app/controllers` — coordenação da aplicação

## Como rodar o sistema

Pré-requisito: ter o Python 3 instalado na máquina.

Abra o terminal na raiz do projeto e execute:

```bash
python main.py
```

Se estiver no Windows e o comando `python` não funcionar, use:

```powershell
py .\main.py
```

Esse comando executa a aplicação principal e imprime um exemplo de cliente e veículo da oficina.
