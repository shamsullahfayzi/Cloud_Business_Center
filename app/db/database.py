from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL configuration
DATABASE_URL = URL.create(
    drivername="mssql+pyodbc",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME"),
    query={"driver": "ODBC Driver 17 for SQL Server"},
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
    pool_size=5,  # Maximum number of connections to keep persistent
    max_overflow=10,  # Maximum number of connections to create when pool is full
)

# SessionLocal class for database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base class for declarative models
Base = declarative_base()
metadata = MetaData()

# Database dependency
def get_db() -> Generator:
    """
    Dependency function to get DB session.
    Used in FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database initialization function
def init_db() -> None:
    """
    Initialize database by creating all tables.
    Call this function when starting your application.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Optional: Database health check
async def check_database_connection() -> bool:
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
    finally:
        db.close()

# Optional: Database cleanup
def cleanup_database() -> None:
    """
    Cleanup database connections.
    Call this function when shutting down your application.
    """
    try:
        engine.dispose()
        print("Database connections closed successfully!")
    except Exception as e:
        print(f"Error closing database connections: {e}")