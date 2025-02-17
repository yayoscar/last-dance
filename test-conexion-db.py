# realiza una conexin de prueba con la BD
import os
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()

DB = os.getenv("PG_DB")
USER=os.getenv("PG_USER")
PWD=os.getenv("PG_PASSWORD")
HOST=os.getenv("PG_HOST")
PORT=os.getenv("PG_PORT")

try:
    print(f"Conectando a: {DB}")

    conn = psycopg2.connect(
        dbname=DB,
        user=USER,
        password=PWD,
        host=HOST,
        port=PORT
    )

    cur = conn.cursor()
    cur.execute("SELECT current_database();")
    db_name = cur.fetchone()
    print(f"✅ Conectado a la base de datos: {db_name[0]}")

    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")
