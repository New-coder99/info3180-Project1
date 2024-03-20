from flask import Flask
import psycopg2
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
from app import views

def get_db_connection():
    conn = psycopg2.connect(
        dbname="info3180project1",
        user="postgres",
        password="chickenback",
        host="localhost",
        port="5432"  # Default PostgreSQL port
    )
    return conn

Query="""
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    location VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL,
    type VARCHAR(20) NOT NULL,
    description TEXT,
    photo varchar(255)
);"""

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("DROP TABLE IF Exists properties")
cursor.execute(Query)
conn.commit()
conn.close()