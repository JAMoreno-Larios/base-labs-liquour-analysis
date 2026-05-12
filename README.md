# Code Challenge for Data Engineer position at Base Labs

### By José Agustín Moreno Larios


## Problem Statement

You are helping Annie, the owner of a large liquor and spirit distributor in the US. She wants to understand her profits and margins. She provided you this link where you can download relevant CSV data:https://www.pwc.com/us/en/careers/university-relations/data-and-analytics-case-studies-files.html 

Task at hand

1. Efficiently ingest the relevant csv files into a suitable database.
2. Transform the data to calculate profits ($) and margins (%).
3. Create a report for Annie outlining:
  1. Top 10 products with highest based on profit ($) and margin (%).
  2. Top 10 brands with highest based on profit ($) and margin (%).
  3. Which brands / products should she drop as a wholesales because they are loosing money.

## Installation and execution

To install into a virtual environment,
```
$ uv sync
```

Activate the virtual environment

```
$ source .venv/bin/activate
```

### Setting the Anthropic API key

Create a `.env` file in the root directory, see `.env.example` for
the template:

```
# Set your Anthropic API key
ANTHROPIC_API_KEY=YOUR_CLAUDE_API_KLEY

# Set Langsmith API key for tracing with Langchain
LANGSMITH_API_KEY=YOUR_LANGSMITH_API_KEY
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=base-labs-liquour-analysis
```

Substitute the API key placeholders with your own. If you're not
interested in using Langsmith tracing, you can remove those lines from
your `.env` file.

### Running the pipeline
Once the virtual environment is activated, we can run the pipeline

```
$ [.venv] python run_pipeline.py
```
The resulting report will be found in `reports/report_llm.md`

The pipeline can accept the following command line arguments:
- `--skip-gathering` Skips data downloading
- `--skip-ingest` Skips CSV ingestion into SQLite
- `--skip-analysis` Skips analysis and report generation
- `--no-llm-analysis` Generates report using `src/report.py` instead of `src/report_claude.py`. Report will be saved as `reports/report.md`

### Jupyter Notebooks

There are a couple of notebooks found in `notebooks`. To run them,
execute

```
$[.venv] jupyter notebook
```
and navigate to the `notebooks` directory. There you will find both
SQL and analysis notebooks.


## Project structure
- Ingest data from CSV to a SQL database
- Perform data analysis with Python
  - Use Jupyter notebooks to explore the ingested data.
  - Create methods that can extract and process the information we obtained
  from the database.
  - Another script deals with generating the report with LLM support.

## Possible follow-up work

- Implement a SQL agent that can perform queries to the database
- Enable caching for common queries and responses

## Stack
- Language: Python 3.14
- Package manager: uv
- LLM support: langchain, langchain-anthropic
- Data processing: pandas, NumPy
- Database: SQLite with SQLAlchemy
- Notebooks: Jupyter with jupysqsl for SQL magic
- Reporting: mdutils, tabulate
- Secrets: dotenv

