import json
import os
import sqlite3
from abc import ABC, abstractmethod


class BaseRepository(ABC):
    def __init__(self, arquivo_dados, table_name, legacy_path=None):
        self.arquivo_dados = arquivo_dados
        self.table_name = table_name
        self.legacy_path = legacy_path or arquivo_dados
        self.db_path = self._resolve_db_path(arquivo_dados)
        self._assegurar_arquivo()
        self._migrar_json_se_necessario()

    def _resolve_db_path(self, arquivo_dados):
        if not arquivo_dados:
            return "data/autotech.db"
        if arquivo_dados.lower().endswith(".sqlite") or arquivo_dados.lower().endswith(".sqlite3") or arquivo_dados.lower().endswith(".db"):
            return arquivo_dados
        return arquivo_dados.rsplit(".", 1)[0] + ".db"

    def _conectar(self):
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _assegurar_arquivo(self):
        """Cria o banco SQLite se não existir"""
        conn = self._conectar()
        try:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def _migrar_json_se_necessario(self):
        """Importa dados antigos em JSON quando o banco estiver vazio."""
        conn = self._conectar()
        try:
            existe_registro = conn.execute(
                f"SELECT 1 FROM {self.table_name} LIMIT 1"
            ).fetchone()
        finally:
            conn.close()

        if existe_registro is not None or not os.path.exists(self.legacy_path):
            return

        try:
            with open(self.legacy_path, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self._salvar(dados)
        except (FileNotFoundError, json.JSONDecodeError):
            return

    def _carregar(self):
        """Carrega registros do banco SQLite em formato de dicionário."""
        conn = self._conectar()
        try:
            linhas = conn.execute(
                f"SELECT id, payload FROM {self.table_name}"
            ).fetchall()
        finally:
            conn.close()

        dados = {}
        for chave, payload in linhas:
            dados[str(chave)] = json.loads(payload)
        return dados

    def _salvar(self, dados):
        """Salva todos os registros no banco SQLite."""
        conn = self._conectar()
        try:
            conn.execute(f"DELETE FROM {self.table_name}")
            for chave, valor in dados.items():
                conn.execute(
                    f"INSERT INTO {self.table_name} (id, payload) VALUES (?, ?)",
                    (str(chave), json.dumps(valor, ensure_ascii=False))
                )
            conn.commit()
        finally:
            conn.close()

    @abstractmethod
    def salvar(self, entidade):
        pass

    @abstractmethod
    def obter_por_id(self, id):
        pass

    @abstractmethod
    def listar_todos(self):
        pass

    @abstractmethod
    def atualizar(self, entidade):
        pass

    @abstractmethod
    def deletar(self, id):
        pass
