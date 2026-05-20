# FlowPredict AI

[![Python Tests](https://github.com/FlowPredict-AI/FlowPredict/workflows/Backend%20Tests/badge.svg)](https://github.com/FlowPredict-AI/FlowPredict/actions)
[![React Tests](https://github.com/FlowPredict-AI/FlowPredict/workflows/Frontend%20Tests/badge.svg)](https://github.com/FlowPredict-AI/FlowPredict/actions)
[![Code Quality](https://github.com/FlowPredict-AI/FlowPredict/workflows/Code%20Quality/badge.svg)](https://github.com/FlowPredict-AI/FlowPredict/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

FlowPredict AI is an intelligent reservoir performance analysis system that predicts oil well production rates using machine learning. Petroleum engineers input reservoir parameters such as porosity, permeability, pressure, and depth, and the system predicts expected production rate in barrels per day (BOPD).

### Key Features
- 🤖 **ML-Powered Predictions**: Scikit-learn models trained on historical reservoir data
- 📊 **Interactive Dashboard**: React-based visualization and analysis tools
- ⚡ **REST API**: FastAPI backend for seamless integration
- 🔒 **Production-Ready**: Comprehensive testing, logging, and error handling
- 📈 **Confidence Intervals**: Uncertainty quantification for predictions
- 🔄 **CI/CD Automation**: GitHub Actions for testing and deployment

## 🏗️ Architecture

```
FlowPredict/
├── backend/              # Python FastAPI application
│   ├── app/
│   │   ├── main.py      # FastAPI app entry point
│   │   ├── models/      # ML models and schemas
│   │   ├── routes/      # API endpoints
│   │   └── utils/       # Helper functions
│   ├── tests/           # Unit and integration tests
│   └── requirements.txt  # Python dependencies
├── frontend/            # React TypeScript dashboard
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json     # npm dependencies
└── docs/                # Documentation
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend API will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend dashboard will be available at `http://localhost:3000`

## 📖 API Documentation

Interactive API docs available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

See [API.md](docs/API.md) for detailed endpoint documentation.

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 ML Model

The system uses trained scikit-learn models for production predictions:
- **Model Type**: Random Forest Regressor
- **Features**: Porosity, Permeability, Pressure, Depth, Temperature
- **Target**: Production Rate (BOPD)
- **Confidence**: 95% prediction intervals

See [ML_MODEL.md](docs/ML_MODEL.md) for model training and evaluation details.

## 🔧 Configuration

Create a `.env` file in the backend directory:

```bash
cp backend/.env.example backend/.env
```

Edit with your configuration:
```
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=sqlite:///./flowpredict.db
MODEL_PATH=./models/production_model.pkl
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and formatting
- Pull request process
- Issue reporting
- Development workflow

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support

For issues, questions, or suggestions:
1. Check [existing issues](https://github.com/FlowPredict-AI/FlowPredict/issues)
2. [Create a new issue](https://github.com/FlowPredict-AI/FlowPredict/issues/new)
3. See [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## 🗺️ Roadmap

- [ ] Enhanced ML models (XGBoost, Neural Networks)
- [ ] Historical data storage and analysis
- [ ] Multi-field reservoir analysis
- [ ] Real-time production monitoring
- [ ] Advanced visualization and reporting
- [ ] Mobile app (React Native)

---

**Built with ❤️ for petroleum engineers**