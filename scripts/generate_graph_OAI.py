import os
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete
from dotenv import load_dotenv

# Load environment variables (for OpenAI API key)
load_dotenv('/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/.env')

# Set up file paths
WORKING_DIR = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/lightrag_data'
MERGED_FILE_PATH = '/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/output1/merged_output.txt'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure working directory exists
if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)

# Initialize LightRAG with the working directory and model function
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete  # Using the gpt_4o_mini_complete model
)

# Read the merged file content
try:
    with open(MERGED_FILE_PATH, 'r') as f:
        merged_content = f.read()
        print("Merged content loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file {MERGED_FILE_PATH} was not found.")
    exit(1)

# Insert the merged content into LightRAG to build the graph
try:
    rag.insert(merged_content)
    print("Content successfully inserted into LightRAG.")
except Exception as e:
    print(f"Error during insertion: {e}")
    exit(1)

# Optionally, you can perform a sample query on the created graph to verify it works
try:
    query_param = QueryParam(mode="global")
    response = rag.query("Which Keystone employees would be best positioned to resolve the github issues found?", param=query_param)
    print("Query response:", response)
except Exception as e:
    print(f"Error during querying: {e}")
