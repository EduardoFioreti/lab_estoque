# 🧪 Lab Estoque — Sistema Inteligente de Gestão de Estoque para Laboratórios

Sistema web desenvolvido para controle de estoque laboratorial, gerenciamento de lotes e monitoramento automático de validade de insumos.

O projeto foi construído utilizando **FastAPI**, **SQLAlchemy**, **SQLite** e **Jinja2**, aplicando conceitos de arquitetura web, modelagem de banco de dados, regras de negócio e automação de processos.

🔗 **Sistema Online:** https://lab-estoque-eduardo-fioreti.onrender.com/

> ⚠️ O plano gratuito do Render entra em modo de hibernação após períodos de inatividade. O primeiro acesso pode levar até 60 segundos para carregar.

---

## 🚀 Tecnologias Utilizadas

| Camada         | Tecnologia   |
| -------------- | ------------ |
| Backend        | FastAPI      |
| Banco de Dados | SQLite       |
| ORM            | SQLAlchemy   |
| Templates      | Jinja2       |
| Frontend       | HTML5 + CSS3 |
| Servidor ASGI  | Uvicorn      |
| Versionamento  | Git + GitHub |
| Deploy         | Render       |

---

## 📋 Funcionalidades

### 📦 Gestão de Insumos

* Cadastro de insumos laboratoriais
* Controle de estoque mínimo
* Registro de unidade de medida
* Armazenamento de link da FISPQ

### 🗃️ Gestão de Lotes

* Cadastro de lotes por insumo
* Controle de quantidade
* Registro de data de recebimento
* Controle de validade
* Baixa automática de estoque

### 🚨 Painel Inteligente de Alertas

O sistema realiza varredura automática do banco de dados para identificar:

* Estoque abaixo do mínimo
* Produtos próximos ao vencimento
* Produtos em estado crítico
* Necessidade de reposição

### 🛒 Lista de Compras Automática

* Sugestão automática de reposição
* Cálculo baseado no estoque mínimo
* Quantidade recomendada para compra

---

## 🏗️ Arquitetura da Aplicação

```text
Frontend (HTML + CSS + Jinja2)
            ↓
         FastAPI
            ↓
      SQLAlchemy ORM
            ↓
          SQLite
```

A aplicação foi estruturada utilizando separação de responsabilidades através de routers independentes, permitindo escalabilidade e manutenção simplificada.

---

## 📁 Estrutura do Projeto

```text
lab_estoque/
├── requirements.txt
├── scripts/
│   └── verificar_estoque.py
│
└── app/
    ├── main.py
    ├── database.py
    ├── models.py
    │
    ├── routers/
    │   ├── insumos.py
    │   ├── lotes.py
    │   └── alertas.py
    │
    ├── static/
    │   └── css/
    │       └── style.css
    │
    └── templates/
        ├── base.html
        ├── index.html
        ├── insumos/
        ├── lotes/
        └── alertas/
```

---

## ⚙️ Lógica de Negócio

A rotina principal do sistema é executada através do script:

```text
scripts/verificar_estoque.py
```

Responsável por:

* Calcular estoque atual de cada insumo
* Identificar itens abaixo do estoque mínimo
* Classificar lotes por proximidade de vencimento
* Gerar lista automática de compras
* Sugerir quantidades para reposição

### Critérios de Classificação

| Status     | Critério                        |
| ---------- | ------------------------------- |
| ✅ OK       | Mais de 90 dias para vencimento |
| ⚠️ Atenção | Entre 31 e 90 dias              |
| 🚨 Crítico | Até 30 dias para vencimento     |

---

## 💡 Desafios Técnicos Resolvidos

Durante o desenvolvimento foram aplicados conceitos de:

* Relacionamentos entre tabelas utilizando SQLAlchemy
* Arquitetura baseada em routers do FastAPI
* Regras de negócio para controle de estoque
* Manipulação de datas para cálculo de validade
* Geração dinâmica de alertas
* Persistência de dados utilizando ORM
* Organização de aplicações web escaláveis

---

## 🚀 Como Executar Localmente

### 1. Clonar o Repositório

```bash
git clone https://github.com/EduardoFioreti/lab_estoque.git

cd lab_estoque
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar o Projeto

```bash
uvicorn app.main:app --reload
```

### 5. Abrir no Navegador

```text
http://127.0.0.1:8000
```

O banco SQLite será criado automaticamente na primeira execução.

---

## 📸 Screenshots

Adicione aqui imagens do sistema:

### Dashboard

```text
screenshots/dashboard.png
```

### Painel de Alertas

```text
screenshots/alertas.png
```

### Lista de Compras

```text
screenshots/compras.png
```

---

## 🔮 Roadmap

* [ ] Autenticação de usuários
* [ ] Controle de permissões
* [ ] Dashboard com gráficos
* [ ] Exportação para Excel
* [ ] Envio automático de alertas por e-mail
* [ ] API REST documentada com Swagger
* [ ] Banco de dados PostgreSQL
* [ ] Dockerização da aplicação

---

## 👨‍💻 Autor

**Eduardo Fioreti**

🎓 Engenharia da Computação — UniCEUMA

🔗 GitHub: https://github.com/EduardoFioreti

💼 LinkedIn: https://linkedin.com/in/eduardo-fioreti-4a8931371

📧 E-mail: [eduardofioretidev@gmail.com](mailto:eduardofioretidev@gmail.com)
