from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from scripts.verificar_estoque import verificar_alertas, gerar_lista_compras

router = APIRouter(tags=["alertas"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/alertas")
def painel_alertas(request: Request, db: Session = Depends(get_db)):
    """
    Chama o script de varredura e passa os resultados para o template.
    A rota não tem lógica de negócio — apenas orquestra.
    """
    alertas = verificar_alertas(db)

    total_alertas = (
        len(alertas["estoque_baixo"]) +
        len(alertas["vencimento_critico"]) +
        len(alertas["vencimento_atencao"])
    )

    return templates.TemplateResponse(
        request=request,
        name="alertas/painel.html",
        context={
            "alertas": alertas,
            "total_alertas": total_alertas
        }
    )


@router.get("/compras")
def lista_compras(request: Request, db: Session = Depends(get_db)):
    """
    Exibe apenas os itens que precisam ser comprados.
    """
    itens = gerar_lista_compras(db)

    return templates.TemplateResponse(
        request=request,
        name="alertas/compras.html",
        context={"itens": itens}
    )