import psycopg2
import pandas as pd
import datetime
import os
import sys
from dotenv import load_dotenv
# Load environment variables
load_dotenv(".env")

# Load ChromaDB configurations
RP_DATABASE_NAME = os.getenv("RP_DATABASE_NAME")
RP_DATABASE_USER = os.getenv("RP_DATABASE_USER")
RP_DATABASE_PASSWORD = os.getenv("RP_DATABASE_PASSWORD")
RP_DATABASE_HOST = os.getenv("RP_DATABASE_HOST")
RP_DATABASE_PORT = os.getenv("RP_DATABASE_PORT")


# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=RP_DATABASE_USER,
    password=RP_DATABASE_PASSWORD,
    host=RP_DATABASE_HOST,
    port=RP_DATABASE_PORT
)

# Query
query = "SELECT * FROM launch WHERE start_time >= DATE_TRUNC('day', NOW() - INTERVAL '1 day') + INTERVAL '11 hours';"
df = pd.read_sql(query, conn)

# Close connection
conn.close()

# Preprocess
df["duration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()

# Convert to JSONL format
df[["name", "status","number", "duration", "start_time"]].to_json("data.jsonl", orient="records", lines=True)

print("Data saved to data.jsonl")