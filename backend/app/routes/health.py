"""Health check endpoints."""

import logging
from fastapi import APIRouter, status

from app.models.ml_model import MLModel
from app.models.schemas import HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize model
ml_model = MLModel()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check API and model health status"
)
def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        model_loaded=ml_model.is_loaded()
    )


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness Check",
    description="Check if API is ready for requests"
)
def readiness_check() -> dict:
    """Readiness check endpoint."""
    return {
        "ready": ml_model.is_loaded(),
        "model_info": ml_model.get_model_info()
    }


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    summary="System Info",
    description="Get system and model information"
)
def get_info() -> dict:
    """Get system information."""
    return {
        "api": {
            "name": "FlowPredict AI API",
            "version": "1.0.0"
        },
        "model": ml_model.get_model_info()
    }