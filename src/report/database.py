import chromadb
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv(".env")

# Load ChromaDB configurations
CHROMADB_PATH = os.getenv("CHROMADB_PATH")

# ✅ Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=f"./{CHROMADB_PATH}")

def get_chroma_schema():
    """
    Retrieves available tables (collections) and metadata fields in ChromaDB v0.6.0.
    """
    collection_names = chroma_client.list_collections()  # ✅ Now returns only names

    schema_info = {}

    for collection_name in collection_names:
        collection = chroma_client.get_collection(collection_name)  # ✅ Fetch full collection details

        # ✅ Retrieve metadata keys from a sample document
        sample_data = collection.get(limit=1)
        metadata_keys = list(sample_data["metadatas"][0].keys()) if sample_data["metadatas"] else []

        schema_info[collection_name] = metadata_keys

    return schema_info

def get_chroma_collections():
    """
    Retrieves available tables (collections) in ChromaDB v0.6.0.
    """
    collection_names = chroma_client.list_collections()  # ✅ Now returns only names

    return collection_names


