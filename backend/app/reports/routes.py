from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from ..database import SessionLocal
from ..models import ConsumptionDaily, TariffPlan
from ..auth.routes import get_current_user
from .service import get_report_summary

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/monthly")
def report_monthly(year: int, month: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    from calendar import monthrange
    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])
    user_id = current_user.id

    data = db.query(ConsumptionDaily).filter(
        ConsumptionDaily.user_id == user_id,
        ConsumptionDaily.date.between(start_date, end_date)
    ).all()

    if not data:
        raise HTTPException(status_code=404, detail="Sem dados para o período.")
    
    tariff = db.query(TariffPlan).filter_by(user_id=user_id).first()
    price = tariff.price_per_kwh if tariff else 1.0

    total_kwh = sum(r.energy_kwh for r in data)
    avg_daily = total_kwh / len(data)
    peak = max(data, key=lambda x: x.energy_kwh)

    return {
        "period": {"year": year, "month": month},
        "summary": {
            "total_energy_kwh": total_kwh,
            "total_cost_brl": round(total_kwh * price, 0),
            "avg_daily_kwh": avg_daily,
            "peak_day": [{"date": str(r.date), "energy_kwh": r.energy_kwh} for r in data]
        },
        "daily_series": [{"date": str(r.date), "energy_kwh": r.energy_kwh} for r in data]
    }

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    report = get_report_summary(db, user.id)
    return report