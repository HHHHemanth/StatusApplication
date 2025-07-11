from sqlalchemy import create_engine, MetaData, Table
from tabulate import tabulate

# Connect to the PostgreSQL database (no password)
DATABASE_URL = "postgresql://postgres@localhost:5432/machine_status"
engine = create_engine(DATABASE_URL)

# Reflect the existing database
metadata = MetaData()
metadata.reflect(bind=engine)
status_table = metadata.tables["status"]

# Fetch all data
with engine.connect() as conn:
    result = conn.execute(status_table.select())
    rows = result.fetchall()
    headers = result.keys()

# Display using tabulate
if rows:
    print(tabulate(rows, headers=headers, tablefmt="grid"))
else:
    print("No data found in the 'status' table.")
