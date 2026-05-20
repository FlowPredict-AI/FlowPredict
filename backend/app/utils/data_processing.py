"""Data processing utilities."""

import logging
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def validate_reservoir_data(data: dict) -> bool:
    """Validate reservoir data.

    Args:
        data: Dictionary of reservoir parameters

    Returns:
        True if data is valid

    Raises:
        ValueError: If data is invalid
    """
    required_fields = ['porosity', 'permeability', 'pressure', 'depth', 'temperature']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(data[field], (int, float)):
            raise ValueError(f"Field {field} must be numeric")
    
    # Validate ranges
    if not (0 <= data['porosity'] <= 1):
        raise ValueError("Porosity must be between 0 and 1")
    
    if data['permeability'] <= 0:
        raise ValueError("Permeability must be positive")
    
    if data['pressure'] <= 0:
        raise ValueError("Pressure must be positive")
    
    if data['depth'] <= 0:
        raise ValueError("Depth must be positive")
    
    if data['temperature'] <= 0:
        raise ValueError("Temperature must be positive")
    
    return True


def normalize_features(X: np.ndarray, scaler: StandardScaler = None) -> Tuple[np.ndarray, StandardScaler]:
    """Normalize features using StandardScaler.

    Args:
        X: Feature matrix
        scaler: Pre-fitted scaler (optional)

    Returns:
        Normalized features and scaler
    """
    if scaler is None:
        scaler = StandardScaler()
        X_normalized = scaler.fit_transform(X)
    else:
        X_normalized = scaler.transform(X)
    
    return X_normalized, scaler


def load_training_data(filepath: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load training data from CSV.

    Args:
        filepath: Path to CSV file

    Returns:
        Features and target variable
    """
    try:
        df = pd.read_csv(filepath)
        logger.info(f"Loaded data from {filepath}: {df.shape[0]} samples")
        
        # Extract features and target
        feature_cols = ['porosity', 'permeability', 'pressure', 'depth', 'temperature']
        X = df[feature_cols]
        y = df['production_rate']
        
        return X, y
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def remove_outliers(X: pd.DataFrame, y: pd.Series, threshold: float = 3.0) -> Tuple[pd.DataFrame, pd.Series]:
    """Remove outliers using z-score method.

    Args:
        X: Features
        y: Target variable
        threshold: Z-score threshold

    Returns:
        Cleaned features and target
    """
    from scipy import stats
    
    z_scores = np.abs(stats.zscore(y))
    mask = z_scores < threshold
    
    X_clean = X[mask]
    y_clean = y[mask]
    
    removed = len(y) - len(y_clean)
    logger.info(f"Removed {removed} outliers")
    
    return X_clean, y_clean


def calculate_statistics(y_pred: np.ndarray, y_true: np.ndarray) -> dict:
    """Calculate prediction statistics.

    Args:
        y_pred: Predicted values
        y_true: Actual values

    Returns:
        Dictionary of statistics
    """
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae),
        'r2_score': float(r2)
    }