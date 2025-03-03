import os
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc
from dotenv import load_dotenv
import logging
import streamlit as st

# Set up logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# Load environment variables (for OpenAI API key, if needed in future)
load_dotenv('/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/.env')

# Set up file paths
BASE_WORKING_DIR = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/lightrag_data'
EXISTING_GRAPH_DIR = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/lightrag_data/graph_20241112_135927'

# Ensure the existing graph directory exists
if not os.path.exists(EXISTING_GRAPH_DIR):
    logging.error(f"Error: The existing graph directory {EXISTING_GRAPH_DIR} does not exist.")
    st.error(f"Error: The existing graph directory {EXISTING_GRAPH_DIR} does not exist.")
    st.stop()

logging.info(f"Using existing working directory at: {EXISTING_GRAPH_DIR}")

# Initialize LightRAG with the existing working directory and Ollama model function
rag = LightRAG(
    working_dir=EXISTING_GRAPH_DIR,
    llm_model_func=ollama_model_complete,  # Ollama model for text generation
    llm_model_name="llama3.2:3b-instruct-fp16",  # Specify the local Ollama model name
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

# Streamlit app
st.title("LightRAG Query App")
st.markdown("Enter a query to get answers from your knowledge base.")

# Input for the user's query
user_query = st.text_input("Your Query:", "Who is the cofounder and chairman of the board for Keystone AI?")

# Select box for search mode
search_mode = st.selectbox(
    "Search Mode:",
    options=["global", "local"],
    index=0  # Default to global
)

# Button to submit the query
if st.button("Submit"):
    try:
        query_param = QueryParam(mode=search_mode)
        response = rag.query(user_query, param=query_param)
        logging.info(f"Query: {user_query}")
        logging.info(f"Search Mode: {search_mode}")
        logging.info(f"Response: {response}")
        st.success("Query Response:")
        st.write(response)
    except Exception as e:
        logging.error(f"Error during querying: {e}")
        st.error(f"An error occurred: {e}")