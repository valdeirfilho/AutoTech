from app.models.ordem_de_servico import OrdemDeServico, StatusOrdem
from app.repositories.servico_repository import ServicoRepository
from app.repositories.peca_repository import PecaRepository


class OrdemDeServicoRepository:
    def __init__(self, database):
        self.database = database
        self.servicos = ServicoRepository(database)
        self.pecas = PecaRepository(database)

    def criar_tabelas(self):
        self.database.criar_tabelas()

    def salvar(self, ordem):
        # A OS e seus itens são gravados atomicamente: ou tudo é salvo, ou nada.
        with self.database.transacao() as c:
            if ordem.id is None:
                c.execute("""INSERT INTO ordens_servico
                    (cliente_id,veiculo_id,mecanico_id,status,observacoes)
                    VALUES(?,?,?,?,?)""",
                    (ordem.cliente_id, ordem.veiculo_id, ordem.mecanico_id,
                     ordem.status.value, ordem.observacoes))
                ordem.id = c.lastrowid
            else:
                c.execute("""UPDATE ordens_servico SET cliente_id=?,veiculo_id=?,
                    mecanico_id=?,status=?,observacoes=? WHERE id=?""",
                    (ordem.cliente_id, ordem.veiculo_id, ordem.mecanico_id,
                     ordem.status.value, ordem.observacoes, ordem.id))
                if not c.rowcount:
                    raise ValueError(f"OS {ordem.id} não encontrada.")
                c.execute("DELETE FROM ordem_servico_servicos WHERE ordem_servico_id=?", (ordem.id,))
                c.execute("DELETE FROM ordem_servico_pecas WHERE ordem_servico_id=?", (ordem.id,))

            for s, valor in zip(ordem.servicos, ordem.valores_servicos):
                c.execute("""INSERT INTO ordem_servico_servicos
                    (ordem_servico_id,servico_id,valor_aplicado) VALUES(?,?,?)""",
                    (ordem.id, s.id, valor))
            for p, qtd, valor in zip(ordem.pecas, ordem.quantidades_pecas, ordem.valores_pecas):
                c.execute("""INSERT INTO ordem_servico_pecas
                    (ordem_servico_id,peca_id,quantidade,valor_unitario) VALUES(?,?,?,?)""",
                    (ordem.id, p.id, qtd, valor))
        return ordem

    def _montar(self, r):
        # Monta os itens antes de restaurar o status final, pois OS concluídas
        # ou canceladas não aceitam inclusão de novos itens pelo domínio.
        os = OrdemDeServico(r["cliente_id"], r["veiculo_id"], r["mecanico_id"],
                            r["id"], StatusOrdem.ABERTA, r["observacoes"])
        c = self.database.cursor()
        rows = c.execute("""SELECT servico_id,valor_aplicado FROM ordem_servico_servicos
                            WHERE ordem_servico_id=? ORDER BY id""", (os.id,)).fetchall()
        for item in rows:
            s = self.servicos.buscar_por_id(item["servico_id"])
            if s:
                os.adicionar_servico(s, item["valor_aplicado"])
        rows = c.execute("""SELECT peca_id,quantidade,valor_unitario FROM ordem_servico_pecas
                            WHERE ordem_servico_id=? ORDER BY id""", (os.id,)).fetchall()
        for item in rows:
            p = self.pecas.buscar_por_id(item["peca_id"])
            if p:
                os.adicionar_peca(p, item["quantidade"], item["valor_unitario"])
        os.status = StatusOrdem(r["status"])
        return os

    def buscar_por_id(self, id):
        r = self.database.cursor().execute("SELECT * FROM ordens_servico WHERE id=?", (id,)).fetchone()
        return self._montar(r) if r else None

    def buscar_todos(self):
        rows = self.database.cursor().execute("SELECT * FROM ordens_servico ORDER BY id DESC").fetchall()
        return [self._montar(r) for r in rows]

    def deletar(self, id):
        c = self.database.cursor()
        c.execute("DELETE FROM ordens_servico WHERE id=?", (id,))
        if not c.rowcount:
            raise ValueError(f"OS {id} não encontrada.")
        self.database.commit()
