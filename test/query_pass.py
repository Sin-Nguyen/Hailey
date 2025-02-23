import chromadb
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load environment variables
load_dotenv(".env")

# Load ChromaDB configurations
CHROMADB_PATH = os.getenv("CHROMADB_PATH")


# ChromaDB Setup (Persistent Mode)
chroma_client = chromadb.PersistentClient(path=CHROMADB_PATH)

def query_test_collection(query_name, top_k=3):
    collection = chroma_client.get_collection(name="reportportal")

    # Filter metadata manually (without embeddings)
    all_data = collection.get()
    exact_results = [
        doc for doc in all_data["metadatas"] if query_name in doc.get("name", "")
    ]

    return exact_results
# Example usage
query = "wechatminiapp"
retrieved_data = query_test_collection(query)
print("🔍 Retrieved Data:", retrieved_data)
