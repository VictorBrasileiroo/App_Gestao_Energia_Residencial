from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..auth.routes import get_current_user
from .service import evaluate_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_alerts(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    from ..models import Alert
    rows = db.query(Alert).filter_by(user_id=current_user.id).all()
    alerts_list = [
        {
            "id": a.id,
            "trigger_date": str(a.trigger_date),
            "value_kwh": a.value_kwh,
            "status": a.status,
            "alert_rule_id": a.alert_rule_id
        }
        for a in rows
    ]
    return {"alerts": alerts_list}

@router.post("/evaluate")
def evaluate_now(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    created = evaluate_alerts(db, current_user.id)
    return {"created_alerts": created}
