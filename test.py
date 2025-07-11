import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the default 'postgres' database without a password
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    host="localhost",
    port="5432"
)

# Allow creating a database
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor()

# Create database 'machine_status'
cur.execute("CREATE DATABASE machine_status")

cur.close()
conn.close()

print("Database 'machine_status' created successfully!")
