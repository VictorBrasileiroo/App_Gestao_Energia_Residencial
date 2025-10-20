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
    rows = db.query("alerts").filter_by(user_id=current_user.id).all()
    return {"message": "Implemente listagem real", "user_id": current_user.id}

@router.post("/evaluate")
def evaluate_now(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    created = evaluate_alerts(db, current_user.id)
    return {"created_alerts": created}
