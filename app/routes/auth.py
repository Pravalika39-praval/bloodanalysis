from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import text
from datetime import timedelta
import logging

from app.models.database_models import User, UserCreate, Token
from app.utils.auth import verify_password, get_password_hash, create_access_token, verify_token
from database import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username}
            )
            user_data = result.fetchone()
        
        if user_data is None:
            raise credentials_exception
        
        return User(
            user_id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            full_name=user_data[4],
            language_pref=user_data[5],
            created_at=user_data[6]
        )
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise credentials_exception

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/signup", response_model=User)
async def signup(user_data: UserCreate):
    """Register new user"""
    try:
        with db.get_connection() as conn:
            # Check if user already exists
            result = conn.execute(
                text("SELECT user_id FROM users WHERE username = :username OR email = :email"),
                {"username": user_data.username, "email": user_data.email}
            )
            existing_user = result.fetchone()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username or email already registered"
                )
            
            # Create new user
            hashed_password = get_password_hash(user_data.password)
            result = conn.execute(
                text("""
                    INSERT INTO users (username, email, password_hash, full_name, language_pref)
                    VALUES (:username, :email, :password_hash, :full_name, :language_pref)
                    RETURNING user_id, created_at
                """),
                {
                    "username": user_data.username,
                    "email": user_data.email,
                    "password_hash": hashed_password,
                    "full_name": user_data.full_name,
                    "language_pref": user_data.language_pref
                }
            )
            new_user = result.fetchone()
            user_id = new_user[0]
            created_at = new_user[1]
            conn.commit()
        
        logger.info(f"New user registered: {user_data.username}")
        return User(
            user_id=user_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            language_pref=user_data.language_pref,
            created_at=created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """User login"""
    try:
        with db.get_connection() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": form_data.username}
            )
            user_data = result.fetchone()
        
        if not user_data or not verify_password(form_data.password, user_data[3]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data[1]}, expires_delta=access_token_expires
        )
        
        logger.info(f"User logged in: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )