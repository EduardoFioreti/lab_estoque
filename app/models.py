from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Insumo(Base):
    """
    Representa um produto/insumo cadastrado no laboratório.
    Ex: "Ácido Sulfúrico", "Luvas de Nitrila", etc.
    """
    __tablename__ = "insumos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)        # Ex: "Reagente", "EPI", "Vidraria"
    estoque_minimo = Column(Float, nullable=False)
    unidade = Column(String, nullable=False)     # Ex: "L", "kg", "unidade"
    link_fispq = Column(String, nullable=True)   # Link externo, pode ser vazio

    # Um insumo pode ter vários lotes associados
    lotes = relationship("Lote", back_populates="insumo")


class Lote(Base):
    """
    Representa uma entrada de estoque: uma carga recebida de um insumo.
    Ex: 5 litros do Ácido Sulfúrico recebidos em 01/06/2025.
    """
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    numero_lote = Column(String, nullable=False)
    quantidade = Column(Float, nullable=False)
    data_recebimento = Column(Date, nullable=False)
    data_validade = Column(Date, nullable=True)   # Alguns insumos não vencem
    consumido = Column(Boolean, default=False)    # Para controle de baixa futura

    # Chave estrangeira: todo lote pertence a um insumo
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=False)

    # Acesso direto ao objeto Insumo a partir do Lote
    insumo = relationship("Insumo", back_populates="lotes")