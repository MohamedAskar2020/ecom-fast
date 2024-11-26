import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    DATABASE_NAME: str
    HOST: str = "0.0.0.0"  # Default value
    PORT: int = 8000        # Default value
    DEBUG: bool = False     # Default value
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    FROM_EMAIL: str
    FROM_NAME: str

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Directory to save uploaded images
UPLOAD_DIRECTORY = "uploads/products"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
