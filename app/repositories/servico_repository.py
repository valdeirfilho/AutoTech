from app.models.servico import Servico


class ServicoRepository:
    def __init__(self, database):
        self.database = database

    def criar_tabelas(self):
        self.database.criar_tabelas()

    def salvar(self, s):
        c = self.database.cursor()
        dados = (s.descricao, s.valor)
        if s.id is None:
            c.execute("INSERT INTO servicos(descricao,valor) VALUES(?,?)", dados)
            s.id = c.lastrowid
        else:
            c.execute("UPDATE servicos SET descricao=?,valor=? WHERE id=?", (*dados, s.id))
            if not c.rowcount:
                raise ValueError(f"Serviço {s.id} não encontrado.")
        self.database.commit()
        return s

    @staticmethod
    def _obj(r):
        return Servico(r["descricao"], r["valor"], r["id"])

    def buscar_por_id(self, id):
        r = self.database.cursor().execute("SELECT * FROM servicos WHERE id=?", (id,)).fetchone()
        return self._obj(r) if r else None

    def buscar_todos(self):
        rows = self.database.cursor().execute("SELECT * FROM servicos ORDER BY descricao").fetchall()
        return [self._obj(r) for r in rows]

    def deletar(self, id):
        c = self.database.cursor()
        c.execute("DELETE FROM servicos WHERE id=?", (id,))
        if not c.rowcount:
            raise ValueError(f"Serviço {id} não encontrado.")
        self.database.commit()
