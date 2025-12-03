from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from config import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    How JWT works:
    1. Takes user data (payload)
    2. Adds expiration time
    3. Encodes with SECRET_KEY using HS256 algorithm
    4. Returns signed token string
    
    The token has 3 parts separated by dots:
    - Header (algorithm info)
    - Payload (user data)
    - Signature (verification)
    
    Args:
        data: Dictionary containing user information (usually {"sub": username})
        expires_delta: Optional custom expiration time
        
    Returns:
        JWT token string
        
    Example:
        >>> token = create_access_token({"sub": "john_doe"})
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration to payload
    to_encode.update({"exp": expire})
    
    # Create and return JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Verify and decode a JWT token.
    
    This function:
    1. Decodes the token using SECRET_KEY
    2. Verifies the signature
    3. Checks expiration time
    4. Returns username if valid
    
    Args:
        token: JWT token string
        
    Returns:
        Username if token is valid, None if invalid or expired
        
    Example:
        >>> token = create_access_token({"sub": "john_doe"})
        >>> username = verify_token(token)
        >>> print(username)
        john_doe
    """
    try:
        # Decode token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Extract username from "sub" (subject) claim
        username: str = payload.get("sub")
        
        if username is None:
            return None
        
        return username
    
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None
