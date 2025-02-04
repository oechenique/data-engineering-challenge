import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def setup_test_data(client, db_session):
    """Fixture para cargar datos de prueba"""
    # Cargar departamentos
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("1,IT\n2,HR\n")
        f.seek(0)
        client.post("/api/v1/upload/departments", 
                   files={"file": ("departments.csv", f, "text/csv")})
    
    # Cargar trabajos
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("1,Developer\n2,Manager\n")
        f.seek(0)
        client.post("/api/v1/upload/jobs", 
                   files={"file": ("jobs.csv", f, "text/csv")})
    
    # Cargar empleados
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w') as f:
        f.write("id,name,datetime,department_id,job_id\n")
        f.write("1,John,2021-01-01T00:00:00Z,1,1\n")
        f.write("2,Jane,2021-02-01T00:00:00Z,1,2\n")
        f.seek(0)
        client.post("/api/v1/upload/hired_employees", 
                   files={"file": ("employees.csv", f, "text/csv")})

def test_quarterly_hiring(client, setup_test_data):
    """Test de métricas trimestrales"""
    response = client.get("/api/v1/metrics/quarterly-hiring")
    assert response.status_code == 200
    data = response.json()
    assert "rows" in data
    assert len(data["rows"]) > 0

def test_departments_above_mean(client, setup_test_data):
    """Test de departamentos sobre la media"""
    response = client.get("/api/v1/metrics/departments-above-mean")
    assert response.status_code == 200
    data = response.json()
    assert "rows" in data