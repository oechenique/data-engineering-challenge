import pytest
from fastapi.testclient import TestClient

def test_upload_jobs_success(client):
    """Test de carga exitosa de trabajos"""
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("1,Developer\n2,Manager\n")
        f.seek(0)
        response = client.post(
            "/api/v1/upload/jobs",
            files={"file": ("jobs.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"].endswith("jobs added successfully")

def test_upload_jobs_invalid_format(client):
    """Test de manejo de formato inválido"""
    response = client.post(
        "/api/v1/upload/jobs",
        files={"file": ("jobs.csv", b"invalid", "text/csv")}
    )
    assert response.status_code == 400