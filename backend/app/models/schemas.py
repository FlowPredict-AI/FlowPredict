"""Pydantic schemas for request/response validation."""

from typing import Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Schema for prediction request."""
    porosity: float = Field(..., ge=0.0, le=1.0, description="Porosity (0-1)")
    permeability: float = Field(..., gt=0, description="Permeability (mD)")
    pressure: float = Field(..., gt=0, description="Pressure (psi)")
    depth: float = Field(..., gt=0, description="Well depth (feet)")
    temperature: float = Field(..., gt=0, description="Temperature (°F)")

    class Config:
        schema_extra = {
            "example": {
                "porosity": 0.25,
                "permeability": 100.0,
                "pressure": 3000.0,
                "depth": 10000.0,
                "temperature": 200.0
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response."""
    production_rate: float = Field(..., description="Predicted production rate (BOPD)")
    confidence_lower: float = Field(..., description="Lower bound of 95% confidence interval")
    confidence_upper: float = Field(..., description="Upper bound of 95% confidence interval")
    model_version: str = Field(..., description="ML model version used")
    prediction_id: str = Field(..., description="Unique prediction identifier")

    class Config:
        schema_extra = {
            "example": {
                "production_rate": 450.5,
                "confidence_lower": 380.2,
                "confidence_upper": 520.8,
                "model_version": "1.0.0",
                "prediction_id": "pred_123abc"
            }
        }


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")

    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "model_loaded": True
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error response."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    type: Optional[str] = Field(None, description="Exception type")