import chromadb
import os
import sys
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from utils import extract_keywords

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load environment variables
load_dotenv(".env")

# Load ChromaDB configurations
CHROMADB_PATH = os.getenv("CHROMADB_PATH")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# ChromaDB Setup (Persistent Mode)
chroma_client = chromadb.PersistentClient(path=CHROMADB_PATH)

def retrieve_relevant_data(query_name, top_k=3):
    try:
        collection = chroma_client.get_collection(name=DATABASE_NAME)

        # Filter metadata manually (without embeddings)
        all_data = collection.get()
        exact_results = [
            doc for doc in all_data["metadatas"] if isinstance(query_name, str) and query_name in doc.get("name", "")
        ]

        return exact_results
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return []

def query_db(query):
    try:
        keywords = extract_keywords(query)
        result_list = []
        for keyword in keywords:
            query_name = keyword
            results = retrieve_relevant_data(query_name)
            result_list.extend(results)
        return result_list
    except Exception as e:
        print(f"Error querying database: {e}")
        return []



