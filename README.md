# 🚀 Globant Data Engineering Challenge

こんにちは！Welcome to the Data Engineering Challenge solution for Globant, showcasing a robust and scalable approach to historical data migration and analysis using Python and PostgreSQL.

## Overview
This project demonstrates a comprehensive data engineering solution with key capabilities:
- **Data Migration**: Seamless CSV to PostgreSQL data transfer
- **API Development**: RESTful endpoints for data management
- **Batch Processing**: Efficient handling of large datasets
- **Metric Analysis**: Advanced hiring analytics
- **Containerization**: Docker-based deployment

## Why This Approach?
The solution offers significant advantages for data engineering challenges:
- **Scalability**: Designed to handle large-volume data migrations
- **Flexibility**: Modular architecture for easy extension
- **Performance**: Optimized batch processing and database interactions
- **Reliability**: Robust error handling and data validation

## Project Components 📦

### 🛠 Technical Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest

### 📂 Project Structure
```
├── app/
│   ├── routes/           # API Endpoints
│   ├── models/           # SQLAlchemy Models
│   ├── services/         # Business Logic
│   └── config/           # Configurations
├── tests/               # Unit & Integration Tests
└── docker/             # Docker Configuration
```

## Getting Started 🚀

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- PostgreSQL

### Quick Setup
1. Clone the repository
```bash
git clone https://github.com/[your-username]/globant-data-engineering-challenge.git
cd globant-data-engineering-challenge
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
.\venv\Scripts\activate   # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Launch with Docker
```bash
docker-compose up -d
```

## Key Endpoints 📊

### Data Upload
- `POST /api/v1/upload/departments`: Department data
- `POST /api/v1/upload/jobs`: Job data
- `POST /api/v1/upload/hired_employees`: Employee data

### Analytics
- `GET /api/v1/metrics/quarterly_hires`: Q2 2021 hiring metrics
- `GET /api/v1/metrics/departments_above_mean`: High-performance departments

## New Features 🆕

### JSON to DataFrame Conversion
A new function simplifies JSON data extraction and visualization:
```python
import pandas as pd

def json_to_dataframe(json_data):
    if 'rows' in json_data:
        return pd.DataFrame(json_data['rows'])
    else:
        print("❌ Error: No data found")
        return pd.DataFrame()
```

#### Example Usage
```python
# Quarterly Hiring Metrics
quarterly_hiring = client.get_quarterly_hiring()
df_quarterly = json_to_dataframe(quarterly_hiring)
print(df_quarterly)

# Departments Above Mean
departments_above_mean = client.get_departments_above_mean()
df_above_mean = json_to_dataframe(departments_above_mean)
print(df_above_mean)
```

This ensures a seamless and structured approach to handling API responses.

## Testing 🧪
Run comprehensive test suite:
```bash
pytest tests/
```

## Performance Considerations
- Optimized for large-scale data processing
- Efficient batch insert mechanisms
- Comprehensive error handling
- Scalable API design

## Requirements
- pandas: `>=2.0.0`
- fastapi: `>=0.95.0`
- sqlalchemy: `>=2.0.0`
- psycopg2: `>=2.9.0`

## Let's Connect! 🌐

[![Twitter Badge](https://img.shields.io/badge/-@GastonEchenique-1DA1F2?style=flat&logo=x&logoColor=white&link=https://x.com/GastonEchenique)](https://x.com/GastonEchenique)
[![LinkedIn Badge](https://img.shields.io/badge/-Gastón_Echenique-0A66C2?style=flat&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/gaston-echenique/)](https://www.linkedin.com/in/gaston-echenique/)
[![GitHub Badge](https://img.shields.io/badge/-oechenique-333?style=flat&logo=github&logoColor=white&link=https://github.com/oechenique)](https://github.com/oechenique)
[![GeoAnalytics Badge](https://img.shields.io/badge/-GeoAnalytics_Site-2ecc71?style=flat&logo=google-earth&logoColor=white&link=https://oechenique.github.io/geoanalytics/)](https://oechenique.github.io/geoanalytics/)
[![Discord Badge](https://img.shields.io/badge/-Gastón|ガストン-5865F2?style=flat&logo=discord&logoColor=white&link=https://discord.com/users/gastonechenique)](https://discord.com/users/gastonechenique)

Developed as part of the Globant Data Engineering Challenge - 2025

よろしくお願いします！Let's transform data engineering together!