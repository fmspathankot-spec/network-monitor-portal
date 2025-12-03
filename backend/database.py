from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# Create SQLAlchemy engine
# This connects to PostgreSQL database
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging
)

# Create session factory
# Sessions are used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

def get_db():
    """
    Dependency function that provides database sessions.
    
    Usage in FastAPI routes:
    @router.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
    
    The session is automatically closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
