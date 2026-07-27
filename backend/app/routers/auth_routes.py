from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/api/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return schemas.TokenResponse(access_token=token, role=user.role, full_name=user.full_name)


@router.post("/api/logout")
def logout():
    # Stateless JWT: logout is handled client-side by discarding the token.
    return {"message": "Logged out"}


@router.get("/api/profile", response_model=schemas.UserProfile)
def get_profile(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
