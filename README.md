"# backend_durga" 
# PubMed Fetcher

## Overview
PubMed Fetcher is a command-line tool designed to retrieve research paper details from PubMed using keywords. It extracts information such as titles, authors, abstracts, and corresponding author emails, then saves them to a CSV file.

## Project Structure
```
pubmed_fetcher/
│── src/
│   ├── pubmed_fetcher/
│   │   ├── __init__.py
│   │   ├── cli.py          # Command-line interface
│   │   ├── fetcher.py      # Functions to fetch paper details
│   │   ├── utils.py        # Helper functions
│── tests/                  # Unit tests
│── poetry.lock             # Poetry lock file
│── pyproject.toml          # Project dependencies and configuration
│── README.md               # Documentation
```

## Installation
### Prerequisites
- Python 3.13
- Poetry (for dependency management)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/pubmed-fetcher.git
   cd pubmed-fetcher
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage
To fetch research papers and save them as a CSV file, use:
```bash
poetry run get-papers-list "cancer treatment" -f papers.csv
```

## Tools and Libraries Used
- **Python 3.13**: Core programming language ([Download](https://www.python.org/))
- **Poetry**: Dependency management ([Poetry Docs](https://python-poetry.org/docs/))
- **Requests**: For making API calls ([Requests Library](https://docs.python-requests.org/en/latest/))
- **Click**: Command-line interface library ([Click Docs](https://click.palletsprojects.com/))
- **PubMed API**: To fetch paper details ([PubMed API](https://www.ncbi.nlm.nih.gov/home/develop/api/))




