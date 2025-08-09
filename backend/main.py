"""
FastAPI backend for Vehicle Registration Dashboard
Fetches data from Vahan Dashboard and provides API endpoints for the React frontend
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import pandas as pd
from datetime import datetime, timedelta
import uvicorn
import logging

from data_collector import VahanDataCollector
from database import DatabaseManager
from analytics import VehicleAnalytics
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Vehicle Registration Dashboard API",
    description="API for fetching and analyzing vehicle registration data from Vahan Dashboard",
    version="1.0.0"
)

# Add CORS middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_collector = VahanDataCollector()
db_manager = DatabaseManager()
analytics = VehicleAnalytics(db_manager)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize database and fetch initial data"""
    await db_manager.initialize()
    # Try to fetch real data from Vahan Dashboard
    try:
        logger.info("Attempting to fetch real data from Vahan Dashboard...")
        await data_collector.fetch_and_store_data()
        logger.info("Real data fetched successfully from Vahan Dashboard")
    except Exception as e:
        logger.warning(f"Could not fetch real data from Vahan Dashboard: {str(e)}")
        logger.info("Using sample data instead")

@app.get("/")
async def root():
    """Health check and API information"""
    try:
        # Get data counts
        vehicle_count = await db_manager.get_vehicle_data_count()
        manufacturer_count = await db_manager.get_manufacturer_data_count()
        latest_date = await db_manager.get_latest_data_date()
        
        return {
            "status": "healthy",
            "service": "Vehicle Registration Dashboard API",
            "version": "1.0.0",
            "data_source": "Vahan Dashboard (https://vahan.parivahan.gov.in)",
            "data_status": {
                "vehicle_registrations": vehicle_count,
                "manufacturer_registrations": manufacturer_count,
                "latest_data_date": latest_date,
                "data_freshness": "Real-time from Vahan Dashboard" if vehicle_count > 0 else "Sample data"
            },
            "endpoints": {
                "registrations": "/api/registrations",
                "insights": "/api/insights", 
                "manufacturers": "/api/manufacturers",
                "refresh": "/api/refresh-data",
                "docs": "/docs"
            }
        }
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return {
            "status": "degraded",
            "error": str(e),
            "service": "Vehicle Registration Dashboard API"
        }

@app.get("/api/registrations")
async def get_registrations(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    category: Optional[str] = Query(None, description="Vehicle category (2W, 3W, 4W)"),
    manufacturers: Optional[str] = Query(None, description="Comma-separated list of manufacturers")
):
    """
    Get vehicle registration data with optional filters
    Returns both raw counts and YoY/QoQ percentage changes
    """
    try:
        # Parse manufacturers
        manufacturer_list = None
        if manufacturers:
            manufacturer_list = [m.strip() for m in manufacturers.split(",")]
        
        # Get data from analytics
        data = await analytics.get_filtered_data(
            start_date=start_date,
            end_date=end_date,
            category=category,
            manufacturers=manufacturer_list
        )
        
        return {
            "status": "success",
            "data": data,
            "filters": {
                "start_date": start_date,
                "end_date": end_date,
                "category": category,
                "manufacturers": manufacturer_list
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights")
async def get_insights():
    """Get key insights and trends"""
    try:
        insights = await analytics.get_insights()
        return {
            "status": "success",
            "data": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/manufacturers")
async def get_manufacturers():
    """Get list of available manufacturers"""
    try:
        manufacturers = await analytics.get_manufacturers()
        return {
            "status": "success",
            "manufacturers": manufacturers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh-data")
async def refresh_data():
    """Manually trigger data refresh from Vahan Dashboard"""
    try:
        logger.info("Manual data refresh requested")
        
        # Try to fetch real data from Vahan Dashboard
        await data_collector.fetch_and_store_data()
        
        # Get updated data count
        vehicle_count = await db_manager.get_vehicle_data_count()
        manufacturer_count = await db_manager.get_manufacturer_data_count()
        
        return {
            "status": "success", 
            "message": "Data refreshed successfully",
            "data_source": "Vahan Dashboard",
            "records_updated": {
                "vehicle_registrations": vehicle_count,
                "manufacturer_registrations": manufacturer_count
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error refreshing data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh data: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
