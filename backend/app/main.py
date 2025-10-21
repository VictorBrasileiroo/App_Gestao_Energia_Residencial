from fastapi import FastAPI
from .database import engine, Base
from . import models
from .auth import routes as auth_routes
from .dashboard import routes as dashboard_routes
from .reports import routes as reports_routes
from .alerts import routes as alerts_routes
from .predictions import routes as predictions_routes

# tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Energy App API")

# incluindo as rotas
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(reports_routes.router)
app.include_router(alerts_routes.router)
app.include_router(predictions_routes.router)

@app.get("/")
def root():
    return {"message": "API rodando! Vá até /docs para testar."}
