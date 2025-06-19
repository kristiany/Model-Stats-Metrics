import psycopg
import os

PG_URL = os.getenv("PG_URL", "postgresql://stats:foobar@localhost:5433/stats")

conn = psycopg.Connection.connect(PG_URL)

# DB setup if needed
with open("db_migration.sql", 'r') as file:
  print(f"running migrations file {file}")
  conn.execute(file.read())
  conn.commit()
