from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.models import StatusOrdem
from app.services import (
    ClienteService,
    FuncionarioService,
    OrdemServicoService,
    PecaService,
    ServicoService,
    VeiculoService,
)


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="OficinaTech API",
    version="1.0.0",
    description="API REST para gerenciamento de oficina mecânica",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web")), name="static")

cliente_service = ClienteService()
veiculo_service = VeiculoService()
servico_service = ServicoService()
peca_service = PecaService()
funcionario_service = FuncionarioService()
ordem_service = OrdemServicoService()


class ClienteCreate(BaseModel):
    id: int
    nome: str
    telefone: str


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None


class VeiculoCreate(BaseModel):
    id: int
    placa: str
    modelo: str
    ano: int
    cliente_id: int


class VeiculoUpdate(BaseModel):
    placa: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None


class ServicoCreate(BaseModel):
    id: int
    nome: str
    descricao: str
    valor: float


class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None


class PecaCreate(BaseModel):
    id: int
    nome: str
    descricao: str
    valor: float
    quantidade_estoque: int


class PecaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None


class FuncionarioCreate(BaseModel):
    id: int
    nome: str
    cargo: str
    telefone: str


class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    telefone: Optional[str] = None


class OrdemCreate(BaseModel):
    id: int
    veiculo_id: int
    cliente_id: int


class OrdemStatusUpdate(BaseModel):
    status: str


class EstoqueUpdate(BaseModel):
    quantidade: int


def cliente_to_dict(cliente):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "veiculos_ids": [veiculo.id for veiculo in cliente.veiculos],
    }


def veiculo_to_dict(veiculo):
    return {
        "id": veiculo.id,
        "placa": veiculo.placa,
        "modelo": veiculo.modelo,
        "ano": veiculo.ano,
        "cliente_id": veiculo.cliente_id,
        "ordens_ids": [ordem.id for ordem in veiculo.ordens],
    }


def servico_to_dict(servico):
    return {
        "id": servico.id,
        "nome": servico.nome,
        "descricao": servico.descricao,
        "valor": servico.valor,
    }


def peca_to_dict(peca):
    return {
        "id": peca.id,
        "nome": peca.nome,
        "descricao": peca.descricao,
        "valor": peca.valor,
        "quantidade_estoque": peca.quantidade_estoque,
    }


def funcionario_to_dict(funcionario):
    return {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "cargo": funcionario.cargo,
        "telefone": funcionario.telefone,
    }


def ordem_to_dict(ordem):
    return {
        "id": ordem.id,
        "veiculo_id": ordem.veiculo_id,
        "cliente_id": ordem.cliente_id,
        "data_abertura": ordem.data_abertura.isoformat(),
        "data_conclusao": ordem.data_conclusao.isoformat() if ordem.data_conclusao else None,
        "status": ordem.status.value,
        "servicos": [servico_to_dict(servico) for servico in ordem.servicos],
        "pecas": [peca_to_dict(peca) for peca in ordem.pecas],
        "funcionario_id": ordem.funcionario_id,
        "observacoes": ordem.observacoes,
        "valor_total": ordem.calcular_valor_total(),
    }


@app.get("/")
def root_page():
    return FileResponse(BASE_DIR / "web" / "index.html")


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "oficina-tech"}


@app.post("/clientes", status_code=status.HTTP_201_CREATED)
def criar_cliente(payload: ClienteCreate):
    try:
        cliente = cliente_service.criar_cliente(payload.id, payload.nome, payload.telefone)
        return cliente_to_dict(cliente)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/clientes")
def listar_clientes():
    return [cliente_to_dict(cliente) for cliente in cliente_service.listar_clientes()]


@app.get("/clientes/{cliente_id}")
def obter_cliente(cliente_id: int):
    try:
        return cliente_to_dict(cliente_service.obter_cliente(cliente_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.put("/clientes/{cliente_id}")
def atualizar_cliente(cliente_id: int, payload: ClienteUpdate):
    try:
        cliente = cliente_service.atualizar_cliente(
            cliente_id,
            nome=payload.nome,
            telefone=payload.telefone,
        )
        return cliente_to_dict(cliente)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int):
    try:
        cliente_service.deletar_cliente(cliente_id)
        return {"message": "Cliente removido com sucesso"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.post("/veiculos", status_code=status.HTTP_201_CREATED)
def criar_veiculo(payload: VeiculoCreate):
    try:
        veiculo = veiculo_service.criar_veiculo(
            payload.id,
            payload.placa,
            payload.modelo,
            payload.ano,
            payload.cliente_id,
        )
        return veiculo_to_dict(veiculo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/veiculos")
def listar_veiculos():
    return [veiculo_to_dict(veiculo) for veiculo in veiculo_service.listar_veiculos()]


@app.get("/veiculos/{veiculo_id}")
def obter_veiculo(veiculo_id: int):
    try:
        return veiculo_to_dict(veiculo_service.obter_veiculo(veiculo_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.get("/veiculos/placa/{placa}")
def obter_veiculo_por_placa(placa: str):
    try:
        return veiculo_to_dict(veiculo_service.obter_por_placa(placa))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.put("/veiculos/{veiculo_id}")
def atualizar_veiculo(veiculo_id: int, payload: VeiculoUpdate):
    try:
        veiculo = veiculo_service.atualizar_veiculo(
            veiculo_id,
            placa=payload.placa,
            modelo=payload.modelo,
            ano=payload.ano,
        )
        return veiculo_to_dict(veiculo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.delete("/veiculos/{veiculo_id}")
def deletar_veiculo(veiculo_id: int):
    try:
        veiculo_service.deletar_veiculo(veiculo_id)
        return {"message": "Veículo removido com sucesso"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.post("/servicos", status_code=status.HTTP_201_CREATED)
def criar_servico(payload: ServicoCreate):
    try:
        servico = servico_service.criar_servico(
            payload.id,
            payload.nome,
            payload.descricao,
            payload.valor,
        )
        return servico_to_dict(servico)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/servicos")
def listar_servicos():
    return [servico_to_dict(servico) for servico in servico_service.listar_servicos()]


@app.get("/servicos/{servico_id}")
def obter_servico(servico_id: int):
    try:
        return servico_to_dict(servico_service.obter_servico(servico_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.put("/servicos/{servico_id}")
def atualizar_servico(servico_id: int, payload: ServicoUpdate):
    try:
        servico = servico_service.atualizar_servico(
            servico_id,
            nome=payload.nome,
            descricao=payload.descricao,
            valor=payload.valor,
        )
        return servico_to_dict(servico)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.delete("/servicos/{servico_id}")
def deletar_servico(servico_id: int):
    try:
        servico_service.deletar_servico(servico_id)
        return {"message": "Serviço removido com sucesso"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.post("/pecas", status_code=status.HTTP_201_CREATED)
def criar_peca(payload: PecaCreate):
    try:
        peca = peca_service.criar_peca(
            payload.id,
            payload.nome,
            payload.descricao,
            payload.valor,
            payload.quantidade_estoque,
        )
        return peca_to_dict(peca)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/pecas")
def listar_pecas():
    return [peca_to_dict(peca) for peca in peca_service.listar_pecas()]


@app.get("/pecas/{peca_id}")
def obter_peca(peca_id: int):
    try:
        return peca_to_dict(peca_service.obter_peca(peca_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.put("/pecas/{peca_id}")
def atualizar_peca(peca_id: int, payload: PecaUpdate):
    try:
        peca = peca_service.atualizar_peca(
            peca_id,
            nome=payload.nome,
            descricao=payload.descricao,
            valor=payload.valor,
        )
        return peca_to_dict(peca)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.patch("/pecas/{peca_id}/estoque")
def atualizar_estoque_peca(peca_id: int, payload: EstoqueUpdate):
    try:
        if payload.quantidade >= 0:
            peca = peca_service.adicionar_estoque(peca_id, payload.quantidade)
        else:
            peca = peca_service.remover_estoque(peca_id, abs(payload.quantidade))
        return peca_to_dict(peca)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.delete("/pecas/{peca_id}")
def deletar_peca(peca_id: int):
    try:
        peca_service.deletar_peca(peca_id)
        return {"message": "Peça removida com sucesso"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.post("/funcionarios", status_code=status.HTTP_201_CREATED)
def criar_funcionario(payload: FuncionarioCreate):
    try:
        funcionario = funcionario_service.criar_funcionario(
            payload.id,
            payload.nome,
            payload.cargo,
            payload.telefone,
        )
        return funcionario_to_dict(funcionario)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/funcionarios")
def listar_funcionarios():
    return [funcionario_to_dict(funcionario) for funcionario in funcionario_service.listar_funcionarios()]


@app.get("/funcionarios/{funcionario_id}")
def obter_funcionario(funcionario_id: int):
    try:
        return funcionario_to_dict(funcionario_service.obter_funcionario(funcionario_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.put("/funcionarios/{funcionario_id}")
def atualizar_funcionario(funcionario_id: int, payload: FuncionarioUpdate):
    try:
        funcionario = funcionario_service.atualizar_funcionario(
            funcionario_id,
            nome=payload.nome,
            cargo=payload.cargo,
            telefone=payload.telefone,
        )
        return funcionario_to_dict(funcionario)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.delete("/funcionarios/{funcionario_id}")
def deletar_funcionario(funcionario_id: int):
    try:
        funcionario_service.deletar_funcionario(funcionario_id)
        return {"message": "Funcionário removido com sucesso"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.post("/ordens", status_code=status.HTTP_201_CREATED)
def criar_ordem(payload: OrdemCreate):
    try:
        ordem = ordem_service.criar_ordem(payload.id, payload.veiculo_id, payload.cliente_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/ordens")
def listar_ordens():
    return [ordem_to_dict(ordem) for ordem in ordem_service.listar_ordens()]


@app.get("/ordens/{ordem_id}")
def obter_ordem(ordem_id: int):
    try:
        return ordem_to_dict(ordem_service.obter_ordem(ordem_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.get("/ordens/status/{status}")
def listar_ordens_por_status(status: str):
    try:
        ordens = ordem_service.listar_ordens_status(status)
        return [ordem_to_dict(ordem) for ordem in ordens]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.post("/ordens/{ordem_id}/servicos/{servico_id}")
def adicionar_servico_ordem(ordem_id: int, servico_id: int):
    try:
        ordem = ordem_service.adicionar_servico(ordem_id, servico_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.post("/ordens/{ordem_id}/pecas/{peca_id}")
def adicionar_peca_ordem(ordem_id: int, peca_id: int):
    try:
        ordem = ordem_service.adicionar_peca(ordem_id, peca_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.post("/ordens/{ordem_id}/funcionarios/{funcionario_id}")
def atribuir_funcionario_ordem(ordem_id: int, funcionario_id: int):
    try:
        ordem = ordem_service.atribuir_funcionario(ordem_id, funcionario_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.post("/ordens/{ordem_id}/iniciar")
def iniciar_ordem(ordem_id: int):
    try:
        ordem = ordem_service.iniciar_ordem(ordem_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.post("/ordens/{ordem_id}/concluir")
def concluir_ordem(ordem_id: int):
    try:
        ordem = ordem_service.concluir_ordem(ordem_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.post("/ordens/{ordem_id}/cancelar")
def cancelar_ordem(ordem_id: int):
    try:
        ordem = ordem_service.cancelar_ordem(ordem_id)
        return ordem_to_dict(ordem)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@app.get("/ordens/cliente/{cliente_id}")
def listar_ordens_cliente(cliente_id: int):
    try:
        return [ordem_to_dict(ordem) for ordem in ordem_service.listar_ordens_cliente(cliente_id)]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@app.get("/ordens/veiculo/{veiculo_id}")
def listar_ordens_veiculo(veiculo_id: int):
    try:
        return [ordem_to_dict(ordem) for ordem in ordem_service.listar_ordens_veiculo(veiculo_id)]
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
