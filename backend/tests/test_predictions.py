"""Tests for prediction endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestPredictionEndpoints:
    """Test prediction endpoints."""

    @pytest.fixture
    def valid_request(self):
        """Fixture for valid prediction request."""
        return {
            "porosity": 0.25,
            "permeability": 100.0,
            "pressure": 3000.0,
            "depth": 10000.0,
            "temperature": 200.0
        }

    def test_predict_with_valid_input(self, valid_request):
        """Test prediction with valid input."""
        response = client.post("/api/v1/predict", json=valid_request)
        assert response.status_code == 200

    def test_predict_response_structure(self, valid_request):
        """Test prediction response structure."""
        response = client.post("/api/v1/predict", json=valid_request)
        data = response.json()
        
        assert "production_rate" in data
        assert "confidence_lower" in data
        assert "confidence_upper" in data
        assert "model_version" in data
        assert "prediction_id" in data

    def test_production_rate_is_positive(self, valid_request):
        """Test production rate is positive."""
        response = client.post("/api/v1/predict", json=valid_request)
        data = response.json()
        
        assert data["production_rate"] > 0

    def test_confidence_interval_valid(self, valid_request):
        """Test confidence interval is valid."""
        response = client.post("/api/v1/predict", json=valid_request)
        data = response.json()
        
        assert data["confidence_lower"] < data["production_rate"]
        assert data["production_rate"] < data["confidence_upper"]
        assert data["confidence_lower"] >= 0

    def test_predict_with_invalid_porosity(self):
        """Test prediction with invalid porosity."""
        request = {
            "porosity": 1.5,  # Invalid: > 1
            "permeability": 100.0,
            "pressure": 3000.0,
            "depth": 10000.0,
            "temperature": 200.0
        }
        response = client.post("/api/v1/predict", json=request)
        assert response.status_code == 422  # Validation error

    def test_predict_with_negative_permeability(self):
        """Test prediction with negative permeability."""
        request = {
            "porosity": 0.25,
            "permeability": -100.0,  # Invalid: negative
            "pressure": 3000.0,
            "depth": 10000.0,
            "temperature": 200.0
        }
        response = client.post("/api/v1/predict", json=request)
        assert response.status_code == 422  # Validation error

    def test_batch_predict_with_multiple_requests(self, valid_request):
        """Test batch prediction with multiple requests."""
        requests = [valid_request] * 3
        response = client.post("/api/v1/batch-predict", json=requests)
        assert response.status_code == 200

    def test_batch_predict_response_structure(self, valid_request):
        """Test batch prediction response structure."""
        requests = [valid_request] * 2
        response = client.post("/api/v1/batch-predict", json=requests)
        data = response.json()
        
        assert "predictions" in data
        assert "statistics" in data
        assert len(data["predictions"]) == 2

    def test_batch_predict_statistics(self, valid_request):
        """Test batch prediction statistics."""
        requests = [valid_request] * 3
        response = client.post("/api/v1/batch-predict", json=requests)
        data = response.json()
        stats = data["statistics"]
        
        assert stats["count"] == 3
        assert stats["average_rate"] > 0
        assert stats["min_rate"] > 0
        assert stats["max_rate"] > 0