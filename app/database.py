from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.utils.config import get_settings

settings = get_settings()

# Create SQLAlchemy engine
engine = create_engine(settings.database_url)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    public_repos = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    github_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationship with repositories (to be implemented later)
    # repositories = relationship("Repository", back_populates="user")


# Create all tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)


# Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
