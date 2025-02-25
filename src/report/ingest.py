import chromadb
import pandas as pd
import os
import glob
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import json
import datetime

# Load environment variables
load_dotenv(".env")

# Load ChromaDB configurations
CHROMADB_PATH = os.getenv("CHROMADB_PATH")

# ChromaDB Setup (Persistent Mode)
client = chromadb.PersistentClient(path=CHROMADB_PATH)
collection_name = "Hailey"
collection = client.get_or_create_collection(name=collection_name)

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Read and insert JSONL data into ChromaDB with dynamic table name
import json
import datetime

# Function to handle None values
def clean_value(value, default="Unknown"):
    return value if value is not None else default

# Function to convert timestamps (if needed)
def convert_timestamp(timestamp):
    if isinstance(timestamp, (int, float)) and timestamp > 0:
        # ✅ If timestamp is too small, assume it's in SECONDS and convert to MILLISECONDS
        if timestamp < 100000:  
            timestamp = timestamp * 1000  # Convert seconds to milliseconds
        
        timestamp_sec = timestamp / 1000  # Convert to seconds
        return datetime.datetime.utcfromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S')
    
    return "Unknown Time"

# Read and insert JSONL data into ChromaDB with dynamic table name
with open("data.jsonl", "r") as f:
    for i, line in enumerate(f):
        data = json.loads(line)

        # Extract and clean data
        name = clean_value(data.get("name"), "Unknown Name")
        status = clean_value(data.get("status"), "Unknown Status")
        testcases = clean_value(data.get("testcases"), 0)  # Use 0 for testcases
        duration = clean_value(data.get("duration"), 0)
        start_time = convert_timestamp(clean_value(data.get("start_time"), 0))  # Convert timestamp

        # Generate embedding based on "name" (or another field)
        embedding = embedding_model.encode(name).tolist()

        # Insert into ChromaDB with all metadata
        collection.add(
            ids=[str(i)],  # Unique ID
            embeddings=[embedding],  # Store embeddings
            metadatas=[{
                "name": name,
                "status": status,
                "testcases": testcases,
                "duration": duration,
                "start_time": start_time  # Include new key
            }]
        )
        print(f"✅ Added {name} at {start_time} to ChromaDB")
        

print(f"✅ Successfully stored JSONL data in ChromaDB under collection '{collection_name}'!")