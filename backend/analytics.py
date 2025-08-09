"""
Analytics module for calculating YoY, QoQ metrics and generating insights
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import logging

from database import DatabaseManager

logger = logging.getLogger(__name__)

class VehicleAnalytics:
    """
    Provides analytics capabilities for vehicle registration data
    """
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    async def get_filtered_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        manufacturers: Optional[List[str]] = None
    ) -> Dict:
        """
        Get filtered data with YoY and QoQ calculations
        """
        try:
            # Get vehicle category data
            vehicle_data = await self.db.get_vehicle_data(start_date, end_date, category)
            
            # Get manufacturer data
            manufacturer_data = await self.db.get_manufacturer_data(
                start_date, end_date, manufacturers, category
            )
            
            # Calculate metrics
            vehicle_metrics = self._calculate_yoy_qoq_metrics(vehicle_data, 'category')
            manufacturer_metrics = self._calculate_yoy_qoq_metrics(manufacturer_data, 'manufacturer')
            
            # Prepare chart data
            chart_data = self._prepare_chart_data(vehicle_data, manufacturer_data, category, manufacturers)
            
            return {
                "chart_data": chart_data,
                "vehicle_metrics": vehicle_metrics,
                "manufacturer_metrics": manufacturer_metrics,
                "summary": self._calculate_summary_stats(vehicle_data, manufacturer_data)
            }
            
        except Exception as e:
            logger.error(f"Error in get_filtered_data: {str(e)}")
            raise
    
    def _calculate_yoy_qoq_metrics(self, df: pd.DataFrame, group_by: str) -> List[Dict]:
        """
        Calculate Year-over-Year and Quarter-over-Quarter metrics
        """
        if df.empty:
            return []
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        metrics = []
        
        for group_value in df[group_by].unique():
            group_data = df[df[group_by] == group_value].copy()
            group_data = group_data.sort_values('date')
            
            # Calculate YoY metrics
            yearly_data = group_data.groupby(['year'])['registrations'].sum().reset_index()
            yearly_data['yoy_change'] = yearly_data['registrations'].pct_change() * 100
            
            # Calculate QoQ metrics
            quarterly_data = group_data.groupby(['year', 'quarter'])['registrations'].sum().reset_index()
            quarterly_data['qoq_change'] = quarterly_data['registrations'].pct_change() * 100
            
            # Get latest metrics
            latest_year = yearly_data['year'].max()
            latest_quarter = quarterly_data['quarter'].max()
            
            latest_yoy = yearly_data[yearly_data['year'] == latest_year]['yoy_change'].iloc[0] if len(yearly_data) > 1 else 0
            latest_qoq = quarterly_data[quarterly_data['quarter'] == latest_quarter]['qoq_change'].iloc[-1] if len(quarterly_data) > 1 else 0
            
            latest_registrations = group_data['registrations'].sum()
            
            metrics.append({
                group_by: group_value,
                "total_registrations": int(latest_registrations),
                "yoy_change": round(float(latest_yoy), 2) if not np.isnan(latest_yoy) else 0,
                "qoq_change": round(float(latest_qoq), 2) if not np.isnan(latest_qoq) else 0,
                "trend": "up" if latest_yoy > 0 else "down" if latest_yoy < 0 else "stable"
            })
        
        return sorted(metrics, key=lambda x: x["total_registrations"], reverse=True)
    
    def _prepare_chart_data(self, vehicle_data: pd.DataFrame, manufacturer_data: pd.DataFrame, 
                           category: Optional[str] = None, manufacturers: Optional[List[str]] = None) -> List[Dict]:
        """
        Prepare data for charts in the format expected by the frontend
        Handles both vehicle category and manufacturer filtering
        """
        if vehicle_data.empty and manufacturer_data.empty:
            return []
        
        result = []
        
        # If manufacturers are selected, show manufacturer-specific data
        if manufacturers and len(manufacturers) > 0:
            if not manufacturer_data.empty:
                # Convert dates and sort
                manufacturer_data['date'] = pd.to_datetime(manufacturer_data['date'])
                manufacturer_data = manufacturer_data.sort_values('date')
                
                # Filter by selected manufacturers
                filtered_data = manufacturer_data[manufacturer_data['manufacturer'].isin(manufacturers)]
                
                if not filtered_data.empty:
                    # Group by month and manufacturer
                    monthly_data = filtered_data.groupby([
                        filtered_data['date'].dt.to_period('M'), 'manufacturer'
                    ])['registrations'].sum().reset_index()
                    
                    # Convert period back to string for JSON serialization
                    monthly_data['month'] = monthly_data['date'].astype(str)
                    
                    # Pivot to get manufacturers as columns
                    chart_data = monthly_data.pivot(index='month', columns='manufacturer', values='registrations').fillna(0)
                    
                    # Convert to list of dictionaries for the frontend
                    for month in chart_data.index:
                        row = {"month": month}
                        total = 0
                        for manufacturer in chart_data.columns:
                            value = int(chart_data.loc[month, manufacturer])
                            row[manufacturer] = value
                            total += value
                        
                        row["total"] = total
                        result.append(row)
        
        # If no manufacturers selected or manufacturer data is empty, show vehicle category data
        if not result and not vehicle_data.empty:
            # Convert dates and sort
            vehicle_data['date'] = pd.to_datetime(vehicle_data['date'])
            vehicle_data = vehicle_data.sort_values('date')
            
            # Filter by category if specified
            if category:
                vehicle_data = vehicle_data[vehicle_data['category'] == category]
            
            if not vehicle_data.empty:
                # Group by month for better visualization
                monthly_data = vehicle_data.groupby([
                    vehicle_data['date'].dt.to_period('M'), 'category'
                ])['registrations'].sum().reset_index()
                
                # Convert period back to string for JSON serialization
                monthly_data['month'] = monthly_data['date'].astype(str)
                
                # Pivot to get categories as columns
                chart_data = monthly_data.pivot(index='month', columns='category', values='registrations').fillna(0)
                
                # Convert to list of dictionaries for the frontend
                for month in chart_data.index:
                    row = {"month": month}
                    total = 0
                    for cat in chart_data.columns:
                        value = int(chart_data.loc[month, cat])
                        # Normalize category names to lowercase for frontend
                        if cat == '2W':
                            row['2w'] = value
                        elif cat == '3W':
                            row['3w'] = value
                        elif cat == '4W':
                            row['4w'] = value
                        total += value
                    
                    row["total"] = total
                    result.append(row)
        
        return result[-12:] if result else []  # Return last 12 months
    
    def _calculate_summary_stats(self, vehicle_data: pd.DataFrame, manufacturer_data: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics
        """
        if vehicle_data.empty:
            return {}
        
        total_registrations = vehicle_data['registrations'].sum()
        
        # Category breakdown
        category_breakdown = vehicle_data.groupby('category')['registrations'].sum().to_dict()
        
        # Top manufacturers
        top_manufacturers = []
        if not manufacturer_data.empty:
            top_manufacturers = (manufacturer_data.groupby('manufacturer')['registrations']
                               .sum()
                               .sort_values(ascending=False)
                               .head(5)
                               .to_dict())
        
        return {
            "total_registrations": int(total_registrations),
            "category_breakdown": {k: int(v) for k, v in category_breakdown.items()},
            "top_manufacturers": {k: int(v) for k, v in top_manufacturers.items()},
            "data_period": {
                "start": vehicle_data['date'].min() if not vehicle_data.empty else None,
                "end": vehicle_data['date'].max() if not vehicle_data.empty else None
            }
        }
    
    async def get_insights(self) -> List[Dict]:
        """
        Generate key insights and trends
        """
        try:
            # Get recent data (last 12 months)
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
            vehicle_data = await self.db.get_vehicle_data(start_date, end_date)
            manufacturer_data = await self.db.get_manufacturer_data(start_date, end_date)
            
            insights = []
            
            if not vehicle_data.empty:
                # Calculate YoY growth for insights
                vehicle_metrics = self._calculate_yoy_qoq_metrics(vehicle_data, 'category')
                manufacturer_metrics = self._calculate_yoy_qoq_metrics(manufacturer_data, 'manufacturer')
                
                # Find top growth categories
                for metric in vehicle_metrics:
                    if metric['yoy_change'] > 10:
                        insights.append({
                            "type": "growth",
                            "title": f"{metric['category']} vehicles up {metric['yoy_change']:.1f}% YoY",
                            "description": f"Strong growth in {metric['category']} category with {metric['total_registrations']:,} total registrations",
                            "value": metric['yoy_change'],
                            "trend": "positive"
                        })
                
                # Find top manufacturers
                top_manufacturers = sorted(manufacturer_metrics, key=lambda x: x['yoy_change'], reverse=True)[:3]
                for i, manufacturer in enumerate(top_manufacturers):
                    if manufacturer['yoy_change'] > 5:
                        insights.append({
                            "type": "manufacturer",
                            "title": f"{manufacturer['manufacturer']} leading growth",
                            "description": f"YoY growth of {manufacturer['yoy_change']:.1f}% with {manufacturer['total_registrations']:,} registrations",
                            "value": manufacturer['yoy_change'],
                            "trend": "positive"
                        })
                
                # Market share insights
                total_registrations = sum([m['total_registrations'] for m in vehicle_metrics])
                for metric in vehicle_metrics:
                    market_share = (metric['total_registrations'] / total_registrations) * 100
                    insights.append({
                        "type": "market_share",
                        "title": f"{metric['category']} holds {market_share:.1f}% market share",
                        "description": f"Total registrations: {metric['total_registrations']:,}",
                        "value": market_share,
                        "trend": "neutral"
                    })
            
            return insights[:6]  # Return top 6 insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return []
    
    async def get_manufacturers(self) -> List[str]:
        """Get list of all manufacturers"""
        return await self.db.get_manufacturers()
