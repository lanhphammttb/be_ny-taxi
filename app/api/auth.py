from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token
from app.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.user_id), "role": db_user.role})
    return TokenResponse(access_token=access_token, token_type="bearer")
