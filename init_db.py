from config.database import engine, Base
from models.user import User
# Import all other models here

def init_db():
    """Initialize database tables"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def reset_db():
    """Reset database tables"""
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables reset successfully!")

if __name__ == "__main__":
    init_db()