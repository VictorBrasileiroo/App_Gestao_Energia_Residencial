from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models import ConsumptionDaily, TariffPlan, Prediction

def get_report_summary(db: Session, user_id: int):
    today = date.today()
    first_day_month = today.replace(day=1)

    # Pega consumo diário do usuário
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    data_last_7 = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= last_7_days
    ).all()

    data_last_30 = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= last_30_days
    ).all()

    data_current_month = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= first_day_month
    ).all()

    # Cálculos
    energy_7 = sum(r.energy_kwh for r in data_last_7)
    energy_30 = sum(r.energy_kwh for r in data_last_30)
    energy_month = sum(r.energy_kwh for r in data_current_month)

    # Tarifa
    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 1.0

    cost_7 = energy_7 * price
    cost_30 = energy_30 * price
    cost_month = energy_month * price

    # Previsão (opcional)
    prediction = db.query(Prediction).filter_by(user_id=user_id).order_by(Prediction.generated_at.desc()).first()
    pred_dict = None
    if prediction:
        pred_dict = {
            "target_month": prediction.target_month,
            "energy_kwh_pred": prediction.energy_kwh_pred,
            "cost_pred": prediction.cost_pred,
            "confidence_low_kwh": prediction.confidence_low_kwh,
            "confidence_high_kwh": prediction.confidence_high_kwh
        }

    return {
        "energy_last_7_days_kwh": round(energy_7, 2),
        "energy_last_30_days_kwh": round(energy_30, 2),
        "energy_current_month_kwh": round(energy_month, 2),
        "cost_last_7_days": round(cost_7, 2),
        "cost_last_30_days": round(cost_30, 2),
        "cost_current_month": round(cost_month, 2),
        "tariff_price_per_kwh": price,
        "prediction": pred_dict
    }
