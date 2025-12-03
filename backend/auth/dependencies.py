from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.database_models import User
from auth.jwt_handler import verify_token

# OAuth2 scheme - tells FastAPI where to look for the token
# tokenUrl is the endpoint where users can get tokens (login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts and validates the JWT token.
    
    This is used to protect routes that require authentication.
    It automatically:
    1. Extracts token from Authorization header
    2. Verifies token signature and expiration
    3. Fetches user from database
    4. Returns user object
    
    Usage in routes:
        @router.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.username}
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User object if authentication successful
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token and extract username
    username = verify_token(token)
    
    if username is None:
        raise credentials_exception
    
    # Fetch user from database
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency that ensures the user is active (not disabled).
    
    Use this instead of get_current_user when you want to ensure
    the user account is active.
    
    Usage:
        @router.get("/active-only")
        async def active_route(user: User = Depends(get_current_active_user)):
            return {"user": user.username}
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User object if active
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency that ensures the user is an admin.
    
    Use this for admin-only routes.
    
    Usage:
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            admin: User = Depends(get_current_admin_user)
        ):
            # Only admins can access this
            pass
    
    Args:
        current_user: User from get_current_active_user dependency
        
    Returns:
        User object if admin
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return current_user
