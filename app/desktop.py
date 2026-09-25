import tkinter as tk
from tkinter import messagebox, ttk

from app.services import (
    ClienteService,
    FuncionarioService,
    OrdemServicoService,
    PecaService,
    ServicoService,
    VeiculoService,
)


class OficinaTechDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OficinaTech - Desktop")
        self.geometry("1150x700")
        self.minsize(980, 620)
        self.configure(bg="#f3f6f9")

        self.cliente_service = ClienteService()
        self.veiculo_service = VeiculoService()
        self.servico_service = ServicoService()
        self.peca_service = PecaService()
        self.funcionario_service = FuncionarioService()
        self.ordem_service = OrdemServicoService()

        self._build_ui()
        self._carregar_abas()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.tabs = {
            "clientes": self._criar_tab_clientes(notebook),
            "veiculos": self._criar_tab_veiculos(notebook),
            "servicos": self._criar_tab_servicos(notebook),
            "pecas": self._criar_tab_pecas(notebook),
            "funcionarios": self._criar_tab_funcionarios(notebook),
            "ordens": self._criar_tab_ordens(notebook),
        }

        self.status_var = tk.StringVar(value="Sistema pronto")
        status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(10, 6),
        )
        status_bar.pack(fill=tk.X, padx=12, pady=(0, 12))

    def _carregar_abas(self):
        self._atualizar_clientes()
        self._atualizar_veiculos()
        self._atualizar_servicos()
        self._atualizar_pecas()
        self._atualizar_funcionarios()
        self._atualizar_ordens()

    def _mostrar_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)
        self.status_var.set(mensagem)

    def _mostrar_sucesso(self, mensagem):
        self.status_var.set(mensagem)

    def _criar_tab_clientes(self, notebook):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text="Clientes")

        form = ttk.LabelFrame(frame, text="Cadastro de Cliente", padding=12)
        form.pack(fill=tk.X, padx=4, pady=(0, 10))

        campos = {
            "id": ttk.Entry(form, width=18),
            "nome": ttk.Entry(form, width=40),
            "telefone": ttk.Entry(form, width=28),
        }

        for index, (chave, entrada) in enumerate(campos.items()):
            ttk.Label(form, text=self._rotulo(chave)).grid(row=index, column=0, sticky=tk.W, padx=(0, 8), pady=4)
            entrada.grid(row=index, column=1, sticky=tk.EW, padx=3, pady=4)

        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(frame)
        botoes.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(botoes, text="Salvar cliente", command=self._salvar_cliente).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Listar clientes", command=self._atualizar_clientes).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Excluir selecionado", command=self._excluir_cliente).pack(side=tk.LEFT)

        lista = tk.Listbox(frame, height=18, width=120)
        lista.pack(fill=tk.BOTH, expand=True)
        self.clientes_lista = lista
        self.clientes_campos = campos
        return campos

    def _criar_tab_veiculos(self, notebook):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text="Veículos")

        form = ttk.LabelFrame(frame, text="Cadastro de Veículo", padding=12)
        form.pack(fill=tk.X, padx=4, pady=(0, 10))

        campos = {
            "id": ttk.Entry(form, width=18),
            "placa": ttk.Entry(form, width=18),
            "modelo": ttk.Entry(form, width=30),
            "ano": ttk.Entry(form, width=18),
            "cliente_id": ttk.Entry(form, width=18),
        }

        for index, (chave, entrada) in enumerate(campos.items()):
            ttk.Label(form, text=self._rotulo(chave)).grid(row=index, column=0, sticky=tk.W, padx=(0, 8), pady=4)
            entrada.grid(row=index, column=1, sticky=tk.EW, padx=3, pady=4)

        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(frame)
        botoes.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(botoes, text="Salvar veículo", command=self._salvar_veiculo).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Listar veículos", command=self._atualizar_veiculos).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Excluir selecionado", command=self._excluir_veiculo).pack(side=tk.LEFT)

        lista = tk.Listbox(frame, height=18, width=120)
        lista.pack(fill=tk.BOTH, expand=True)
        self.veiculos_lista = lista
        self.veiculos_campos = campos
        return campos

    def _criar_tab_servicos(self, notebook):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text="Serviços")

        form = ttk.LabelFrame(frame, text="Cadastro de Serviço", padding=12)
        form.pack(fill=tk.X, padx=4, pady=(0, 10))

        campos = {
            "id": ttk.Entry(form, width=18),
            "nome": ttk.Entry(form, width=30),
            "descricao": ttk.Entry(form, width=40),
            "valor": ttk.Entry(form, width=18),
        }

        for index, (chave, entrada) in enumerate(campos.items()):
            ttk.Label(form, text=self._rotulo(chave)).grid(row=index, column=0, sticky=tk.W, padx=(0, 8), pady=4)
            entrada.grid(row=index, column=1, sticky=tk.EW, padx=3, pady=4)

        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(frame)
        botoes.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(botoes, text="Salvar serviço", command=self._salvar_servico).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Listar serviços", command=self._atualizar_servicos).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Excluir selecionado", command=self._excluir_servico).pack(side=tk.LEFT)

        lista = tk.Listbox(frame, height=18, width=120)
        lista.pack(fill=tk.BOTH, expand=True)
        self.servicos_lista = lista
        self.servicos_campos = campos
        return campos

    def _criar_tab_pecas(self, notebook):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text="Peças")

        form = ttk.LabelFrame(frame, text="Cadastro de Peça", padding=12)
        form.pack(fill=tk.X, padx=4, pady=(0, 10))

        campos = {
            "id": ttk.Entry(form, width=18),
            "nome": ttk.Entry(form, width=30),
            "descricao": ttk.Entry(form, width=40),
            "valor": ttk.Entry(form, width=18),
            "quantidade_estoque": ttk.Entry(form, width=18),
        }

        for index, (chave, entrada) in enumerate(campos.items()):
            ttk.Label(form, text=self._rotulo(chave)).grid(row=index, column=0, sticky=tk.W, padx=(0, 8), pady=4)
            entrada.grid(row=index, column=1, sticky=tk.EW, padx=3, pady=4)

        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(frame)
        botoes.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(botoes, text="Salvar peça", command=self._salvar_peca).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Listar peças", command=self._atualizar_pecas).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Excluir selecionado", command=self._excluir_peca).pack(side=tk.LEFT)

        lista = tk.Listbox(frame, height=18, width=120)
        lista.pack(fill=tk.BOTH, expand=True)
        self.pecas_lista = lista
        self.pecas_campos = campos
        return campos

    def _criar_tab_funcionarios(self, notebook):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text="Funcionários")

        form = ttk.LabelFrame(frame, text="Cadastro de Funcionário", padding=12)
        form.pack(fill=tk.X, padx=4, pady=(0, 10))

        campos = {
            "id": ttk.Entry(form, width=18),
            "nome": ttk.Entry(form, width=30),
            "cargo": ttk.Entry(form, width=20),
            "telefone": ttk.Entry(form, width=28),
        }

        for index, (chave, entrada) in enumerate(campos.items()):
            ttk.Label(form, text=self._rotulo(chave)).grid(row=index, column=0, sticky=tk.W, padx=(0, 8), pady=4)
            entrada.grid(row=index, column=1, sticky=tk.EW, padx=3, pady=4)

        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(frame)
        botoes.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(botoes, text="Salvar funcionário", command=self._salvar_funcionario).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Listar funcionários", command=self._atualizar_funcionarios).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Excluir selecionado", command=self._excluir_funcionario).pack(side=tk.LEFT)

        lista = tk.Listbox(frame, height=18, width=120)
        lista.pack(fill=tk.BOTH, expand=True)
        self.funcionarios_lista = lista
        self.funcionarios_campos = campos
        return campos

    def _criar_tab_ordens(self, notebook):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text="Ordens")

        form = ttk.LabelFrame(frame, text="Nova Ordem de Serviço", padding=12)
        form.pack(fill=tk.X, padx=4, pady=(0, 10))

        campos = {
            "id": ttk.Entry(form, width=18),
            "cliente_id": ttk.Entry(form, width=18),
            "veiculo_id": ttk.Entry(form, width=18),
        }

        for index, (chave, entrada) in enumerate(campos.items()):
            ttk.Label(form, text=self._rotulo(chave)).grid(row=index, column=0, sticky=tk.W, padx=(0, 8), pady=4)
            entrada.grid(row=index, column=1, sticky=tk.EW, padx=3, pady=4)

        form.columnconfigure(1, weight=1)

        botoes = ttk.Frame(frame)
        botoes.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(botoes, text="Criar ordem", command=self._salvar_ordem).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Iniciar", command=self._iniciar_ordem).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Concluir", command=self._concluir_ordem).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botoes, text="Listar ordens", command=self._atualizar_ordens).pack(side=tk.LEFT)

        lista = tk.Listbox(frame, height=18, width=120)
        lista.pack(fill=tk.BOTH, expand=True)
        self.ordens_lista = lista
        self.ordens_campos = campos
        return campos

    def _rotulo(self, nome):
        aliases = {
            "cliente_id": "Cliente ID",
            "veiculo_id": "Veículo ID",
            "quantidade_estoque": "Estoque",
            "nome": "Nome",
            "telefone": "Telefone",
            "cargo": "Cargo",
            "descricao": "Descrição",
            "placa": "Placa",
            "modelo": "Modelo",
            "ano": "Ano",
            "valor": "Valor",
            "id": "ID",
        }
        return aliases.get(nome, nome.replace("_", " ").title())

    def _campo(self, nome, container):
        widget = next(
            (w for chave, w in container.items() if chave == nome),
            None,
        )
        if widget is None:
            return ""
        return widget.get().strip()

    def _limpar_campos(self, container):
        for widget in container.values():
            widget.delete(0, tk.END)

    def _listar_clientes(self):
        return self.cliente_service.listar_clientes()

    def _listar_veiculos(self):
        return self.veiculo_service.listar_veiculos()

    def _listar_servicos(self):
        return self.servico_service.listar_servicos()

    def _listar_pecas(self):
        return self.peca_service.listar_pecas()

    def _listar_funcionarios(self):
        return self.funcionario_service.listar_funcionarios()

    def _listar_ordens(self):
        return self.ordem_service.listar_ordens()

    def _obter_selecao(self, lista):
        try:
            item = lista.get(tk.ANCHOR)
        except Exception:
            return None
        if not item:
            return None
        return item.split(" | ", 1)[0]

    def _atualizar_clientes(self):
        self.clientes_lista.delete(0, tk.END)
        for cliente in self._listar_clientes():
            self.clientes_lista.insert(tk.END, f"{cliente.id} | {cliente.nome} | {cliente.telefone}")
        self._mostrar_sucesso("Clientes atualizados")

    def _atualizar_veiculos(self):
        self.veiculos_lista.delete(0, tk.END)
        for veiculo in self._listar_veiculos():
            self.veiculos_lista.insert(tk.END, f"{veiculo.id} | {veiculo.placa} | {veiculo.modelo} | {veiculo.ano} | cliente {veiculo.cliente_id}")
        self._mostrar_sucesso("Veículos atualizados")

    def _atualizar_servicos(self):
        self.servicos_lista.delete(0, tk.END)
        for servico in self._listar_servicos():
            self.servicos_lista.insert(tk.END, f"{servico.id} | {servico.nome} | R$ {servico.valor:.2f}")
        self._mostrar_sucesso("Serviços atualizados")

    def _atualizar_pecas(self):
        self.pecas_lista.delete(0, tk.END)
        for peca in self._listar_pecas():
            self.pecas_lista.insert(tk.END, f"{peca.id} | {peca.nome} | estoque {peca.quantidade_estoque} | R$ {peca.valor:.2f}")
        self._mostrar_sucesso("Peças atualizadas")

    def _atualizar_funcionarios(self):
        self.funcionarios_lista.delete(0, tk.END)
        for funcionario in self._listar_funcionarios():
            self.funcionarios_lista.insert(tk.END, f"{funcionario.id} | {funcionario.nome} | {funcionario.cargo}")
        self._mostrar_sucesso("Funcionários atualizados")

    def _atualizar_ordens(self):
        self.ordens_lista.delete(0, tk.END)
        for ordem in self._listar_ordens():
            self.ordens_lista.insert(tk.END, f"{ordem.id} | cliente {ordem.cliente_id} | veículo {ordem.veiculo_id} | status {ordem.status.value}")
        self._mostrar_sucesso("Ordens atualizadas")

    def _salvar_cliente(self):
        campos = self.tabs["clientes"]
        dados = {
            "id": self._campo("id", campos),
            "nome": self._campo("nome", campos),
            "telefone": self._campo("telefone", campos),
        }
        if not dados["nome"] or not dados["telefone"]:
            self._mostrar_erro("Informe nome e telefone do cliente.")
            return
        try:
            self.cliente_service.criar_cliente(int(dados["id"] or 0), dados["nome"], dados["telefone"])
            self._limpar_campos(campos)
            self._atualizar_clientes()
            self._mostrar_sucesso("Cliente salvo com sucesso")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _salvar_veiculo(self):
        campos = self.tabs["veiculos"]
        dados = {
            "id": self._campo("id", campos),
            "placa": self._campo("placa", campos),
            "modelo": self._campo("modelo", campos),
            "ano": self._campo("ano", campos),
            "cliente_id": self._campo("cliente_id", campos),
        }
        try:
            self.veiculo_service.criar_veiculo(
                int(dados["id"] or 0),
                dados["placa"],
                dados["modelo"],
                int(dados["ano"]),
                int(dados["cliente_id"]),
            )
            self._limpar_campos(campos)
            self._atualizar_veiculos()
            self._mostrar_sucesso("Veículo salvo com sucesso")
        except (ValueError, TypeError) as exc:
            self._mostrar_erro(str(exc))

    def _salvar_servico(self):
        campos = self.tabs["servicos"]
        dados = {
            "id": self._campo("id", campos),
            "nome": self._campo("nome", campos),
            "descricao": self._campo("descricao", campos),
            "valor": self._campo("valor", campos),
        }
        try:
            self.servico_service.criar_servico(
                int(dados["id"] or 0),
                dados["nome"],
                dados["descricao"],
                float(dados["valor"]),
            )
            self._limpar_campos(campos)
            self._atualizar_servicos()
            self._mostrar_sucesso("Serviço salvo com sucesso")
        except (ValueError, TypeError) as exc:
            self._mostrar_erro(str(exc))

    def _salvar_peca(self):
        campos = self.tabs["pecas"]
        dados = {
            "id": self._campo("id", campos),
            "nome": self._campo("nome", campos),
            "descricao": self._campo("descricao", campos),
            "valor": self._campo("valor", campos),
            "quantidade_estoque": self._campo("quantidade_estoque", campos),
        }
        try:
            self.peca_service.criar_peca(
                int(dados["id"] or 0),
                dados["nome"],
                dados["descricao"],
                float(dados["valor"]),
                int(dados["quantidade_estoque"]),
            )
            self._limpar_campos(campos)
            self._atualizar_pecas()
            self._mostrar_sucesso("Peça salva com sucesso")
        except (ValueError, TypeError) as exc:
            self._mostrar_erro(str(exc))

    def _salvar_funcionario(self):
        campos = self.tabs["funcionarios"]
        dados = {
            "id": self._campo("id", campos),
            "nome": self._campo("nome", campos),
            "cargo": self._campo("cargo", campos),
            "telefone": self._campo("telefone", campos),
        }
        try:
            self.funcionario_service.criar_funcionario(
                int(dados["id"] or 0),
                dados["nome"],
                dados["cargo"],
                dados["telefone"],
            )
            self._limpar_campos(campos)
            self._atualizar_funcionarios()
            self._mostrar_sucesso("Funcionário salvo com sucesso")
        except (ValueError, TypeError) as exc:
            self._mostrar_erro(str(exc))

    def _salvar_ordem(self):
        campos = self.tabs["ordens"]
        dados = {
            "id": self._campo("id", campos),
            "cliente_id": self._campo("cliente_id", campos),
            "veiculo_id": self._campo("veiculo_id", campos),
        }
        try:
            self.ordem_service.criar_ordem(
                int(dados["id"] or 0),
                int(dados["veiculo_id"]),
                int(dados["cliente_id"]),
            )
            self._limpar_campos(campos)
            self._atualizar_ordens()
            self._mostrar_sucesso("Ordem criada com sucesso")
        except (ValueError, TypeError) as exc:
            self._mostrar_erro(str(exc))

    def _iniciar_ordem(self):
        ordem_id = self._obter_selecao(self.ordens_lista)
        if not ordem_id:
            self._mostrar_erro("Selecione uma ordem na lista.")
            return
        try:
            self.ordem_service.iniciar_ordem(int(ordem_id))
            self._atualizar_ordens()
            self._mostrar_sucesso("Ordem iniciada")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _concluir_ordem(self):
        ordem_id = self._obter_selecao(self.ordens_lista)
        if not ordem_id:
            self._mostrar_erro("Selecione uma ordem na lista.")
            return
        try:
            self.ordem_service.concluir_ordem(int(ordem_id))
            self._atualizar_ordens()
            self._mostrar_sucesso("Ordem concluída")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _excluir_cliente(self):
        cliente_id = self._obter_selecao(self.clientes_lista)
        if not cliente_id:
            self._mostrar_erro("Selecione um cliente da lista.")
            return
        try:
            self.cliente_service.deletar_cliente(int(cliente_id))
            self._atualizar_clientes()
            self._mostrar_sucesso("Cliente removido")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _excluir_veiculo(self):
        veiculo_id = self._obter_selecao(self.veiculos_lista)
        if not veiculo_id:
            self._mostrar_erro("Selecione um veículo da lista.")
            return
        try:
            self.veiculo_service.deletar_veiculo(int(veiculo_id))
            self._atualizar_veiculos()
            self._mostrar_sucesso("Veículo removido")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _excluir_servico(self):
        servico_id = self._obter_selecao(self.servicos_lista)
        if not servico_id:
            self._mostrar_erro("Selecione um serviço da lista.")
            return
        try:
            self.servico_service.deletar_servico(int(servico_id))
            self._atualizar_servicos()
            self._mostrar_sucesso("Serviço removido")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _excluir_peca(self):
        peca_id = self._obter_selecao(self.pecas_lista)
        if not peca_id:
            self._mostrar_erro("Selecione uma peça da lista.")
            return
        try:
            self.peca_service.deletar_peca(int(peca_id))
            self._atualizar_pecas()
            self._mostrar_sucesso("Peça removida")
        except ValueError as exc:
            self._mostrar_erro(str(exc))

    def _excluir_funcionario(self):
        funcionario_id = self._obter_selecao(self.funcionarios_lista)
        if not funcionario_id:
            self._mostrar_erro("Selecione um funcionário da lista.")
            return
        try:
            self.funcionario_service.deletar_funcionario(int(funcionario_id))
            self._atualizar_funcionarios()
            self._mostrar_sucesso("Funcionário removido")
        except ValueError as exc:
            self._mostrar_erro(str(exc))


def launch_desktop():
    app = OficinaTechDesktopApp()
    app.mainloop()


if __name__ == "__main__":
    launch_desktop()
