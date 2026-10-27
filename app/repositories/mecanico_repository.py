from app.models.mecanico import Mecanico


class MecanicoRepository:
    def __init__(self, database):
        self.database = database

    def criar_tabelas(self):
        self.database.criar_tabelas()

    def salvar(self, m):
        c = self.database.cursor()
        dados = (m.nome, m.especialidade)
        if m.id is None:
            c.execute("INSERT INTO mecanicos(nome,especialidade) VALUES(?,?)", dados)
            m.id = c.lastrowid
        else:
            c.execute("UPDATE mecanicos SET nome=?,especialidade=? WHERE id=?", (*dados, m.id))
            if not c.rowcount:
                raise ValueError(f"Mecânico {m.id} não encontrado.")
        self.database.commit()
        return m

    @staticmethod
    def _obj(r):
        return Mecanico(r["nome"], r["especialidade"], r["id"])

    def buscar_por_id(self, id):
        r = self.database.cursor().execute("SELECT * FROM mecanicos WHERE id=?", (id,)).fetchone()
        return self._obj(r) if r else None

    def buscar_todos(self):
        rows = self.database.cursor().execute("SELECT * FROM mecanicos ORDER BY nome").fetchall()
        return [self._obj(r) for r in rows]

    def deletar(self, id):
        c = self.database.cursor()
        c.execute("DELETE FROM mecanicos WHERE id=?", (id,))
        if not c.rowcount:
            raise ValueError(f"Mecânico {id} não encontrado.")
        self.database.commit()
