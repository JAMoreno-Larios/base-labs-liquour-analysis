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

### Running the pipeline
Once the virtual environment is activated, we can run the pipeline

```
$ [.venv] python run_pipeline.py
```
The resulting report will be found in `reports/report.md`

The pipeline can accept the following command line arguments:
- `--skip-gathering` Skips data downloading
- `--skip-ingest` Skips CSV ingestion into SQLite
- `--skip-analysis` Skips analysis and report generation

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
  - Another script deals with generating the report. Create another Jupyter notebook for easy visualization.

## Stack
- Language: Python 3.14
- Package manager: uv
- Data processing: pandas, NumPy
- Database: SQLite with SQLAlchemy
- Notebooks: Jupyter with jupysqsl for SQL magic
- Reporting: mdutils, tabulate

