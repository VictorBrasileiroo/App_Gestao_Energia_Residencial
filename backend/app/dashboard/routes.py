from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from ..database import SessionLocal
from ..models import ConsumptionDaily, ConsumptionHourly, TariffPlan, Prediction, Alert
from ..auth.routes import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_dashboard(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    today = date.today()
    yesterday = today - timedelta(days=1)

    # tarifa e o preco por kwh
    tariff = db.query(TariffPlan).filter(TariffPlan.user_id == user_id).first()
    price = tariff.price_per_kwh if tariff else 1.0

    # record de dados de 'hoje' e de 'ontem'
    today_record = db.query(ConsumptionDaily).filter_by(user_id=user_id, date=today).first()
    yesterday_record = db.query(ConsumptionDaily).filter_by(user_id=user_id, date=yesterday).first()

    # kwh gastos 'hoje' e 'ontem'
    today_kwh = today_record.energy_kwh if today_record else 0
    yesterday_kwh = yesterday_record.energy_kwh if yesterday_record else 0

    # comparacao entre a energia gasta 'hoje' e 'ontem'
    comparison = ((today_kwh - yesterday_kwh) / yesterday_kwh * 100) if yesterday_kwh else 0

    # ultimos 7 dias
    start_7 = today - timedelta(days=6)
    last_7 = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date >= start_7
    ).order_by(ConsumptionDaily.date).all()

    daily_series = [{"date": str(r.date), "energy_kwh": r.energy_kwh} for r in last_7]

    # predicao mais recente
    pred = db.query(Prediction).filter_by(user_id=user_id).order_by(Prediction.generated_at.desc()).first()

    return {
        "summary_today": {
            "date": str(today),
            "energy_kwh": today_kwh,
            "cost_brl": round(today_kwh * price, 2),
            "comparison_vs_yesterday_pct": round(comparison, 1)
        },
        "daily_view_last_7_days": {
            "series": daily_series
        },
        "next_month_prediction": {
            "target_month": pred.target_month if pred else None,
            "energy_kwh_pred": pred.energy_kwh_pred if pred else None,
            "cost_brl_pred": pred.cost_pred if pred else None
        }
    }
