from app.models.veiculo import Veiculo


class VeiculoRepository:
    def __init__(self, database):
        self.database = database

    def criar_tabelas(self):
        self.database.criar_tabelas()

    def salvar(self, v):
        c = self.database.cursor()
        dados = (v.placa, v.marca, v.modelo, v.ano, v.cliente_id)
        if v.id is None:
            c.execute("INSERT INTO veiculos(placa,marca,modelo,ano,cliente_id) VALUES(?,?,?,?,?)", dados)
            v.id = c.lastrowid
        else:
            c.execute("UPDATE veiculos SET placa=?,marca=?,modelo=?,ano=?,cliente_id=? WHERE id=?",
                      (*dados, v.id))
            if not c.rowcount:
                raise ValueError(f"Veículo {v.id} não encontrado.")
        self.database.commit()
        return v

    @staticmethod
    def _obj(r):
        return Veiculo(r["placa"], r["marca"], r["modelo"], r["ano"], r["cliente_id"], r["id"])

    def buscar_por_id(self, id):
        r = self.database.cursor().execute("SELECT * FROM veiculos WHERE id=?", (id,)).fetchone()
        return self._obj(r) if r else None

    def buscar_por_placa(self, placa):
        r = self.database.cursor().execute("SELECT * FROM veiculos WHERE placa=?", (placa.strip().upper(),)).fetchone()
        return self._obj(r) if r else None

    def buscar_por_cliente(self, cliente_id):
        rows = self.database.cursor().execute("SELECT * FROM veiculos WHERE cliente_id=? ORDER BY placa",
                                               (cliente_id,)).fetchall()
        return [self._obj(r) for r in rows]

    def buscar_todos(self):
        rows = self.database.cursor().execute("SELECT * FROM veiculos ORDER BY placa").fetchall()
        return [self._obj(r) for r in rows]

    def deletar(self, id):
        c = self.database.cursor()
        c.execute("DELETE FROM veiculos WHERE id=?", (id,))
        if not c.rowcount:
            raise ValueError(f"Veículo {id} não encontrado.")
        self.database.commit()
