from passlib.context import CryptContext

# Create password context for hashing
# bcrypt is a secure one-way hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    This is a one-way hash - you cannot reverse it to get the original password.
    Each time you hash the same password, you get a different hash (due to salt).
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> print(hashed)
        $2b$12$KIXxBz9...
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password from database
        
    Returns:
        True if passwords match, False otherwise
        
    Example:
        >>> hashed = hash_password("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)
