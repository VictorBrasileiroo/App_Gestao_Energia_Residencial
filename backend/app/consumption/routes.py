from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..auth.routes import get_current_user
from .service import process_and_save_consumption

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
