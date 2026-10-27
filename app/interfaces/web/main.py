"""Interface web inicial do AutoTech. Execute: python -m app.interfaces.web.main"""
from pathlib import Path
from nicegui import ui

from app.database.database import Database
from app.services.oficina_service import OficinaService
from app.models.ordem_de_servico import StatusOrdem

ROOT = Path(__file__).resolve().parents[3]
database = Database(ROOT / "oficina.db")
service = OficinaService(database)

def brl(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def notify_error(exc):
    ui.notify(str(exc), type="negative", position="top")


def refresh_table(table, rows_fn, mapper):
    table.rows = [mapper(item) for item in rows_fn()]
    table.update()


def table_for(columns, rows=[]):
    return ui.table(columns=columns, rows=rows, row_key='id').classes('w-full').props('flat bordered dense')


@ui.page('/')
def home():
    # Configuração visual dentro da função da página para evitar UI global.
    ui.colors(primary="#2563eb", secondary="#475569", accent="#0f766e")
    ui.query('body').classes('bg-slate-100')
    with ui.header().classes('items-center justify-between bg-slate-900'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('build_circle', size='2rem').classes('text-blue-300')
            with ui.column().classes('gap-0'):
                ui.label('AutoTech').classes('text-xl font-bold text-white')
                ui.label('Gestão de oficina mecânica').classes('text-xs text-slate-300')
        ui.label('Versão inicial • Interface web').classes('text-sm text-slate-300')

    with ui.column().classes('w-full max-w-7xl mx-auto p-6 gap-5'):
        ui.label('Painel de controle').classes('text-2xl font-bold text-slate-800')
        ui.label('Cadastros e ordens de serviço em um só lugar.').classes('text-slate-500')
        cards = ui.row().classes('w-full gap-4 flex-wrap')
        def draw_cards():
            cards.clear()
            resumo = service.resumo()
            with cards:
                for titulo, valor, icone in [
                    ('Clientes', resumo['clientes'], 'groups'),
                    ('Veículos', resumo['veiculos'], 'directions_car'),
                    ('Mecânicos', resumo['mecanicos'], 'engineering'),
                    ('Ordens abertas/em andamento', resumo['ordens_abertas'], 'assignment'),
                ]:
                    with ui.card().classes('min-w-52 flex-grow shadow-sm'):
                        with ui.row().classes('items-center justify-between w-full'):
                            ui.label(titulo).classes('text-sm text-slate-500')
                            ui.icon(icone).classes('text-blue-600 text-xl')
                        ui.label(str(valor)).classes('text-3xl font-bold text-slate-800')
        draw_cards()

        with ui.tabs().classes('w-full') as tabs:
            tab_clientes = ui.tab('Clientes', icon='groups')
            tab_veiculos = ui.tab('Veículos', icon='directions_car')
            tab_mecanicos = ui.tab('Mecânicos', icon='engineering')
            tab_servicos = ui.tab('Serviços', icon='handyman')
            tab_pecas = ui.tab('Peças / estoque', icon='inventory_2')
            tab_ordens = ui.tab('Ordens de serviço', icon='assignment')
        with ui.tab_panels(tabs, value=tab_clientes).classes('w-full bg-transparent'):
            with ui.tab_panel(tab_clientes):
                with ui.card().classes('w-full'):
                    ui.label('Cadastrar cliente').classes('text-lg font-semibold')
                    with ui.row().classes('w-full items-end'):
                        cliente_nome = ui.input('Nome completo').classes('grow')
                        cliente_telefone = ui.input('Telefone').classes('grow')
                        tabela_clientes = table_for([
                            {'name':'id','label':'ID','field':'id','align':'left'},
                            {'name':'nome','label':'Nome','field':'nome','align':'left'},
                            {'name':'telefone','label':'Telefone','field':'telefone','align':'left'},
                        ])
                    def salvar_cliente():
                        try:
                            service.cadastrar_cliente(cliente_nome.value or '', cliente_telefone.value or '')
                            cliente_nome.value = ''; cliente_telefone.value = ''
                            refresh_table(tabela_clientes, service.clientes.buscar_todos,
                                          lambda x: {'id':x.id,'nome':x.nome,'telefone':x.telefone})
                            cliente_opts = {x.id: f'{x.nome} (#{x.id})' for x in service.clientes.buscar_todos()}
                            cliente_veiculo.options = cliente_opts; cliente_veiculo.update()
                            cliente_os.options = cliente_opts; cliente_os.update()
                            draw_cards(); ui.notify('Cliente cadastrado.', type='positive')
                        except Exception as exc: notify_error(exc)
                    ui.button('Salvar cliente', icon='save', on_click=salvar_cliente).classes('mt-2')
                    refresh_table(tabela_clientes, service.clientes.buscar_todos,
                                  lambda x: {'id':x.id,'nome':x.nome,'telefone':x.telefone})

            with ui.tab_panel(tab_veiculos):
                with ui.card().classes('w-full'):
                    ui.label('Cadastrar veículo').classes('text-lg font-semibold')
                    clientes = service.clientes.buscar_todos()
                    with ui.row().classes('w-full items-end'):
                        cliente_veiculo = ui.select({x.id: f'{x.nome} (#{x.id})' for x in clientes}, label='Proprietário').classes('grow')
                        placa = ui.input('Placa').classes('grow')
                        marca = ui.input('Marca').classes('grow')
                        modelo = ui.input('Modelo').classes('grow')
                        ano = ui.number('Ano', value=2022, min=1900, max=2100).classes('w-28')
                    tabela_veiculos = table_for([
                        {'name':'id','label':'ID','field':'id'}, {'name':'placa','label':'Placa','field':'placa'},
                        {'name':'veiculo','label':'Veículo','field':'veiculo'}, {'name':'ano','label':'Ano','field':'ano'},
                        {'name':'cliente','label':'Proprietário','field':'cliente'},
                    ])
                    def salvar_veiculo():
                        try:
                            if cliente_veiculo.value is None: raise ValueError('Cadastre e selecione um cliente primeiro.')
                            service.cadastrar_veiculo(placa.value or '', marca.value or '', modelo.value or '', int(ano.value), cliente_veiculo.value)
                            placa.value = ''; marca.value = ''; modelo.value = ''
                            refresh_table(tabela_veiculos, service.veiculos.buscar_todos, veiculo_row)
                            veiculo_os.options = {x.id:f'{x.placa} — {x.marca} {x.modelo}' for x in service.veiculos.buscar_todos()}
                            veiculo_os.update()
                            ui.notify('Veículo cadastrado.', type='positive')
                        except Exception as exc: notify_error(exc)
                    ui.button('Salvar veículo', icon='save', on_click=salvar_veiculo).classes('mt-2')
                    def veiculo_row(x):
                        dono = service.clientes.buscar_por_id(x.cliente_id)
                        return {'id':x.id,'placa':x.placa,'veiculo':f'{x.marca} {x.modelo}','ano':x.ano,'cliente':dono.nome if dono else '—'}
                    refresh_table(tabela_veiculos, service.veiculos.buscar_todos, veiculo_row)

            with ui.tab_panel(tab_mecanicos):
                with ui.card().classes('w-full'):
                    ui.label('Cadastrar mecânico').classes('text-lg font-semibold')
                    with ui.row().classes('w-full items-end'):
                        mecanico_nome = ui.input('Nome').classes('grow')
                        especialidade = ui.input('Especialidade').classes('grow')
                    tabela_mecanicos = table_for([{'name':'id','label':'ID','field':'id'}, {'name':'nome','label':'Nome','field':'nome'}, {'name':'especialidade','label':'Especialidade','field':'especialidade'}])
                    def salvar_mecanico():
                        try:
                            service.cadastrar_mecanico(mecanico_nome.value or '', especialidade.value or '')
                            mecanico_nome.value = ''; especialidade.value = ''
                            refresh_table(tabela_mecanicos, service.mecanicos.buscar_todos, lambda x:{'id':x.id,'nome':x.nome,'especialidade':x.especialidade})
                            mecanico_os.options = {x.id:f'{x.nome} — {x.especialidade}' for x in service.mecanicos.buscar_todos()}
                            mecanico_os.update()
                            draw_cards(); ui.notify('Mecânico cadastrado.', type='positive')
                        except Exception as exc: notify_error(exc)
                    ui.button('Salvar mecânico', icon='save', on_click=salvar_mecanico).classes('mt-2')
                    refresh_table(tabela_mecanicos, service.mecanicos.buscar_todos, lambda x:{'id':x.id,'nome':x.nome,'especialidade':x.especialidade})

            with ui.tab_panel(tab_servicos):
                with ui.card().classes('w-full'):
                    ui.label('Catálogo de serviços').classes('text-lg font-semibold')
                    with ui.row().classes('w-full items-end'):
                        descricao = ui.input('Descrição do serviço').classes('grow')
                        valor_servico = ui.number('Valor (R$)', value=0, min=0, format='%.2f').classes('w-48')
                    tabela_servicos = table_for([{'name':'id','label':'ID','field':'id'}, {'name':'descricao','label':'Descrição','field':'descricao'}, {'name':'valor','label':'Valor','field':'valor'}])
                    def salvar_servico():
                        try:
                            service.cadastrar_servico(descricao.value or '', valor_servico.value or 0)
                            descricao.value = ''; valor_servico.value = 0
                            refresh_table(tabela_servicos, service.servicos.buscar_todos, lambda x:{'id':x.id,'descricao':x.descricao,'valor':brl(x.valor)})
                            servicos_os.options = {x.id:f'{x.descricao} — {brl(x.valor)}' for x in service.servicos.buscar_todos()}
                            servicos_os.update()
                            ui.notify('Serviço cadastrado.', type='positive')
                        except Exception as exc: notify_error(exc)
                    ui.button('Salvar serviço', icon='save', on_click=salvar_servico).classes('mt-2')
                    refresh_table(tabela_servicos, service.servicos.buscar_todos, lambda x:{'id':x.id,'descricao':x.descricao,'valor':brl(x.valor)})

            with ui.tab_panel(tab_pecas):
                with ui.card().classes('w-full'):
                    ui.label('Peças e estoque').classes('text-lg font-semibold')
                    with ui.row().classes('w-full items-end'):
                        peca_nome = ui.input('Nome da peça').classes('grow')
                        valor_peca = ui.number('Valor unitário (R$)', value=0, min=0, format='%.2f').classes('w-48')
                        estoque = ui.number('Quantidade em estoque', value=0, min=0, precision=0).classes('w-48')
                    tabela_pecas = table_for([{'name':'id','label':'ID','field':'id'}, {'name':'nome','label':'Peça','field':'nome'}, {'name':'valor','label':'Valor','field':'valor'}, {'name':'estoque','label':'Estoque','field':'estoque'}])
                    def salvar_peca():
                        try:
                            service.cadastrar_peca(peca_nome.value or '', valor_peca.value or 0, int(estoque.value or 0))
                            peca_nome.value = ''; valor_peca.value = 0; estoque.value = 0
                            refresh_table(tabela_pecas, service.pecas.buscar_todos, lambda x:{'id':x.id,'nome':x.nome,'valor':brl(x.valor),'estoque':x.quantidade_estoque})
                            peca_os.options = {x.id:f'{x.nome} (estoque: {x.quantidade_estoque}) — {brl(x.valor)}' for x in service.pecas.buscar_todos()}
                            peca_os.update()
                            draw_cards(); ui.notify('Peça cadastrada.', type='positive')
                        except Exception as exc: notify_error(exc)
                    ui.button('Salvar peça', icon='save', on_click=salvar_peca).classes('mt-2')
                    refresh_table(tabela_pecas, service.pecas.buscar_todos, lambda x:{'id':x.id,'nome':x.nome,'valor':brl(x.valor),'estoque':x.quantidade_estoque})

            with ui.tab_panel(tab_ordens):
                with ui.card().classes('w-full'):
                    ui.label('Abrir ordem de serviço').classes('text-lg font-semibold')
                    clientes = service.clientes.buscar_todos()
                    veiculos = service.veiculos.buscar_todos()
                    mecanicos = service.mecanicos.buscar_todos()
                    servicos = service.servicos.buscar_todos()
                    pecas = service.pecas.buscar_todos()
                    with ui.row().classes('w-full items-end'):
                        cliente_os = ui.select({x.id:f'{x.nome} (#{x.id})' for x in clientes}, label='Cliente').classes('grow')
                        veiculo_os = ui.select({x.id:f'{x.placa} — {x.marca} {x.modelo}' for x in veiculos}, label='Veículo').classes('grow')
                        mecanico_os = ui.select({x.id:f'{x.nome} — {x.especialidade}' for x in mecanicos}, label='Mecânico (opcional)', clearable=True).classes('grow')
                    servicos_os = ui.select({x.id:f'{x.descricao} — {brl(x.valor)}' for x in servicos}, label='Serviços (selecione um ou mais)', multiple=True).classes('w-full')
                    with ui.row().classes('w-full items-end'):
                        peca_os = ui.select({x.id:f'{x.nome} (estoque: {x.quantidade_estoque}) — {brl(x.valor)}' for x in pecas}, label='Peça (opcional)', clearable=True).classes('grow')
                        qtd_os = ui.number('Quantidade', value=1, min=1, precision=0).classes('w-40')
                    observacoes_os = ui.textarea('Observações').classes('w-full')
                    tabela_ordens = table_for([
                        {'name':'id','label':'OS','field':'id'}, {'name':'status','label':'Status','field':'status'},
                        {'name':'cliente','label':'Cliente','field':'cliente'}, {'name':'veiculo','label':'Veículo','field':'veiculo'},
                        {'name':'total','label':'Total','field':'total'},
                    ])
                    def ordem_row(o):
                        c = service.clientes.buscar_por_id(o.cliente_id)
                        v = service.veiculos.buscar_por_id(o.veiculo_id)
                        return {'id':o.id,'status':o.status.value,'cliente':c.nome if c else '—',
                                'veiculo':f'{v.placa} — {v.modelo}' if v else '—','total':brl(o.calcular_total())}
                    def salvar_os():
                        try:
                            if cliente_os.value is None or veiculo_os.value is None:
                                raise ValueError('Selecione o cliente e o veículo.')
                            service.criar_ordem(cliente_os.value, veiculo_os.value, mecanico_os.value,
                                observacoes_os.value or '', servicos_os.value or [], peca_os.value,
                                int(qtd_os.value or 1))
                            observacoes_os.value = ''; servicos_os.value = []; peca_os.value = None; qtd_os.value = 1
                            refresh_table(tabela_ordens, service.ordens.buscar_todos, ordem_row)
                            draw_cards(); ui.notify('Ordem de serviço criada.', type='positive')
                        except Exception as exc: notify_error(exc)
                    ui.button('Abrir ordem de serviço', icon='add_task', on_click=salvar_os).classes('mt-2')
                    with ui.row().classes('items-end mt-4'):
                        id_status = ui.number('Número da OS para alterar status', min=1, precision=0).classes('w-64')
                        ui.button('Iniciar', on_click=lambda: alterar_status(id_status.value, StatusOrdem.EM_ANDAMENTO, tabela_ordens, ordem_row, draw_cards)).props('color=blue')
                        ui.button('Concluir', on_click=lambda: alterar_status(id_status.value, StatusOrdem.CONCLUIDA, tabela_ordens, ordem_row, draw_cards)).props('color=positive')
                        ui.button('Cancelar', on_click=lambda: alterar_status(id_status.value, StatusOrdem.CANCELADA, tabela_ordens, ordem_row, draw_cards)).props('color=negative')
                    refresh_table(tabela_ordens, service.ordens.buscar_todos, ordem_row)


def alterar_status(ordem_id, status, tabela, mapper, draw_cards):
    try:
        if ordem_id is None: raise ValueError('Informe o número da OS.')
        service.alterar_status_ordem(ordem_id, status)
        refresh_table(tabela, service.ordens.buscar_todos, mapper)
        draw_cards(); ui.notify('Status da ordem atualizado.', type='positive')
    except Exception as exc: notify_error(exc)


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='AutoTech | Oficina mecânica', host='127.0.0.1', port=8080, reload=False)
