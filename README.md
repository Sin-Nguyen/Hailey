# Hailey - AI analysis of test automation

## Overview
This repository contains tools and models for analyzing and reporting on test automation logs. It includes utilities for extracting keywords from queries, querying a ChromaDB database, and providing insights into test case failures.

## Directory Structure
```
Hailey
├── modelfile
│   └── report
│       └── Modelfile
├── src
│   ├── report
│   │   └── finding.py
│   └── utils.py
└── tutorials
    └── QueryWithChromaDB.md
```

## Files

### Modelfile
- **/modelfile/report/Modelfile**: Defines the models and system information for analyzing test case failures and providing job reports.

### Source Code
- **/src/utils.py**: Contains utility functions for extracting keywords from user queries and determining the intent of the queries.
- **/src/report/finding.py**: Contains functions for querying the ChromaDB database and retrieving relevant data based on user queries.

### Tutorials
- **/tutorials/QueryWithChromaDB.md**: A tutorial on how to write AI queries using ChromaDB.

## Installation

1. Clone the repository:
    ```bash
    https://github.com/Sin-Nguyen/Hailey.git
    cd Hailey
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    Create a `.env` file in the root directory and add the following:
    ```env
    CHROMADB_PATH=your_chromadb_path
    ```

## Usage

### Extracting Keywords
Use the `extract_keywords` function to extract keywords from a user query:
```python
from utils import extract_keywords

question = "Can you show me the latest failed test results for miniapp?"
keywords = extract_keywords(question)
print("Extracted Keywords:", keywords)
```

### Querying the Database
Use the `query_db` function to query the ChromaDB database:
```python
from report.finding import query_db

query = "Show me the latest failed test results for miniapp"
results = query_db(query)
print("Query Results:", results)
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
