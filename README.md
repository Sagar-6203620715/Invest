# Investor Fleet Vision  Vehicle Registration Dashboard

A comprehensive, investor-friendly dashboard for analyzing vehicle registration data from the Vahan Dashboard. This project combines a modern React frontend with a powerful Python backend to provide real-time insights into vehicle registration trends across India.

## 🚗 Features

### Frontend (React + TypeScript)
- 📊 **Interactive Charts**: Real-time visualization using Recharts
- 🎛️ **Advanced Filters**: Date range, vehicle category, and manufacturer filtering
- 📱 **Responsive Design**: Works seamlessly on all devices
- 🎨 **Modern UI**: Built with Tailwind CSS and shadcn/ui components
- 📈 **Market Insights**: AI-generated insights and trend analysis

### Backend (Python + FastAPI)
- 🔄 **Data Collection**: Fetches data from Vahan Dashboard
- 📊 **Analytics Engine**: YoY and QoQ calculations
- 🗄️ **Database**: SQLite for efficient data storage
- 🚀 **Fast APIs**: RESTful endpoints with automatic documentation
- 📈 **Insights Generation**: Automated trend detection and market analysis

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **Recharts** for data visualization
- **React Query** for API state management

### Backend
- **FastAPI** for high-performance APIs
- **SQLite** for data storage
- **Pandas** for data analysis
- **Pydantic** for data validation
- **Uvicorn** for ASGI server

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python start_project.py
```

This will:
- Install all dependencies (Python + Node.js)
- Initialize the database with sample data
- Start both backend and frontend servers
- Open your browser to the dashboard

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend**:
   ```bash
   python run.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd investor-fleet-vision
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

## 📊 Dashboard Features

### Real-time Data Visualization
- **Area Charts**: Vehicle registration trends over time
- **Category Breakdown**: 2W, 3W, and 4W registration analysis
- **Manufacturer Performance**: Top performers with YoY/QoQ metrics

### Advanced Filtering
- **Date Range Picker**: Select custom time periods
- **Vehicle Categories**: Filter by 2W, 3W, or 4W
- **Manufacturer Multi-select**: Choose specific manufacturers

### Market Insights
- **Growth Analysis**: Automatic YoY and QoQ calculations
- **Trend Detection**: AI-powered insight generation
- **Market Share**: Category and manufacturer market analysis

## 🔧 Project Structure

```
├── investor-fleet-vision/          # React frontend
│   ├── src/
│   │   ├── components/             # UI components
│   │   ├── services/               # API service layer
│   │   ├── context/                # React context providers
│   │   └── pages/                  # Application pages
│   └── package.json
├── backend/                        # Python backend
│   ├── main.py                     # FastAPI application
│   ├── data_collector.py           # Data fetching logic
│   ├── database.py                 # Database operations
│   ├── analytics.py                # YoY/QoQ calculations
│   └── requirements.txt
├── start_project.py                # Automated setup script
└── README.md
```

## 📡 API Endpoints

- **GET `/api/registrations`** - Get filtered registration data
- **GET `/api/insights`** - Get market insights and trends
- **GET `/api/manufacturers`** - Get available manufacturers
- **POST `/api/refresh-data`** - Refresh data from Vahan Dashboard

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🎯 Key Metrics

The dashboard provides several key metrics for investment analysis:

- **YoY Growth**: Year-over-year percentage change
- **QoQ Growth**: Quarter-over-quarter percentage change
- **Market Share**: Category and manufacturer distribution
- **Registration Trends**: Historical patterns and forecasts
- **Top Performers**: Fastest-growing categories and manufacturers

## 🔄 Data Flow

1. **Data Collection**: Python backend fetches data from Vahan Dashboard
2. **Processing**: Raw data is cleaned and stored in SQLite database
3. **Analytics**: YoY/QoQ calculations and trend analysis
4. **API Layer**: FastAPI serves processed data to frontend
5. **Visualization**: React frontend displays interactive charts and insights

## 🌐 Development

### Frontend Development
```bash
cd investor-fleet-vision
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd backend
python main.py       # Start with auto-reload
python run.py        # Start with data initialization
```

## 📈 Future Enhancements

- [ ] **Real-time Data**: WebSocket integration for live updates
- [ ] **Advanced Analytics**: ML-powered forecasting
- [ ] **Export Features**: PDF/Excel report generation
- [ ] **Authentication**: User management and role-based access
- [ ] **Mobile App**: React Native mobile application
- [ ] **More Data Sources**: Integration with additional vehicle databases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- **Vahan Dashboard**: For providing vehicle registration data
- **shadcn/ui**: For beautiful UI components
- **FastAPI**: For the excellent Python web framework
- **Recharts**: For powerful React charting capabilities

---

**Live Demo**: Backend at `http://localhost:8000` | Frontend at `http://localhost:5173`
