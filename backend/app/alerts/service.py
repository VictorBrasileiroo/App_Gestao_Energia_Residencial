from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..models import AlertRule, Alert, ConsumptionDaily

def evaluate_alerts(db: Session, user_id: int):
    rules = db.query(AlertRule).filter_by(user_id=user_id, enabled=True).all()
    today = date.today()
    for rule in rules:
        cfg = rule.config
        if rule.rule_type == "FIXED_THRESHOLD":
            threshold = cfg.get("threshold_kwh", 999999)
            rec = db.query(ConsumptionDaily).filter_by(user_id=user_id, date=today - timedelta(days=1)).first()
            if rec and rec.energy_kwh > threshold:
                alert = Alert(
                    user_id=user_id,
                    alert_rule_id=rule.id,
                    trigger_date=rec.date,
                    value_kwh=rec.energy_kwh,
                    status="OPEN"
                )
                db.add(alert)
    db.commit()
