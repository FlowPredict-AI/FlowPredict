# FlowPredict AI Backend

FastAPI backend service for oil well production rate prediction.

## 📋 Features

- **REST API**: FastAPI-based endpoints for predictions
- **ML Models**: Scikit-learn ensemble models
- **Validation**: Pydantic request/response validation
- **Error Handling**: Comprehensive error messages
- **Testing**: Unit tests with pytest
- **Logging**: Structured logging throughout
- **CORS**: Cross-origin resource sharing configured

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip or poetry

### Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file**
   ```bash
   cp .env.example .env
   ```

### Running the Server

```bash
# Development mode with auto-reload
python -m uvicorn app.main:app --reload

# Production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Docs

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Base URL

```
http://localhost:8000/api/v1
```

## 🔌 Endpoints

### Health Check

```http
GET /api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true
}
```

### Prediction

```http
POST /api/v1/predict
Content-Type: application/json

{
  "porosity": 0.25,
  "permeability": 100.0,
  "pressure": 3000.0,
  "depth": 10000.0,
  "temperature": 200.0
}
```

Response:
```json
{
  "production_rate": 450.5,
  "confidence_lower": 380.2,
  "confidence_upper": 520.8,
  "model_version": "1.0.0",
  "prediction_id": "pred_123abc"
}
```

### Batch Prediction

```http
POST /api/v1/batch-predict
Content-Type: application/json

[
  {"porosity": 0.25, "permeability": 100.0, "pressure": 3000.0, "depth": 10000.0, "temperature": 200.0},
  {"porosity": 0.30, "permeability": 150.0, "pressure": 3500.0, "depth": 11000.0, "temperature": 210.0}
]
```

Response:
```json
{
  "predictions": [...],
  "statistics": {
    "count": 2,
    "average_rate": 500.5,
    "min_rate": 450.0,
    "max_rate": 551.0
  }
}
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_predictions.py

# Run with verbose output
pytest -v
```

### Test Coverage

```bash
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html
```

## 📊 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   ├── schemas.py       # Pydantic models
│   │   └── ml_model.py      # ML model wrapper
│   ├── routes/
│   │   ├── health.py        # Health check endpoints
│   │   └── predictions.py   # Prediction endpoints
│   └── utils/
│       ├── data_processing.py
│       └── model_loader.py
├── tests/
│   ├── test_health.py
│   ├── test_predictions.py
│   └── test_ml_model.py
├── models/                  # Saved ML models
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔧 Configuration

Edit `.env` file:

```bash
# Environment
ENVIRONMENT=development
DEBUG=True

# API
API_PORT=8000
API_HOST=0.0.0.0

# ML Model
MODEL_PATH=./models/production_model.pkl
CONFIDENCE_LEVEL=0.95

# Frontend
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

## 📦 Dependencies

### Core
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation

### Data & ML
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning
- **joblib**: Model persistence

### Development
- **pytest**: Testing framework
- **black**: Code formatter
- **pylint**: Linter
- **flake8**: Style guide

## 🚨 Error Handling

The API returns structured error responses:

```json
{
  "detail": "Invalid input: Porosity must be between 0 and 1",
  "error_code": "VALIDATION_ERROR",
  "type": "ValueError"
}
```

## 📝 Logging

Logs are written to:
- **Console**: Real-time output
- **File**: `logs/app.log` (if configured)

## 🔒 Security

- Input validation with Pydantic
- CORS configured for frontend
- Error messages don't leak sensitive data
- Environment variables for configuration

## 🐛 Troubleshooting

### Model not loading

```bash
# Check model file exists
ls -la models/

# Check permissions
chmod 644 models/production_model.pkl
```

### CORS issues

Update `CORS_ORIGINS` in `.env` and restart server.

### Port already in use

```bash
# Use different port
python -m uvicorn app.main:app --port 8001
```

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

## 📧 Support

For issues or questions, please open a GitHub issue.