from app.models.peca import Peca


class PecaRepository:
    def __init__(self, database):
        self.database = database

    def criar_tabelas(self):
        self.database.criar_tabelas()

    def salvar(self, p):
        c = self.database.cursor()
        dados = (p.nome, p.valor, p.quantidade_estoque)
        if p.id is None:
            c.execute("INSERT INTO pecas(nome,valor,quantidade_estoque) VALUES(?,?,?)", dados)
            p.id = c.lastrowid
        else:
            c.execute("UPDATE pecas SET nome=?,valor=?,quantidade_estoque=? WHERE id=?",
                      (*dados, p.id))
            if not c.rowcount:
                raise ValueError(f"Peça {p.id} não encontrada.")
        self.database.commit()
        return p

    @staticmethod
    def _obj(r):
        return Peca(r["nome"], r["valor"], r["quantidade_estoque"], r["id"])

    def buscar_por_id(self, id):
        r = self.database.cursor().execute("SELECT * FROM pecas WHERE id=?", (id,)).fetchone()
        return self._obj(r) if r else None

    def buscar_todos(self):
        rows = self.database.cursor().execute("SELECT * FROM pecas ORDER BY nome").fetchall()
        return [self._obj(r) for r in rows]

    def atualizar_estoque(self, id, quantidade):
        p = self.buscar_por_id(id)
        if p is None:
            raise ValueError(f"Peça {id} não encontrada.")
        p.adicionar_ao_estoque(quantidade)
        return self.salvar(p)

    def deletar(self, id):
        c = self.database.cursor()
        c.execute("DELETE FROM pecas WHERE id=?", (id,))
        if not c.rowcount:
            raise ValueError(f"Peça {id} não encontrada.")
        self.database.commit()
