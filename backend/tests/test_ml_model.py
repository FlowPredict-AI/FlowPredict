"""Tests for ML model wrapper."""

import pytest
from app.models.ml_model import MLModel
from app.models.schemas import PredictionRequest


class TestMLModel:
    """Test ML model wrapper."""

    @pytest.fixture
    def ml_model(self):
        """Fixture for ML model."""
        return MLModel()

    @pytest.fixture
    def valid_request(self):
        """Fixture for valid prediction request."""
        return PredictionRequest(
            porosity=0.25,
            permeability=100.0,
            pressure=3000.0,
            depth=10000.0,
            temperature=200.0
        )

    def test_model_initialization(self, ml_model):
        """Test model is initialized."""
        assert ml_model.model is not None

    def test_model_is_loaded(self, ml_model):
        """Test model is loaded."""
        assert ml_model.is_loaded() is True

    def test_prediction_returns_valid_response(self, ml_model, valid_request):
        """Test prediction returns valid response."""
        response = ml_model.predict(valid_request)
        
        assert response.production_rate > 0
        assert response.confidence_lower >= 0
        assert response.confidence_upper > response.production_rate
        assert response.model_version == "1.0.0"
        assert response.prediction_id.startswith("pred_")

    def test_prediction_confidence_interval(self, ml_model, valid_request):
        """Test confidence interval is valid."""
        response = ml_model.predict(valid_request)
        
        assert response.confidence_lower < response.production_rate
        assert response.production_rate < response.confidence_upper

    def test_multiple_predictions_consistency(self, ml_model, valid_request):
        """Test multiple predictions for same input."""
        response1 = ml_model.predict(valid_request)
        response2 = ml_model.predict(valid_request)
        
        # Predictions should be the same for same input
        assert response1.production_rate == response2.production_rate

    def test_different_inputs_give_different_predictions(self, ml_model):
        """Test different inputs give different predictions."""
        request1 = PredictionRequest(
            porosity=0.25,
            permeability=100.0,
            pressure=3000.0,
            depth=10000.0,
            temperature=200.0
        )
        request2 = PredictionRequest(
            porosity=0.35,
            permeability=200.0,
            pressure=4000.0,
            depth=12000.0,
            temperature=250.0
        )
        
        response1 = ml_model.predict(request1)
        response2 = ml_model.predict(request2)
        
        # Different inputs should give different predictions
        assert response1.production_rate != response2.production_rate

    def test_get_model_info(self, ml_model):
        """Test get model info."""
        info = ml_model.get_model_info()
        
        assert "version" in info
        assert "type" in info
        assert "loaded" in info
        assert info["loaded"] is True