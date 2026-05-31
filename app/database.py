from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o caminho do arquivo .db que será criado na raiz do projeto
DATABASE_URL = "sqlite:///./lab_estoque.db"

# O engine é o objeto que faz a conexão com o banco
# check_same_thread=False é necessário para o SQLite funcionar com FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cada instância de SessionLocal será uma sessão de conversa com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe pai que todos os nossos modelos vão herdar
Base = declarative_base()


# Função geradora usada nas rotas para abrir e fechar sessões com segurança
# O "yield" entrega a sessão para a rota, e o "finally" garante que ela
# sempre será fechada, mesmo se ocorrer um erro
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()