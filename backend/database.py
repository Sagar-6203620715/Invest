"""
Database management module for storing and retrieving vehicle registration data
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import asyncio
import aiosqlite
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manages SQLite database operations for vehicle registration data
    """
    
    def __init__(self, db_path: str = "vehicle_data.db"):
        self.db_path = db_path
    
    async def initialize(self):
        """Initialize database and create tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Create vehicle registrations table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS vehicle_registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    quarter INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    registrations INTEGER NOT NULL,
                    state TEXT DEFAULT 'All India',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, category, state)
                )
            """)
            
            # Create manufacturer registrations table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS manufacturer_registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    quarter INTEGER NOT NULL,
                    manufacturer TEXT NOT NULL,
                    category TEXT NOT NULL,
                    registrations INTEGER NOT NULL,
                    state TEXT DEFAULT 'All India',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, manufacturer, category, state)
                )
            """)
            
            # Create indexes for better query performance
            await db.execute("CREATE INDEX IF NOT EXISTS idx_vehicle_date ON vehicle_registrations(date)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_vehicle_category ON vehicle_registrations(category)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_vehicle_year_quarter ON vehicle_registrations(year, quarter)")
            
            await db.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer_date ON manufacturer_registrations(date)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer_name ON manufacturer_registrations(manufacturer)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer_category ON manufacturer_registrations(category)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer_year_quarter ON manufacturer_registrations(year, quarter)")
            
            await db.commit()
            
        logger.info("Database initialized successfully")
    
    async def store_vehicle_data(self, data: List[Dict]):
        """Store vehicle category data"""
        async with aiosqlite.connect(self.db_path) as db:
            for record in data:
                await db.execute("""
                    INSERT OR REPLACE INTO vehicle_registrations 
                    (date, year, month, quarter, category, registrations, state)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    record['date'], record['year'], record['month'], 
                    record['quarter'], record['category'], record['registrations'],
                    record.get('state', 'All India')
                ))
            
            await db.commit()
            logger.info(f"Stored {len(data)} vehicle registration records")
    
    async def store_manufacturer_data(self, data: List[Dict]):
        """Store manufacturer data"""
        async with aiosqlite.connect(self.db_path) as db:
            for record in data:
                await db.execute("""
                    INSERT OR REPLACE INTO manufacturer_registrations 
                    (date, year, month, quarter, manufacturer, category, registrations, state)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    record['date'], record['year'], record['month'], 
                    record['quarter'], record['manufacturer'], record['category'], 
                    record['registrations'], record.get('state', 'All India')
                ))
            
            await db.commit()
            logger.info(f"Stored {len(data)} manufacturer registration records")
    
    async def get_vehicle_data(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> pd.DataFrame:
        """Get vehicle registration data with filters"""
        
        query = """
            SELECT date, year, month, quarter, category, registrations, state
            FROM vehicle_registrations
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY date DESC"
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
        
        return pd.DataFrame(rows, columns=columns)
    
    async def get_manufacturer_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        manufacturers: Optional[List[str]] = None,
        category: Optional[str] = None
    ) -> pd.DataFrame:
        """Get manufacturer registration data with filters"""
        
        query = """
            SELECT date, year, month, quarter, manufacturer, category, registrations, state
            FROM manufacturer_registrations
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if manufacturers:
            placeholders = ",".join(["?" for _ in manufacturers])
            query += f" AND manufacturer IN ({placeholders})"
            params.extend(manufacturers)
        
        query += " ORDER BY date DESC"
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
        
        return pd.DataFrame(rows, columns=columns)
    
    async def get_manufacturers(self) -> List[str]:
        """Get list of all distinct manufacturers"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT DISTINCT manufacturer FROM manufacturer_registrations ORDER BY manufacturer"
            ) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
    
    async def get_vehicle_data_count(self) -> int:
        """Get total count of vehicle registration records"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM vehicle_registrations") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_manufacturer_data_count(self) -> int:
        """Get total count of manufacturer registration records"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM manufacturer_registrations") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0
    
    async def get_latest_data_date(self) -> Optional[str]:
        """Get the most recent date in the database"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT MAX(date) FROM vehicle_registrations") as cursor:
                result = await cursor.fetchone()
        
        return result[0] if result and result[0] else None
