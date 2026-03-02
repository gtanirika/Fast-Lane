"""
Fast Lane - Main FastAPI Application
Entry point for the backend API server
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict

from config.settings import settings, validate_settings, get_cors_config
from backend.database import init_db, get_db, seed_db
from backend.models import Base, User
from backend.auth import TokenManager, authenticate_user, create_user, get_current_user
from backend.schemas import (
    SignUpRequest, LoginRequest, Token, UserResponse
)

# ============== LOGGING CONFIGURATION ==============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler(settings.log_file),
    ]
)
logger = logging.getLogger(__name__)


# ============== STARTUP & SHUTDOWN EVENTS ==============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle (startup/shutdown).
    """
    # Startup
    logger.info("🚀 Starting Fast Lane API Server...")
    logger.info(f"📊 Database: {settings.database_url}")
    logger.info(f"🔐 Environment: {settings.debug and 'Development' or 'Production'}")
    
    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Seed database with initial data
    try:
        seed_db()
        logger.info("✅ Database seeded with initial data")
    except Exception as e:
        logger.warning(f"⚠️  Database seeding: {e}")
    
    validate_settings()
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Fast Lane API Server...")


# ============== FASTAPI APPLICATION ==============

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# ============== MIDDLEWARE ==============

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    **get_cors_config()
)

logger.info("✅ CORS middleware configured")


# ============== ROOT ENDPOINT ==============

@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint - API health check."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "message": "Welcome to Fast Lane API! 🏎️",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


# ============== AUTHENTICATION ROUTES ==============

@app.post(
    "/api/auth/signup",
    response_model=Dict,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
    summary="Register a new user",
)
def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        # Check if user exists
        existing = db.query(User).filter(
            (User.email == request.email) | (User.username == request.username)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        # Create user
        user = create_user(
            db=db,
            username=request.username,
            email=request.email,
            password=request.password,
        )
        
        logger.info(f"✅ New user registered: {user.username}")
        
        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@app.post(
    "/api/auth/login",
    response_model=Dict,
    tags=["Auth"],
    summary="Login user",
)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    try:
        # Find user and verify password
        user = authenticate_user(db, request.email, request.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create token
        token_data = TokenManager.create_token_pair(user.id, user.username)
        
        logger.info(f"✅ User logged in: {user.username}")
        
        return {
            **token_data,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "coins": user.coins,
                "gems": user.gems,
                "level_unlocked": user.level_unlocked,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@app.post(
    "/api/auth/refresh",
    response_model=Dict,
    tags=["Auth"],
    summary="Refresh token",
)
def refresh_token(current_user: User = Depends(get_current_user)) -> Dict:
    """Refresh JWT token."""
    try:
        # Create new token
        token_data = TokenManager.create_token_pair(
            current_user.id,
            current_user.username
        )
        
        logger.info(f"✅ Token refreshed for: {current_user.username}")
        
        return token_data
    
    except Exception as e:
        logger.error(f"❌ Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


# ============== USER ROUTES ==============

@app.get(
    "/api/users/me",
    response_model=Dict,
    tags=["Users"],
    summary="Get current user profile",
)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get the authenticated user's profile."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "coins": current_user.coins,
        "gems": current_user.gems,
        "current_level": current_user.current_level,
        "level_unlocked": current_user.level_unlocked,
        "best_distance": current_user.best_distance,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat(),
    }


@app.get(
    "/api/users/{user_id}",
    response_model=Dict,
    tags=["Users"],
    summary="Get user by ID",
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get public user profile by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "username": user.username,
        "level_unlocked": user.level_unlocked,
        "best_distance": user.best_distance,
    }


# ============== ERROR HANDLERS ==============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code,
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Generic exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "success": False,
        "error": "Internal server error",
        "status_code": 500,
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🏎️  FAST LANE - HILL CLIMB RACING CLONE")
    print("="*60)
    print(f"📱 App: {settings.app_name}")
    print(f"🔌 Server: http://{settings.host}:{settings.port}")
    print(f"📚 Docs: http://{settings.host}:{settings.port}/docs")
    print(f"💾 Database: {settings.database_url}")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
