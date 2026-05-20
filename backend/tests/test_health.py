"""Tests for health check endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check_returns_200(self):
        """Test health check returns 200 OK."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_check_structure(self):
        """Test health check response structure."""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "model_loaded" in data
        assert data["status"] == "healthy"

    def test_readiness_check_returns_200(self):
        """Test readiness check returns 200 OK."""
        response = client.get("/api/v1/ready")
        assert response.status_code == 200

    def test_readiness_check_structure(self):
        """Test readiness check response structure."""
        response = client.get("/api/v1/ready")
        data = response.json()
        
        assert "ready" in data
        assert "model_info" in data

    def test_info_endpoint_returns_200(self):
        """Test info endpoint returns 200 OK."""
        response = client.get("/api/v1/info")
        assert response.status_code == 200

    def test_info_endpoint_structure(self):
        """Test info endpoint response structure."""
        response = client.get("/api/v1/info")
        data = response.json()
        
        assert "api" in data
        assert "model" in data
        assert data["api"]["name"] == "FlowPredict AI API"