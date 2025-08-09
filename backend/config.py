"""
Configuration settings for the Vehicle Registration Dashboard
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///vehicle_data.db")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Vahan Dashboard Configuration
    VAHAN_BASE_URL = os.getenv("VAHAN_BASE_URL", "https://vahan.parivahan.gov.in/vahan4dashboard/")
    VAHAN_API_KEY = os.getenv("VAHAN_API_KEY", "")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Development
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS origins for development
    CORS_ORIGINS = [
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Create React App default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

settings = Settings()
