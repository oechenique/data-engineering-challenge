from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Configuración de la base de datos
USER = "postgres"
PASSWORD = "ToKy04g@9GaE"  # Asegurate de usar la contraseña correcta
HOST = "localhost"
PORT = "5432"
DB_NAME = "globant_db"

# Codifica la contraseña para evitar problemas con caracteres especiales
encoded_password = quote_plus(PASSWORD)

# Construye la URL de conexión
DATABASE_URL = f"postgresql://{USER}:{encoded_password}@{HOST}:{PORT}/{DB_NAME}"

# Intenta conectar a la base de datos
try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("✅ Conexión exitosa a PostgreSQL!")
    conn.close()
except Exception as e:
    print("❌ Error de conexión:", e)
