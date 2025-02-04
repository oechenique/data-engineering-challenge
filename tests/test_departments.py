import pytest
from fastapi.testclient import TestClient

def test_upload_departments_success(client, sample_csv):
    """Test de carga exitosa de departamentos"""
    # Crear CSV temporal de departamentos
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("1,IT\n2,HR\n")
        f.seek(0)
        response = client.post(
            "/api/v1/upload/departments",
            files={"file": ("departments.csv", f, "text/csv")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"].endswith("departments added successfully")

def test_upload_departments_duplicate_id(client):
    """Test de manejo de IDs duplicados"""
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("1,IT\n1,HR\n")  # ID duplicado
        f.seek(0)
        response = client.post(
            "/api/v1/upload/departments",
            files={"file": ("departments.csv", f, "text/csv")}
        )
    assert response.status_code == 500