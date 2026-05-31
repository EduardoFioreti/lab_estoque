from app.database import engine, Base
from app import models 

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

print("Banco de dados criado com sucesso!")
print("Tabelas:", list(Base.metadata.tables.keys()))