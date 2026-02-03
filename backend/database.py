"""
SQLAlchemy database setup for Railway PostgreSQL.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read DATABASE_URL from environment variable (Railway sets this automatically)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine only when DATABASE_URL is available
# Note: psycopg2-binary is used for synchronous connections
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Enable connection health checks
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False           # Set to True for SQL logging (dev only)
    )
    # Create SessionLocal class for database sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

# Create declarative base for models
Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session.
    Ensures session is closed after use.
    """
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database by creating all tables.
    Call this at startup using FastAPI startup event.
    """
    if engine is None:
        print("DATABASE_URL not set - skipping table creation")
        return
    # Import models to ensure they are registered with Base
    from models import Equipment
    
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
