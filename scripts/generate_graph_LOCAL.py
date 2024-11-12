import os
from datetime import datetime
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# Load environment variables (for OpenAI API key, if needed in future)
load_dotenv('/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/.env')

# Set up file paths
BASE_WORKING_DIR = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/lightrag_data'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
WORKING_DIR = os.path.join(BASE_WORKING_DIR, f"graph_{timestamp}")
MERGED_FILE_PATH = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/output1/merged_output.txt'

# Ensure working directory exists
os.makedirs(WORKING_DIR, exist_ok=True)
logging.info(f"Working directory created at: {WORKING_DIR}")

# Initialize LightRAG with the working directory and Ollama model function
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,  # Ollama model for text generation
    llm_model_name="llama3.1:8b-instruct-q8_0",  # Specify the local Ollama model name
    llm_model_max_async=4,  # Maximum number of async requests
    llm_model_max_token_size=60000,  # Maximum context size
    llm_model_kwargs={
        "host": "http://localhost:11434",  # Ollama server host
        "options": {"num_ctx": 60000}  # Context size configuration
    },
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embedding(
            texts,
            embed_model="nomic-embed-text:latest",
            host="http://localhost:11434"  # Specify Ollama embedding host
        )
    )
)

logging.info("LightRAG initialized with Ollama model.")

# Read the merged file content
try:
    with open(MERGED_FILE_PATH, 'r') as f:
        merged_content = f.read()
        logging.info("Merged content loaded successfully.")
except FileNotFoundError:
    logging.error(f"Error: The file {MERGED_FILE_PATH} was not found.")
    exit(1)

# Insert the merged content into LightRAG to build the graph
try:
    rag.insert(merged_content)
    logging.info("Content successfully inserted into LightRAG.")
except Exception as e:
    logging.error(f"Error during insertion: {e}")
    exit(1)

# Optionally, perform a sample query on the created graph to verify it works
try:
    query_param = QueryParam(mode="global")
    response = rag.query(
        "Which Keystone employees would be best positioned to resolve the GitHub issues found?",
        param=query_param
    )
    logging.info("Query response:")
    print(response)
except Exception as e:
    logging.error(f"Error during querying: {e}")