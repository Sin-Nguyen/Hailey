import subprocess
import threading
import time
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
import logging
import argparse
from report.finding import query_db  # Your ChromaDB query function
from constraints import query_prompt

# ✅ Enable Debug Logging
logging.basicConfig(level=logging.INFO)

# ✅ Function to format retrieved ChromaDB results
def format_retrieved_data(retrieved_docs):
    if not retrieved_docs:
        return "No relevant information found in the database."

    formatted_context = "\n".join([
        f"- Name: {doc.get('name', 'Unknown')}, Status: {doc.get('status', 'Unknown')}, "
        f"Number: {doc.get('number', 'Unknown')}, Duration: {doc.get('duration', 'Unknown')}, "
        f"Start Time: {doc.get('start_time', 'Unknown')}"
        for doc in retrieved_docs
    ])
    
    return f"Here is the relevant data from previous test runs:\n{formatted_context}"

# ✅ LangChain Prompt for Debugging Hailey’s Query
prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template=query_prompt("context", "query")
)

# ✅ Hailey's Query Function with LangChain Integration
def query_hailey_with_context(query):
    logging.debug(f"🔍 Query Received: {query}\n")

    # 🔍 Retrieve relevant test data from ChromaDB
    retrieved_docs = query_db(query)
    logging.debug(f"🔍 Retrieved Data: {retrieved_docs}\n")

    # 📝 Format retrieved data for Hailey
    formatted_context = format_retrieved_data(retrieved_docs)
    logging.debug(f"📄 Formatted Context:\n{formatted_context}\n")

    # 🔥 Generate Final Query for Hailey
    final_prompt = prompt_template.format(context=formatted_context, query=query)

    # 🛠️ Debug the prompt before sending to Hailey
    logging.debug(f"📩 Final Hailey's Prompt:\n{final_prompt}\n")
    
    logging.debug(f"🚀 Running Hailey with LangChain for debugging...\n")

    # 🚀 Run Hailey via Ollama with LangChain for debugging
    result = subprocess.run(["ollama", "run", "hailey"], input=final_prompt, text=True, capture_output=True)

    # 📝 Log the response
    hailey_response = result.stdout.strip()
    logging.debug(f"🤖 Hailey's Answer:\r {hailey_response}")

    return hailey_response

def loading_animation():
    print("\n")
    while not stop_loading:
        for char in "|/-\\":
            print(f"\rHailey thinking.... {char}", end="")
            time.sleep(0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Hailey's query with context")
    parser.add_argument("message", type=str, help="The message to query Hailey with context")
    args = parser.parse_args()

    stop_loading = False
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    try:
        response = query_hailey_with_context(args.message)
    finally:
        stop_loading = True
        loading_thread.join()

    print("\n🤖 Hailey's Answer\r" + response)