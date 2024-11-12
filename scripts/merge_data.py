import os
from pathlib import Path
import tiktoken

# Define paths
data_folder = Path("/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/data")
output_file = Path("/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/output1/merged_output.txt")

# Initialize content to store merged text
merged_content = ""

# Loop through all .txt files in the data folder
for txt_file in data_folder.glob("*.txt"):
    with open(txt_file, "r", encoding="utf-8") as file:
        merged_content += file.read() + "\n\n"  # Add extra newlines for separation

# Save merged content to the output file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(merged_content)

# Count words, characters, and tokens
word_count = len(merged_content.split())
character_count = len(merged_content)

# Use a general BPE encoding from tiktoken
encoding = tiktoken.get_encoding("cl100k_base")  # General-purpose BPE encoding

# Encode the content and calculate token count
token_count = len(encoding.encode(merged_content))

# Display counts
print(f"Word count: {word_count}")
print(f"Character count: {character_count}")
print(f"Token count: {token_count}")
