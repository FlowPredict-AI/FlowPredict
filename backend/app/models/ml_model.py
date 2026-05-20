"""Machine Learning model wrapper for predictions."""

import logging
import os
import uuid
from typing import Tuple

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from app.models.schemas import PredictionRequest, PredictionResponse

logger = logging.getLogger(__name__)


class MLModel:
    """Wrapper for ML model predictions."""

    def __init__(self, model_path: str = None):
        """Initialize ML model.

        Args:
            model_path: Path to saved model file
        """
        self.model_path = model_path or os.getenv(
            "MODEL_PATH", "./models/production_model.pkl"
        )
        self.model = None
        self.scaler = None
        self.confidence_level = float(os.getenv("CONFIDENCE_LEVEL", 0.95))
        self.model_version = "1.0.0"
        self._load_model()

    def _load_model(self) -> None:
        """Load model from disk."""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.warning(
                    f"Model file not found at {self.model_path}. "
                    "Using default model."
                )
                self._create_default_model()
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self._create_default_model()

    def _create_default_model(self) -> None:
        """Create a default model for testing."""
        logger.info("Creating default Random Forest model")
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        # Create dummy training data for initialization
        X_dummy = np.array([
            [0.25, 100, 3000, 10000, 200],
            [0.30, 150, 3500, 11000, 210],
            [0.20, 80, 2500, 9000, 190]
        ])
        y_dummy = np.array([450, 550, 350])
        self.model.fit(X_dummy, y_dummy)

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """Generate prediction for given parameters.

        Args:
            request: Prediction request with reservoir parameters

        Returns:
            PredictionResponse with predicted production rate and confidence interval
        """
        try:
            # Extract features
            features = np.array([[
                request.porosity,
                request.permeability,
                request.pressure,
                request.depth,
                request.temperature
            ]])

            # Make prediction
            if hasattr(self.model, 'estimators_'):
                # For ensemble models, get predictions from all estimators
                predictions = np.array([
                    estimator.predict(features)[0]
                    for estimator in self.model.estimators_
                ])
                mean_prediction = predictions.mean()
                std_prediction = predictions.std()
            else:
                mean_prediction = self.model.predict(features)[0]
                std_prediction = mean_prediction * 0.15  # 15% uncertainty

            # Calculate confidence interval
            z_score = 1.96  # 95% confidence
            confidence_lower = mean_prediction - (z_score * std_prediction)
            confidence_upper = mean_prediction + (z_score * std_prediction)

            # Ensure non-negative predictions
            confidence_lower = max(0, confidence_lower)

            return PredictionResponse(
                production_rate=float(mean_prediction),
                confidence_lower=float(confidence_lower),
                confidence_upper=float(confidence_upper),
                model_version=self.model_version,
                prediction_id=f"pred_{uuid.uuid4().hex[:8]}"
            )

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

    def is_loaded(self) -> bool:
        """Check if model is loaded.

        Returns:
            True if model is loaded
        """
        return self.model is not None

    def get_model_info(self) -> dict:
        """Get model information.

        Returns:
            Dictionary with model info
        """
        return {
            "version": self.model_version,
            "type": type(self.model).__name__,
            "loaded": self.is_loaded(),
            "path": self.model_path,
            "confidence_level": self.confidence_level
        }