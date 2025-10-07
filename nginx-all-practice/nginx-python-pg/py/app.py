from flask import Flask
import psycopg2 as pg
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
container_name = os.getenv("APP_NAME", "Unknown Container")

# Database connection retry function
def get_conn(retries=10, delay=3):
    """Attempt to connect to Postgres with retries."""
    for attempt in range(1, retries + 1):
        try:
            conn = pg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            print("Database connection successful!")
            return conn
        except pg.OperationalError as e:
            print(f"[Attempt {attempt}/{retries}] Database not ready: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to database after several attempts")

# Fetch all rows from table
def fetch_data_from_csun_nav():
    conn = get_conn()
    cur = conn.cursor()
    
    debug_info = []
    
    # Debug connection info
    debug_info.append(f"Connected to database: {os.getenv('DB_NAME')}")
    debug_info.append(f"Host: {os.getenv('DB_HOST')}")
    debug_info.append(f"User: {os.getenv('DB_USER')}")
    
    # Check current database
    cur.execute("SELECT current_database();")
    current_db = cur.fetchone()[0]
    debug_info.append(f"Current database: {current_db}")
    
    # Get and print available tables
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cur.fetchall()
    debug_info.append(f"Available tables: {tables}")
    
    # Check if test table exists specifically
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'test');")
    table_exists = cur.fetchone()[0]
    debug_info.append(f"Test table exists: {table_exists}")
    
    # Try to query the table
    try:
        cur.execute("SELECT * FROM test")
        rows = cur.fetchall()
        debug_info.append(f"Successfully queried test table, got {len(rows)} rows")
    except Exception as e:
        debug_info.append(f"Error querying test table: {e}")
        rows = debug_info  # Return debug info instead
    
    cur.close()
    conn.close()
    return rows
# Routes
@app.route("/")
def home():
    rows = fetch_data_from_csun_nav()
    return f"<h1>NGINX-Python-Postgres demo</h1><pre>{rows}</pre>"

@app.route("/check-server")
def check_server():
    return {"message": f"You are on this server: {container_name}"}

if __name__ == "__main__":
    # Run Flask
    app.run(host="0.0.0.0", port=5000)