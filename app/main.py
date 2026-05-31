from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import insumos, lotes, alertas     # ← ADICIONADO ALERTAS AQUI!

app = FastAPI(title="Lab Estoque")

# Registra a pasta de arquivos estáticos (CSS, imagens, JS futuros)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registra a pasta de templates Jinja2
templates = Jinja2Templates(directory="app/templates")

app.include_router(insumos.router)
app.include_router(lotes.router)
app.include_router(alertas.router)                  # ← LINHA NOVA DO CLAUDE


@app.get("/")
def pagina_inicial(request: Request):
    """Rota raiz: renderiza a página de boas-vindas."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"mensagem": None}
    )