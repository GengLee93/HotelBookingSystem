import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-hard-to-guess-string'
    
    # Get the database URL from environment variable
    database_url = os.environ.get('DATABASE_URL')
    
    # Fix for Heroku/Render: SQLAlchemy requires 'postgresql://', but some hosts use 'postgres://'
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'postgresql://postgres:123@localhost:5432/hotel_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
