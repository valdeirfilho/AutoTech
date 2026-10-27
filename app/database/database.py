import sqlite3
from pathlib import Path
from contextlib import contextmanager


class Database:
    def __init__(self, caminho="oficina.db"):
        self.caminho = str(caminho)
        if self.caminho != ":memory:":
            Path(self.caminho).parent.mkdir(parents=True, exist_ok=True)
        self.conexao = sqlite3.connect(self.caminho)
        self.conexao.row_factory = sqlite3.Row
        self.conexao.execute("PRAGMA foreign_keys = ON")

    def cursor(self):
        return self.conexao.cursor()

    def commit(self):
        self.conexao.commit()

    def rollback(self):
        self.conexao.rollback()

    def criar_tabelas(self):
        self.conexao.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, telefone TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE, marca TEXT NOT NULL,
            modelo TEXT NOT NULL, ano INTEGER NOT NULL,
            cliente_id INTEGER NOT NULL REFERENCES clientes(id)
        );
        CREATE TABLE IF NOT EXISTS mecanicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, especialidade TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL, valor REAL NOT NULL CHECK(valor >= 0)
        );
        CREATE TABLE IF NOT EXISTS pecas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, valor REAL NOT NULL CHECK(valor >= 0),
            quantidade_estoque INTEGER NOT NULL CHECK(quantidade_estoque >= 0)
        );
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL REFERENCES clientes(id),
            veiculo_id INTEGER NOT NULL REFERENCES veiculos(id),
            mecanico_id INTEGER REFERENCES mecanicos(id),
            status TEXT NOT NULL, observacoes TEXT NOT NULL DEFAULT '',
            criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS ordem_servico_servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ordem_servico_id INTEGER NOT NULL REFERENCES ordens_servico(id) ON DELETE CASCADE,
            servico_id INTEGER NOT NULL REFERENCES servicos(id),
            valor_aplicado REAL NOT NULL CHECK(valor_aplicado >= 0)
        );
        CREATE TABLE IF NOT EXISTS ordem_servico_pecas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ordem_servico_id INTEGER NOT NULL REFERENCES ordens_servico(id) ON DELETE CASCADE,
            peca_id INTEGER NOT NULL REFERENCES pecas(id),
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            valor_unitario REAL NOT NULL CHECK(valor_unitario >= 0)
        );
        """)
        self.commit()

    @contextmanager
    def transacao(self):
        try:
            yield self.conexao.cursor()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def fechar(self):
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None
