from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import structlog

from app.core.database import get_db, User
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint"""
    try:
        # Find user by email (username field in form contains email)
        user = db.query(User).filter(User.email == form_data.username).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o password non corretti",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account disabilitato"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.role.value if hasattr(user.role, 'value') else str(user.role)},
            expires_delta=access_token_expires
        )
        
        logger.info("User logged in successfully", email=user.email)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value if hasattr(user.role, 'value') else str(user.role)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(status_code=500, detail="Errore interno del server")

@router.post("/register")
async def register(
    email: str,
    full_name: str,
    password: str,
    role: str = "receptionist",
    db: Session = Depends(get_db)
):
    """Register new user (admin only)"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email già esistente"
            )
        
        # Create new user
        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role=role
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info("New user registered", email=email, full_name=full_name)
        
        return {
            "message": "Utente registrato con successo",
            "user_id": new_user.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("Registration failed", error=str(e))
        raise HTTPException(status_code=500, detail="Errore interno del server")
