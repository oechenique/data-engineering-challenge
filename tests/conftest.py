import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
import os
import tempfile
import pandas as pd

# Configuración de base de datos de prueba
SQLALCHEMY_TEST_DATABASE_URL = "postgresql://postgres:ToKy04g@9GaE@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    yield engine
    # Limpiar después de las pruebas
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_csv():
    """Crear un CSV temporal para pruebas"""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w') as f:
        f.write("id,name,datetime,department_id,job_id\n")
        f.write("1,John Doe,2021-01-01T00:00:00Z,1,1\n")
    yield f.name
    os.unlink(f.name)