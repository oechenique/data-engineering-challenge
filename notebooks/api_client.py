import pandas as pd
import requests
import logging
import os
import json

# ✅ Agregar la validación al inicio del archivo
def validate_csv(file_path):
    """Verifica que el archivo no esté vacío antes de enviarlo."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    if os.stat(file_path).st_size == 0:
        raise ValueError(f"El archivo {file_path} está vacío.")

class GlobantAPIClient:
    BASE_URL = "http://localhost:8000/api/v1"

    def __init__(self):
        self.session = requests.Session()

    def health_check(self):
        """Verifica si la API está en funcionamiento."""
        response = self.session.get("http://localhost:8000/api/health")
        return response.json()

    def upload_departments(self, file_path):
        """Sube el archivo de departamentos"""
        validate_csv(file_path)  # ✅ Validar antes de enviarlo
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = self.session.post(f"{self.BASE_URL}/upload/departments", files=files)
        return response.json()
    
    def upload_jobs(self, file_path):
        """Sube el archivo de trabajos"""
        validate_csv(file_path)  # ✅ Validar antes de enviarlo
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = self.session.post(f"{self.BASE_URL}/upload/jobs", files=files)
        return response.json()

    def upload_hired_employees(self, file_path, update_existing=True):
        """Sube el archivo de empleados contratados"""
        validate_csv(file_path)  # ✅ Validar antes de enviarlo
        with open(file_path, 'rb') as file:
            files = {'file': file}
            params = {'update_existing': str(update_existing).lower()}
            response = self.session.post(f"{self.BASE_URL}/upload/hired_employees", files=files, params=params)
        return response.json()

    def get_quarterly_hiring(self):
        """Obtener métricas trimestrales"""
        response = self.session.get(f"{self.BASE_URL}/metrics/quarterly-hiring")
        return self._handle_response(response)

    def get_departments_above_mean(self):
        """Obtener departamentos sobre la media"""
        response = self.session.get(f"{self.BASE_URL}/metrics/departments-above-mean")
        return self._handle_response(response)
    
    def _handle_response(self, response):
        """Maneja la respuesta de la API"""
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

# 🔥 **Testeo Automático**
if __name__ == "__main__":
    client = GlobantAPIClient()

    # 1️⃣ Verificar que la API está corriendo
    try:
        logger.info("Verificando conexión con la API...")
        health = client.health_check()
        logger.info(f"API Saludable: {json.dumps(health, indent=2)}")
    except Exception as e:
        logger.error("❌ API no responde")
        raise

    # 2️⃣ Cargar datos
    try:
        datasets = {
            "departments": "departments.csv",
            "jobs": "jobs.csv",
            "employees": "hired_employees.csv"
        }

        for dataset, file in datasets.items():
            logger.info(f"Cargando {dataset}...")
            upload_method = getattr(client, f"upload_{dataset}")
            result = upload_method(file)
            logger.info(f"✅ {dataset.capitalize()} cargado correctamente: {json.dumps(result, indent=2)}")

    except Exception as e:
        logger.error(f"❌ Error en la carga de datos: {str(e)}")
        raise

    # 3️⃣ Obtener métricas
    try:
        logger.info("📊 Obteniendo métricas trimestrales...")
        quarterly = client.get_quarterly_hiring()
        df_quarterly = pd.DataFrame(quarterly["rows"])
        logger.info(f"\nMétricas trimestrales:\n{df_quarterly}")

        logger.info("📊 Obteniendo departamentos sobre la media...")
        above_mean = client.get_departments_above_mean()
        df_above_mean = pd.DataFrame(above_mean["rows"])
        logger.info(f"\nDepartamentos sobre la media:\n{df_above_mean}")

    except Exception as e:
        logger.error(f"❌ Error obteniendo métricas: {str(e)}")
        raise