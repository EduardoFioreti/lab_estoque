from datetime import date
from sqlalchemy.orm import Session
from app import models


def verificar_alertas(db: Session) -> dict:
    """
    Função principal de varredura do banco de dados.
    Retorna um dicionário com três listas:
      - estoque_baixo: insumos abaixo do estoque mínimo
      - vencimento_critico: lotes que vencem em até 30 dias
      - vencimento_atencao: lotes que vencem entre 31 e 90 dias
    """
    alertas = {
        "estoque_baixo": [],
        "vencimento_critico": [],
        "vencimento_atencao": []
    }

    hoje = date.today()

    # ── BLOCO 1: Verificação de estoque baixo ──────────────────────────────
    # Para cada insumo, soma os lotes ativos e compara com o mínimo
    insumos = db.query(models.Insumo).all()

    for insumo in insumos:
        estoque_atual = sum(
            lote.quantidade
            for lote in insumo.lotes
            if not lote.consumido
        )

        if estoque_atual < insumo.estoque_minimo:
            alertas["estoque_baixo"].append({
                "insumo_id": insumo.id,
                "nome": insumo.nome,
                "tipo": insumo.tipo,
                "unidade": insumo.unidade,
                "estoque_atual": estoque_atual,
                "estoque_minimo": insumo.estoque_minimo,
                # Quanto precisa comprar para atingir o dobro do mínimo
                "quantidade_sugerida": (insumo.estoque_minimo * 2) - estoque_atual
            })

    # ── BLOCO 2: Verificação de validade ──────────────────────────────────
    # Busca apenas lotes ativos que têm data de validade definida
    lotes_ativos = (
        db.query(models.Lote)
        .filter(
            models.Lote.consumido == False,
            models.Lote.data_validade != None
        )
        .all()
    )

    for lote in lotes_ativos:
        dias_restantes = (lote.data_validade - hoje).days

        entrada = {
            "lote_id": lote.id,
            "numero_lote": lote.numero_lote,
            "insumo_nome": lote.insumo.nome,
            "quantidade": lote.quantidade,
            "unidade": lote.insumo.unidade,
            "data_validade": lote.data_validade.strftime("%d/%m/%Y"),
            "dias_restantes": dias_restantes
        }

        if dias_restantes <= 30:
            alertas["vencimento_critico"].append(entrada)
        elif dias_restantes <= 90:
            alertas["vencimento_atencao"].append(entrada)

    # Ordena cada lista pelo mais urgente primeiro
    alertas["estoque_baixo"].sort(key=lambda x: x["estoque_atual"])
    alertas["vencimento_critico"].sort(key=lambda x: x["dias_restantes"])
    alertas["vencimento_atencao"].sort(key=lambda x: x["dias_restantes"])

    return alertas


def gerar_lista_compras(db: Session) -> list:
    """
    Gera a lista de compras a partir dos insumos com estoque baixo.
    Reutiliza a lógica de verificar_alertas para não duplicar código.
    """
    alertas = verificar_alertas(db)
    return alertas["estoque_baixo"]