from fastapi import APIRouter, Request, Depends, Form, Query   # ← ADICIONAMOS O Query AQUI!
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/insumos", tags=["insumos"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def listar_insumos(
    request: Request, 
    db: Session = Depends(get_db),
    mensagem: str = Query(None),           # ← LINHA NOVA: Agora o Python lê a mensagem da URL!
    tipo_mensagem: str = Query("sucesso")  # ← LINHA NOVA: Lê o tipo da mensagem!
):
    """
    Busca todos os insumos no banco e calcula o estoque atual de cada um.
    O estoque atual é a soma das quantidades de todos os lotes não consumidos.
    """
    insumos = db.query(models.Insumo).all()

    # Para cada insumo, calculamos o estoque atual somando os lotes ativos
    insumos_com_estoque = []
    for insumo in insumos:
        estoque_atual = sum(
            lote.quantidade
            for lote in insumo.lotes
            if not lote.consumido
        )
        insumos_com_estoque.append({
            "id": insumo.id,
            "nome": insumo.nome,
            "tipo": insumo.tipo,
            "unidade": insumo.unidade,
            "estoque_minimo": insumo.estoque_minimo,
            "estoque_atual": estoque_atual,
            "link_fispq": insumo.link_fispq,
            # Flag para colorir a linha na tabela quando estoque estiver baixo
            "estoque_baixo": estoque_atual < insumo.estoque_minimo
        })

    return templates.TemplateResponse(
        request=request,
        name="insumos/listar.html",
        context={
            "insumos": insumos_com_estoque,
            "mensagem": mensagem,           # ← PASSANDO A MENSAGEM PARA O HTML!
            "tipo_mensagem": tipo_mensagem  # ← PASSANDO O TIPO PARA O HTML!
        }
    )


@router.get("/cadastrar")
def form_cadastrar(request: Request):
    """Renderiza o formulário em branco para cadastro de novo insumo."""
    return templates.TemplateResponse(
        request=request,
        name="insumos/cadastrar.html",
        context={"mensagem": None}
    )


@router.post("/cadastrar")
def cadastrar_insumo(
    request: Request,
    nome: str = Form(...),
    tipo: str = Form(...),
    unidade: str = Form(...),
    estoque_minimo: float = Form(...),
    link_fispq: str = Form(""),   # campo opcional, padrão vazio
    db: Session = Depends(get_db)
):
    """
    Recebe os dados do formulário HTML via POST,
    cria o objeto e salva no banco de dados.
    """
    novo_insumo = models.Insumo(
        nome=nome,
        tipo=tipo,
        unidade=unidade,
        estoque_minimo=estoque_minimo,
        link_fispq=link_fispq if link_fispq.strip() else None
    )
    db.add(novo_insumo)
    db.commit()

    # Após salvar, redireciona para a listagem com mensagem de sucesso
    return RedirectResponse(
        url="/insumos?mensagem=Insumo+cadastrado+com+sucesso!&tipo_mensagem=sucesso",
        status_code=303
    )