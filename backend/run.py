"""
Startup script for the Vehicle Registration Dashboard backend
"""

import asyncio
import uvicorn
from main import app
from data_collector import VahanDataCollector
from database import DatabaseManager

async def initialize_data():
    """Initialize database and populate with sample data"""
    print("Initializing database...")
    
    db_manager = DatabaseManager()
    await db_manager.initialize()
    
    print("Fetching initial data...")
    data_collector = VahanDataCollector()
    await data_collector.fetch_and_store_data()
    
    print("Data initialization completed!")

if __name__ == "__main__":
    # Initialize data first
    asyncio.run(initialize_data())
    
    # Start the server with import string to ensure stability with reload
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
