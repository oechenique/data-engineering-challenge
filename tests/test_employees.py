import pytest
from fastapi.testclient import TestClient
import pandas as pd

def test_upload_employees_success(client, sample_csv):
    """Test de carga exitosa de empleados"""
    with open(sample_csv, 'rb') as f:
        response = client.post(
            "/api/v1/upload/hired_employees",
            files={"file": ("test.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["summary"]["processed_successfully"] > 0

def test_upload_employees_invalid_csv(client):
    """Test de manejo de CSV inválido"""
    response = client.post(
        "/api/v1/upload/hired_employees",
        files={"file": ("test.csv", b"invalid,csv", "text/csv")}
    )
    assert response.status_code == 400

def test_upload_employees_missing_required_columns(client):
    """Test de manejo de columnas faltantes"""
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("id,name\n")  # Faltan columnas requeridas
        f.write("1,John Doe\n")
        f.seek(0)
        response = client.post(
            "/api/v1/upload/hired_employees",
            files={"file": ("test.csv", f, "text/csv")}
        )
    assert response.status_code == 400