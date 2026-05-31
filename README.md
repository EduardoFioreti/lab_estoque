# 🧪 Lab Estoque

Sistema web de gestão de estoque e automação de alertas para laboratórios, desenvolvido com **FastAPI**, **SQLite** e **Jinja2**.

🔗 **[Acesse o sistema online](https://lab-estoque-eduardo-fioreti.onrender.com/)**

> O plano gratuito hiberna após 15 minutos de inatividade. O primeiro acesso pode levar até 60 segundos para carregar.

---

## 📋 Funcionalidades

- 📦 **Cadastro de Insumos** — nome, tipo, estoque mínimo, unidade e link da FISPQ
- 🗃️ **Cadastro de Lotes** — número do lote, quantidade, data de recebimento e validade
- 🚨 **Painel de Alertas** — varredura automática do banco para identificar:
  - Estoques abaixo do mínimo
  - Lotes com vencimento crítico (até 30 dias)
  - Lotes com vencimento próximo (31 a 90 dias)
- 🛒 **Lista de Compras** — gerada automaticamente com sugestão de quantidade a repor
- 🗑️ **Baixa de Estoque** — marcação de lotes como consumidos

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) |
| Banco de Dados | SQLite com [SQLAlchemy](https://www.sqlalchemy.org/) |
| Templates | [Jinja2](https://jinja.palletsprojects.com/) |
| Frontend | HTML5 + CSS3 |
| Servidor | [Uvicorn](https://www.uvicorn.org/) |

---

## 📁 Estrutura do Projeto

```
lab_estoque/
├── requirements.txt
├── scripts/
│   └── verificar_estoque.py   # Lógica de alertas e lista de compras
└── app/
    ├── main.py                # Ponto de entrada da aplicação
    ├── database.py            # Configuração do SQLite + SQLAlchemy
    ├── models.py              # Modelos das tabelas (Insumo, Lote)
    ├── routers/
    │   ├── insumos.py         # Rotas de insumos
    │   ├── lotes.py           # Rotas de lotes
    │   └── alertas.py         # Rotas de alertas e compras
    ├── static/
    │   └── css/
    │       └── style.css
    └── templates/
        ├── base.html
        ├── index.html
        ├── insumos/
        │   ├── listar.html
        │   └── cadastrar.html
        ├── lotes/
        │   ├── listar.html
        │   └── cadastrar.html
        └── alertas/
            ├── painel.html
            └── compras.html
```

---

## 🚀 Como Rodar Localmente

**Pré-requisitos:** Python 3.10+

**1. Clone o repositório**
```bash
git clone https://github.com/EduardoFioreti/lab_estoque.git
cd lab_estoque
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Inicie o servidor**
```bash
uvicorn app.main:app --reload
```

**5. Acesse no navegador**
```
http://127.0.0.1:8000
```

O banco de dados SQLite (`lab_estoque.db`) é criado automaticamente na primeira execução.

---

## 🖥️ Telas do Sistema

| Rota | Descrição |
|---|---|
| `/` | Página inicial |
| `/insumos` | Listagem de insumos com status de estoque |
| `/insumos/cadastrar` | Formulário de cadastro de insumo |
| `/lotes` | Listagem de lotes com status de validade |
| `/lotes/cadastrar` | Formulário de cadastro de lote |
| `/alertas` | Painel de alertas automáticos |
| `/compras` | Lista de compras gerada automaticamente |

---

## ⚙️ Lógica de Alertas

A varredura é feita pelo script `scripts/verificar_estoque.py` que:

- Calcula o **estoque atual** de cada insumo somando todos os lotes não consumidos
- Compara com o **estoque mínimo** cadastrado
- Sugere quantidade de reposição equivalente ao **dobro do mínimo** menos o estoque atual
- Classifica lotes por proximidade do vencimento em três níveis: **OK**, **Atenção** e **Crítico**
