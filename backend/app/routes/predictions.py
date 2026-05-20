"""Prediction endpoints."""

import logging
from fastapi import APIRouter, HTTPException, status

from app.models.ml_model import MLModel
from app.models.schemas import PredictionRequest, PredictionResponse, ErrorResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize model
ml_model = MLModel()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Make Prediction",
    description="Predict oil well production rate based on reservoir parameters",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input parameters"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
def make_prediction(request: PredictionRequest) -> PredictionResponse:
    """Make a production rate prediction.

    Args:
        request: Prediction request with reservoir parameters

    Returns:
        Prediction response with production rate and confidence interval

    Raises:
        HTTPException: If model is not loaded or prediction fails
    """
    try:
        if not ml_model.is_loaded():
            logger.error("ML model is not loaded")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model is not available. Please try again later."
            )

        prediction = ml_model.predict(request)
        logger.info(f"Prediction successful: {prediction.prediction_id}")
        return prediction

    except ValueError as e:
        logger.warning(f"Invalid input: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed. Please try again."
        )


@router.post(
    "/batch-predict",
    status_code=status.HTTP_200_OK,
    summary="Batch Prediction",
    description="Make predictions for multiple sets of reservoir parameters"
)
def batch_predict(requests: list[PredictionRequest]) -> dict:
    """Make batch predictions.

    Args:
        requests: List of prediction requests

    Returns:
        Dictionary with predictions and statistics
    """
    try:
        if not ml_model.is_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ML model is not available."
            )

        predictions = [ml_model.predict(req) for req in requests]

        # Calculate statistics
        production_rates = [p.production_rate for p in predictions]
        avg_rate = sum(production_rates) / len(production_rates)
        min_rate = min(production_rates)
        max_rate = max(production_rates)

        logger.info(f"Batch prediction successful: {len(predictions)} predictions")

        return {
            "predictions": predictions,
            "statistics": {
                "count": len(predictions),
                "average_rate": avg_rate,
                "min_rate": min_rate,
                "max_rate": max_rate
            }
        }

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch prediction failed."
        )