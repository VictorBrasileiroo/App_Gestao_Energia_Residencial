from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..auth.routes import get_current_user
from .service import process_and_save_consumption
from .analytics import get_hourly_pattern, get_daily_distribution

router = APIRouter(prefix="/consumption", tags=["Consumption"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
def upload_consumption(file: UploadFile = File(...), current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    result = process_and_save_consumption(db, current_user.id, file)
    return {"status": "success", "records_created": result}

@router.get("/hourly-pattern")
def get_hourly_pattern_route(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Retorna o padrão de consumo por hora do dia"""
    pattern = get_hourly_pattern(db, current_user.id)
    distribution = get_daily_distribution(db, current_user.id)
    return {
        "hourly_pattern": pattern,
        "daily_distribution": distribution
    }
