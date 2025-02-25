import psycopg2
import pandas as pd
import datetime
import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timezone

def convert_datetime_to_utc(dt):
    timestamp_s = dt / 1000

    # Convert to UTC datetime
    utc_datetime = datetime.fromtimestamp(dt, tz=timezone.utc)

    # Format to the required pattern
    formatted_time = utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return formatted_time

# Load environment variables
load_dotenv(".env")

# Load ChromaDB configurations
DATABASE_NAME = os.getenv("RP_DATABASE_NAME")
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
query = "SELECT * FROM public.launch WHERE LOWER(name) <> 'codeceptjs tests' ORDER BY id DESC;"
df = pd.read_sql(query, conn)

# Close connection
conn.close()

# Preprocess
df["duration"] = (df["end_time"] - df["start_time"]).dt.total_seconds()
df["start_time"] = df["start_time"].apply(lambda x: convert_datetime_to_utc(x.timestamp()))
df["test_cases"] = df["number"]


# Convert to JSONL format
df[["name", "status","test_cases", "duration", "start_time"]].to_json("data.jsonl", orient="records", lines=True)

print("Data saved to data.jsonl")