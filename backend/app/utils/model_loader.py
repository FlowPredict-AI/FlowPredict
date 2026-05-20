"""Model loading and management utilities."""

import logging
import os
from pathlib import Path

import joblib

logger = logging.getLogger(__name__)


class ModelManager:
    """Manage model loading, saving, and versioning."""

    def __init__(self, model_dir: str = "./models"):
        """Initialize model manager.

        Args:
            model_dir: Directory for storing models
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)

    def save_model(self, model, name: str, version: str = "1.0.0") -> str:
        """Save model to disk.

        Args:
            model: Model to save
            name: Model name
            version: Model version

        Returns:
            Path to saved model
        """
        try:
            filename = f"{name}_v{version}.pkl"
            filepath = self.model_dir / filename
            
            joblib.dump(model, filepath)
            logger.info(f"Model saved to {filepath}")
            
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

    def load_model(self, filepath: str):
        """Load model from disk.

        Args:
            filepath: Path to model file

        Returns:
            Loaded model
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Model file not found: {filepath}")
            
            model = joblib.load(filepath)
            logger.info(f"Model loaded from {filepath}")
            
            return model
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def list_models(self) -> list:
        """List all saved models.

        Returns:
            List of model filenames
        """
        if not self.model_dir.exists():
            return []
        
        models = list(self.model_dir.glob("*.pkl"))
        return [m.name for m in models]

    def get_latest_model(self, name: str):
        """Get latest version of a model.

        Args:
            name: Model name

        Returns:
            Latest model
        """
        models = list(self.model_dir.glob(f"{name}_v*.pkl"))
        if not models:
            raise FileNotFoundError(f"No models found for {name}")
        
        # Sort by modification time
        latest = max(models, key=os.path.getmtime)
        return self.load_model(str(latest))