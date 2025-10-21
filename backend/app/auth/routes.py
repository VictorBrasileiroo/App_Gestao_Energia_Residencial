from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import models
from ..database import SessionLocal
from ..utils.security import hash_password, verify_password, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# sessao do db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sem 'sub'")
    user = db.query(models.User).filter(models.User.id == int(sub)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@router.post("/register")
def register_user(name: str | None = None, email: str = None, password: str = None, db: Session = Depends(get_db)):
    if not email or not password:
        raise HTTPException(status_code=400, detail="email e password são obrigatórios")
    exists = db.query(models.User).filter(models.User.email == email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = models.User(name=name or "", email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Usuário criado com sucesso", "user_id": user.id}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm entrega username e password
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# teste
@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name}
