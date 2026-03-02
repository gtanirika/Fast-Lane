"""
Fast Lane - Authentication & Security
JWT token handling, password hashing, and auth dependencies
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import os
import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from backend.schemas import TokenData, UserResponse
from backend.models import User
from sqlalchemy.orm import Session

# ============== PASSWORD HASHING ==============

# Configure bcrypt context for password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    
    Args:
        password: Plain-text password
    
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hash.
    
    Args:
        plain_password: Plain-text password
        hashed_password: Hashed password from database
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============== JWT TOKEN HANDLING ==============

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-env")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Security scheme for OpenAPI documentation
security = HTTPBearer()


class TokenManager:
    """Manages JWT token creation and validation."""
    
    @staticmethod
    def create_access_token(
        data: Dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Payload data to encode
            expires_delta: Token expiration time delta
        
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        # Set expiration
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        
        to_encode.update({"exp": expire})
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def create_token_pair(user_id: int, username: str) -> Dict[str, str]:
        """
        Create both access and refresh tokens for a user.
        
        Args:
            user_id: User ID
            username: Username
        
        Returns:
            Dictionary with 'access_token', 'token_type', and 'expires_in'
        """
        # Create access token
        token_data = {
            "sub": str(user_id),
            "username": username,
        }
        
        access_token = TokenManager.create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded token data
        
        Raises:
            HTTPException: If token is invalid or expired
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            user_id: str = payload.get("sub")
            username: str = payload.get("username")
            
            if user_id is None or username is None:
                raise credentials_exception
            
            return TokenData(user_id=int(user_id), username=username)
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise credentials_exception
        except ValidationError:
            raise credentials_exception


# ============== FASTAPI DEPENDENCIES ==============

def get_current_user(
    token: HTTPBearer = Depends(HTTPBearer()),
) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    
    Usage in route:
        @app.get("/user/me")
        def get_me(current_user: User = Depends(get_current_user)):
            return current_user
    
    Args:
        token: HTTP Bearer token from header
        db: Database session
    
    Returns:
        Current user object
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        token_str = token.credentials if hasattr(token, 'credentials') else str(token)
        token_data = TokenManager.verify_token(token_str)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # create a new db session every call
    from backend.database import SessionLocal
    db = SessionLocal()
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    return user


async def get_optional_user(
    token: Optional[str] = None,
) -> Optional[TokenData]:
    """
    Dependency to get optional authenticated user (doesn't require auth).
    
    Returns:
        Token data if authenticated, None otherwise
    """
    if token is None:
        return None
    
    try:
        token_data = TokenManager.verify_token(token)
        return token_data
    except HTTPException:
        return None


# ============== HELPER FUNCTIONS ==============

def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> Optional[User]:
    """
    Authenticate user with email and password.
    
    Args:
        db: Database session
        email: User email
        password: Plain-text password
    
    Returns:
        User object if authentication succeeds, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
) -> User:
    """
    Create a new user with hashed password.
    
    Args:
        db: Database session
        username: User username
        email: User email
        password: Plain-text password
    
    Returns:
        Created user object
    
    Raises:
        HTTPException: If user already exists
    """
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        if existing_user.username == username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    
    # Create user
    hashed_password = hash_password(password)
    db_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        coins=0,
        gems=0,
        current_level=1,
        level_unlocked=1,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


# ============== ROLE-BASED ACCESS CONTROL (Future) ==============

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to enforce admin role.
    
    Usage:
        @app.delete("/admin/users/{user_id}")
        def delete_user(user_id: int, admin: User = Depends(require_admin)):
            ...
    """
    # TODO: Add role field to User model
    # if current_user.role != "admin":
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Admin access required"
    #     )
    return current_user
