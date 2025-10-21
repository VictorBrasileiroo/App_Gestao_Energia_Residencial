# app/predictions/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..auth.routes import get_current_user
from .job import generate_prediction_for_user
from .. import models

router = APIRouter(prefix="/predictions", tags=["Predictions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/latest")
def latest(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    pred = db.query(models.Prediction).filter(models.Prediction.user_id == current_user.id).order_by(models.Prediction.generated_at.desc()).first()
    if not pred:
        return {"message": "Nenhuma predição disponível"}
    return {
        "target_month": pred.target_month,
        "energy_kwh_pred": pred.energy_kwh_pred,
        "cost_brl_pred": pred.cost_pred,
        "confidence_interval_kwh": [pred.confidence_low_kwh, pred.confidence_high_kwh],
        "generated_at": pred.generated_at.isoformat()
    }

@router.post("/generate")
def generate_now(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    pred = generate_prediction_for_user(db, current_user.id)
    if not pred:
        return {"message": "Não foi possível gerar predição (dados insuficientes)"}
    return {"message": "Predição gerada", "prediction_id": pred.id}
