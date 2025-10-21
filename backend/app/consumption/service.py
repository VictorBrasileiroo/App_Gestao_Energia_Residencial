from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from ..models import ConsumptionDaily, TariffPlan, Prediction
from fastapi import UploadFile
from .upload import process_csv

def process_and_save_consumption(db: Session, user_id: int, file: UploadFile):
    """Processa arquivo CSV de consumo e salva no banco"""
    return process_csv(user_id, file, db)

def generate_prediction(db: Session, user_id: int):
    today = date.today()
    target_month = (today.replace(day=1) + timedelta(days=32)).strftime("%Y-%m")

    # pega os ultimos 3 meses
    cutoff = today - timedelta(days=90)
    data = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= cutoff
    ).all()

    if not data:
        return None

    avg_kwh = sum(r.energy_kwh for r in data) / len(data)
    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 1.0
    cost_pred = avg_kwh * 30 * price  # previsão simples

    pred = Prediction(
        user_id=user_id,
        target_month=target_month,
        energy_kwh_pred=avg_kwh * 30,
        cost_pred=cost_pred,
        confidence_low_kwh=avg_kwh * 28,
        confidence_high_kwh=avg_kwh * 32,
        generated_at=datetime.utcnow()
    )

    db.add(pred)
    db.commit()
    return pred
