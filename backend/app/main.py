from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .auth import routes as auth_routes
from .dashboard import routes as dashboard_routes
from .reports import routes as reports_routes
from .alerts import routes as alerts_routes
from .predictions import routes as predictions_routes
from .consumption import routes as consumption_routes

# tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Energy App API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# incluindo as rotas
app.include_router(auth_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(reports_routes.router)
app.include_router(alerts_routes.router)
app.include_router(predictions_routes.router)
app.include_router(consumption_routes.router)

@app.get("/")
def root():
    return {"message": "API rodando! Vá até /docs para testar."}
