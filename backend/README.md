# Vehicle Registration Dashboard - Backend

This is the Python backend for the Vehicle Registration Dashboard. It provides RESTful APIs for fetching, processing, and analyzing vehicle registration data from the Vahan Dashboard.

## Features

- 🚗 **Data Collection**: Fetches vehicle registration data from Vahan Dashboard
- 📊 **Analytics**: Calculates YoY (Year-over-Year) and QoQ (Quarter-over-Quarter) metrics
- 🗄️ **Database**: SQLite database for efficient data storage and retrieval
- 🔄 **Real-time APIs**: RESTful endpoints for the React frontend
- 📈 **Insights**: Generates key market insights and trends

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLite**: Lightweight database for data storage
- **Pandas**: Data analysis and manipulation
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── data_collector.py    # Vahan Dashboard data collection
├── database.py          # Database operations and management
├── analytics.py         # YoY/QoQ calculations and insights
├── config.py           # Configuration settings
├── run.py              # Startup script with data initialization
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database and start server**:
   ```bash
   python run.py
   ```

The server will start on `http://localhost:8000` with automatic database initialization and sample data.

## API Endpoints

### Core Endpoints

- **GET `/`** - Health check
- **GET `/api/registrations`** - Get vehicle registration data with filters
- **GET `/api/insights`** - Get key market insights and trends
- **GET `/api/manufacturers`** - Get list of available manufacturers
- **POST `/api/refresh-data`** - Manually refresh data from Vahan Dashboard

### Query Parameters for `/api/registrations`

- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `category` (optional): Vehicle category (2W, 3W, 4W)
- `manufacturers` (optional): Comma-separated list of manufacturers

### Example API Calls

```bash
# Get all registration data
curl "http://localhost:8000/api/registrations"

# Get 2W data for specific date range
curl "http://localhost:8000/api/registrations?start_date=2023-01-01&end_date=2023-12-31&category=2W"

# Get data for specific manufacturers
curl "http://localhost:8000/api/registrations?manufacturers=Hero%20MotoCorp,TVS"

# Get market insights
curl "http://localhost:8000/api/insights"
```

## Data Model

### Vehicle Registrations
- Date, Year, Month, Quarter
- Vehicle Category (2W, 3W, 4W)
- Registration Count
- Geographic State

### Manufacturer Registrations
- Date, Year, Month, Quarter
- Manufacturer Name
- Vehicle Category
- Registration Count
- Geographic State

## Analytics Features

### YoY (Year-over-Year) Analysis
- Compares current year data with previous year
- Calculates percentage growth/decline
- Identifies trends across vehicle categories and manufacturers

### QoQ (Quarter-over-Quarter) Analysis
- Compares current quarter with previous quarter
- Tracks seasonal patterns and short-term trends
- Provides granular performance insights

### Market Insights
- Automatic identification of top growth categories
- Leading manufacturer performance analysis
- Market share calculations
- Trend detection and alerting

## Development

### Running in Development Mode

```bash
# Start with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations

The SQLite database is automatically created and initialized. Data files:
- `vehicle_data.db` - Main database file

### Adding New Data Sources

To add new data sources, modify `data_collector.py`:

1. Add new fetch methods
2. Update data storage methods in `database.py`
3. Extend analytics calculations in `analytics.py`

## Production Deployment

### Environment Variables

Create a `.env` file with:

```env
DATABASE_URL=sqlite:///vehicle_data.db
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
DEBUG=False
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

### Production Considerations

- Use PostgreSQL for production database
- Implement proper error handling and logging
- Add authentication and rate limiting
- Set up monitoring and health checks
- Configure HTTPS/SSL certificates

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill existing process
   lsof -ti:8000 | xargs kill -9
   ```

2. **Database connection errors**:
   - Check if SQLite database file is accessible
   - Verify permissions on the data directory

3. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

### Logs

Check application logs for debugging:
```bash
python run.py 2>&1 | tee app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
