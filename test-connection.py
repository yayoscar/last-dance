import os
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    print(f"Conectando a: {DATABASE_URL}")

    conn = psycopg2.connect(
        dbname="last-dance",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("SELECT current_database();")
    db_name = cur.fetchone()
    print(f"✅ Conectado a la base de datos: {db_name[0]}")

    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")
