from app.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, database):
        self.database = database

    def criar_tabelas(self):
        self.database.criar_tabelas()

    def salvar(self, cliente):
        c = self.database.cursor()
        if cliente.id is None:
            c.execute("INSERT INTO clientes(nome, telefone) VALUES (?, ?)",
                      (cliente.nome, cliente.telefone))
            cliente.id = c.lastrowid
        else:
            c.execute("UPDATE clientes SET nome=?, telefone=? WHERE id=?",
                      (cliente.nome, cliente.telefone, cliente.id))
            if not c.rowcount:
                raise ValueError(f"Cliente {cliente.id} não encontrado.")
        self.database.commit()
        return cliente

    def buscar_por_id(self, id):
        r = self.database.cursor().execute(
            "SELECT * FROM clientes WHERE id=?", (id,)).fetchone()
        return Cliente(r["nome"], r["telefone"], r["id"]) if r else None

    def buscar_por_telefone(self, telefone):
        r = self.database.cursor().execute(
            "SELECT * FROM clientes WHERE telefone=?", (telefone,)).fetchone()
        return Cliente(r["nome"], r["telefone"], r["id"]) if r else None

    def buscar_todos(self):
        rows = self.database.cursor().execute("SELECT * FROM clientes ORDER BY nome").fetchall()
        return [Cliente(r["nome"], r["telefone"], r["id"]) for r in rows]

    def deletar(self, id):
        c = self.database.cursor()
        c.execute("DELETE FROM clientes WHERE id=?", (id,))
        if not c.rowcount:
            raise ValueError(f"Cliente {id} não encontrado.")
        self.database.commit()
