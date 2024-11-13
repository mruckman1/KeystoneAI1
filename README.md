# README for Repository `mruckman1/KeystoneAI1`

## Overview

This repository, `mruckman1/KeystoneAI1`, contains a collection of scripts and data aimed at processing GitHub repositories, merging data from multiple sources, and generating knowledge graphs to facilitate analysis and decision-making. The primary focus is on integrating data from the open-source project [openai/swarm](https://github.com/openai/swarm) along with employee profiles from [Keystone AI](https://www.keystone.ai/our-people).

## Repository Structure

```
├── data/
│   ├── openai_swarm_2024-11-12_19-01-10.txt
│   └── our_people.txt
└── scripts/
    ├── app.py
    ├── fetch_github_data.py
    ├── generate_graph_LOCAL.py
    ├── generate_graph_OAI.py
    ├── merge_data.py
    └── scrape_website.py
```

## Data Files

### `data/openai_swarm_2024-11-12_19-01-10.txt`

This file contains the structured content of the [openai/swarm](https://github.com/openai/swarm) repository, including:

- Repository structure.
- Recent issues (past 3 months).
  
The data is formatted in markdown for readability.

### `data/our_people.txt`

This CSV file holds detailed profiles of Keystone AI employees, including:

- **Name**
- **Position**
- **Biography**
- **Education**

## Scripts

### `scripts/app.py`
*Currently lacks specific functionality; reserved for future use.*

### `scripts/fetch_github_data.py`

**Purpose:** Fetches the contents and recent issues from a specified GitHub repository.

**Usage:**

```bash
python fetch_github_data.py
```

**Functionality:**
- Authenticates with GitHub using a token.
- Processes repository structure, excluding certain files/patterns (e.g., tests, documentation).
- Retrieves recent issues within the last 3 months and includes additional context such as labels, assignees, milestones, comments, etc.
- Saves the structured data to a `.txt` file in the specified output directory.

### `scripts/generate_graph_LOCAL.py`

**Purpose:** Creates a knowledge graph using local language models with the help of [LightRAG](https://github.com/mruckman1/lightrag).

**Usage:**

```bash
python generate_graph_LOCAL.py
```

**Functionality:**
- Loads merged content from `output1/merged_output.txt`.
- Initializes LightRAG with a local Ollama model (`llama3.1:8b-instruct-q8_0`).
- Inserts the merged content into the graph.
- Optionally queries the graph to find suitable Keystone employees for resolving GitHub issues.

### `scripts/generate_graph_OAI.py`

**Purpose:** Similar to `generate_graph_LOCAL.py`, but uses OpenAI models instead of local models.

**Usage:**

```bash
python generate_graph_OAI.py
```

**Functionality:**
- Loads merged content from `output1/merged_output.txt`.
- Initializes LightRAG with the GPT-4 mini model.
- Inserts the merged content into the graph.
- Optionally queries the graph to find suitable Keystone employees for resolving GitHub issues.

### `scripts/merge_data.py`

**Purpose:** Merges multiple `.txt` files from a specified directory into a single file, counting words, characters, and tokens.

**Usage:**

```bash
python merge_data.py
```

**Functionality:**
- Reads all `.txt` files in the `data/` folder.
- Concatenates their contents into `output1/merged_output.txt`.
- Counts and prints word count, character count, and token count using a BPE encoding.

### `scripts/scrape_website.py`

**Purpose:** Scrapes employee profiles from the [Keystone AI "Our People" page](https://www.keystone.ai/our-people).

**Usage:**

```bash
python scrape_website.py
```

**Functionality:**
- Requests and parses the main page to find individual profile links.
- Scapes each profile for details such as name, position, biography, and education.
- Saves the extracted data in CSV format to `data/our_people.txt`.

## Environment Setup

Ensure you have the necessary environment variables set up in a `.env` file located at `/Users/mruckman1/Desktop/ImagesGraphAgentsExperiment/.env`. The required variables are:

- **GITHUB_TOKEN**: GitHub personal access token for authentication.
- **OPENAI_API_KEY**: OpenAI API key (required by `generate_graph_OAI.py`).

## Dependencies

The scripts require the following Python packages:

- `PyGithub`
- `dotenv`
- `requests`
- `beautifulsoup4`
- `lightrag`
- `tiktoken`

You can install them using pip:

```bash
pip install PyGithub python-dotenv requests beautifulsoup4 lightrag tiktoken
```

## Usage

1. **Fetch GitHub Data:**
   ```bash
   python scripts/fetch_github_data.py
   ```

2. **Scrape Keystone AI Employee Profiles:**
   ```bash
   python scripts/scrape_website.py
   ```

3. **Merge Data Files:**
   ```bash
   python scripts/merge_data.py
   ```

4. **Generate Knowledge Graph Using Local Model:**
   ```bash
   python scripts/generate_graph_LOCAL.py
   ```

5. **Generate Knowledge Graph Using OpenAI Model:**
   ```bash
   python scripts/generate_graph_OAI.py
   ```

## Contributing

Contributions are welcome! Please open an issue or pull request to suggest improvements, add new features, or fix bugs.

## License

This repository is licensed under the [MIT License](LICENSE).

---

Feel free to modify and extend these scripts to suit your specific needs. Happy coding!