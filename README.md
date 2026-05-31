🧪 Lab Estoque
Sistema web de gestão de estoque e automação de alertas para laboratórios, desenvolvido com FastAPI, SQLite e Jinja2.

📋 Funcionalidades

📦 Cadastro de Insumos — nome, tipo, estoque mínimo, unidade e link da FISPQ
🗃️ Cadastro de Lotes — número do lote, quantidade, data de recebimento e validade
🚨 Painel de Alertas — varredura automática do banco para identificar:

Estoques abaixo do mínimo
Lotes com vencimento crítico (até 30 dias)
Lotes com vencimento próximo (31 a 90 dias)


🛒 Lista de Compras — gerada automaticamente com sugestão de quantidade a repor
🗑️ Baixa de Estoque — marcação de lotes como consumidos


🛠️ Tecnologias Utilizadas
CamadaTecnologiaBackendFastAPIBanco de DadosSQLite com SQLAlchemyTemplatesJinja2FrontendHTML5 + CSS3ServidorUvicorn

📁 Estrutura do Projeto
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

🚀 Como Rodar Localmente
Pré-requisitos: Python 3.10+
1. Clone o repositório
bashgit clone https://github.com/SEU_USUARIO/lab_estoque.git
cd lab_estoque
2. Crie e ative o ambiente virtual
bashpython -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
3. Instale as dependências
bashpip install -r requirements.txt
4. Inicie o servidor
bashuvicorn app.main:app --reload
5. Acesse no navegador
http://127.0.0.1:8000
O banco de dados SQLite (lab_estoque.db) é criado automaticamente na primeira execução.

🖥️ Telas do Sistema
RotaDescrição/Página inicial/insumosListagem de insumos com status de estoque/insumos/cadastrarFormulário de cadastro de insumo/lotesListagem de lotes com status de validade/lotes/cadastrarFormulário de cadastro de lote/alertasPainel de alertas automáticos/comprasLista de compras gerada automaticamente

⚙️ Lógica de Alertas
A varredura é feita pelo script scripts/verificar_estoque.py que:

Calcula o estoque atual de cada insumo somando todos os lotes não consumidos
Compara com o estoque mínimo cadastrado
Sugere quantidade de reposição equivalente ao dobro do mínimo menos o estoque atual
Classifica lotes por proximidade do vencimento em três níveis: OK, Atenção e Crítico


🌐 Deploy
O sistema está disponível em produção via Render:
🔗 https://lab-estoque-eduardo-fioreti.onrender.com/

O plano gratuito hiberna após 15 minutos de inatividade. O primeiro acesso pode levar até 60 segundos para carregar.
