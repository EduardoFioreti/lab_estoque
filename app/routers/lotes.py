from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app import models

router = APIRouter(prefix="/lotes", tags=["lotes"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def listar_lotes(
    request: Request,
    db: Session = Depends(get_db),
    mensagem: str = Query(None),
    tipo_mensagem: str = Query("sucesso")
):
    """
    Busca todos os lotes e faz o JOIN com a tabela de insumos
    para exibir o nome do insumo ao lado de cada lote.
    """
    lotes = db.query(models.Lote).all()

    # Calculamos os dias restantes para vencer diretamente aqui
    # para não poluir o template com lógica de negócio
    lotes_enriquecidos = []
    for lote in lotes:
        dias_para_vencer = None
        status_validade = "sem_validade"

        if lote.data_validade:
            dias_para_vencer = (lote.data_validade - date.today()).days
            if dias_para_vencer < 0:
                status_validade = "vencido"
            elif dias_para_vencer <= 30:
                status_validade = "critico"
            elif dias_para_vencer <= 90:
                status_validade = "atencao"
            else:
                status_validade = "ok"

        lotes_enriquecidos.append({
            "id": lote.id,
            "numero_lote": lote.numero_lote,
            "insumo_nome": lote.insumo.nome,
            "quantidade": lote.quantidade,
            "unidade": lote.insumo.unidade,
            "data_recebimento": lote.data_recebimento.strftime("%d/%m/%Y"),
            "data_validade": lote.data_validade.strftime("%d/%m/%Y") if lote.data_validade else None,
            "dias_para_vencer": dias_para_vencer,
            "status_validade": status_validade,
            "consumido": lote.consumido
        })

    return templates.TemplateResponse(
        request=request,
        name="lotes/listar.html",
        context={
            "lotes": lotes_enriquecidos,
            "mensagem": mensagem,
            "tipo_mensagem": tipo_mensagem
        }
    )


@router.get("/cadastrar")
def form_cadastrar(request: Request, db: Session = Depends(get_db)):
    """
    Renderiza o formulário de cadastro de lote.
    Precisa buscar os insumos no banco para popular o <select>.
    """
    insumos = db.query(models.Insumo).order_by(models.Insumo.nome).all()
    return templates.TemplateResponse(
        request=request,
        name="lotes/cadastrar.html",
        context={
            "insumos": insumos,
            "mensagem": None
        }
    )


@router.post("/cadastrar")
def cadastrar_lote(
    request: Request,
    insumo_id: int = Form(...),
    numero_lote: str = Form(...),
    quantidade: float = Form(...),
    data_recebimento: date = Form(...),
    data_validade: str = Form(""),    # string primeiro para validar se está vazio
    db: Session = Depends(get_db)
):
    """
    Processa o formulário e salva o lote no banco.
    A data_validade é opcional: se vier vazia, salva como None.
    """
    # Converte a string da data de validade para objeto date ou None
    validade_convertida = None
    if data_validade.strip():
        validade_convertida = date.fromisoformat(data_validade)

    novo_lote = models.Lote(
        insumo_id=insumo_id,
        numero_lote=numero_lote,
        quantidade=quantidade,
        data_recebimento=data_recebimento,
        data_validade=validade_convertida,
        consumido=False
    )
    db.add(novo_lote)
    db.commit()

    return RedirectResponse(
        url="/lotes?mensagem=Lote+cadastrado+com+sucesso!&tipo_mensagem=sucesso",
        status_code=303
    )


@router.post("/consumir/{lote_id}")
def consumir_lote(lote_id: int, db: Session = Depends(get_db)):
    """
    Marca um lote como consumido (baixa de estoque).
    Usamos POST em vez de DELETE para compatibilidade com formulários HTML puros.
    """
    lote = db.query(models.Lote).filter(models.Lote.id == lote_id).first()

    if lote:
        lote.consumido = True
        db.commit()

    return RedirectResponse(
        url="/lotes?mensagem=Lote+marcado+como+consumido!&tipo_mensagem=sucesso",
        status_code=303
    )