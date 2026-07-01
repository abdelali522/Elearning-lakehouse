# E-Learning Lakehouse

A lightweight, local lakehouse pipeline for exploring student behavior and
learning outcomes in the **Open University Learning Analytics Dataset (OULAD)**.
The project downloads the dataset from Kaggle, converts its seven source tables
from CSV to compressed Parquet, exposes them through DuckDB, and uses dbt to
create a clean, tested staging layer for analytics.

The repository is designed as a small, reproducible data-engineering project:
it requires no external database server and keeps the complete pipeline local.

## Architecture

```text
Kaggle (OULAD)
      |
      v
CSV ingestion with Python
      |
      v
Parquet data lake (datalake/raw/oulad)
      |
      v
DuckDB views (datalake/elearning.duckdb)
      |
      v
dbt staging models and data-quality tests
```

## Dataset

OULAD contains anonymized information about courses, students, registrations,
assessments, and interactions with the university's virtual learning
environment.

The pipeline ingests all seven source tables:

| Table | Contents |
| --- | --- |
| `studentInfo` | Student demographics and final outcomes |
| `studentRegistration` | Registration and withdrawal dates |
| `studentAssessment` | Student assessment submissions and scores |
| `studentVle` | Student interactions and click activity |
| `assessments` | Assessment definitions, dates, and weights |
| `vle` | Virtual learning environment activity metadata |
| `courses` | Module presentation details |

Source: [OULAD on Kaggle](https://www.kaggle.com/datasets/anlgrbz/student-demographics-online-education-dataoulad)

## Tech stack

- **Python and pandas** for ingestion
- **KaggleHub** for dataset download
- **Apache Parquet and PyArrow** for efficient columnar storage
- **DuckDB** as the embedded analytical database
- **dbt-duckdb** for SQL transformations and data-quality tests

## Project structure

```text
.
├── dags/
│   └── scripts/
│       ├── ingest_to_lake.py   # Download CSV files and write Parquet
│       └── profile_all.py      # Report row counts for all raw tables
├── transform_dbt/
│   ├── models/staging/         # Cleaned and renamed dbt models
│   ├── dbt_project.yml         # dbt project configuration
│   ├── profiles.yml            # Local DuckDB connection
│   └── load_parquet.py         # Create DuckDB views over Parquet files
├── datalake/                   # Generated locally and excluded from Git
└── requirements.txt
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- Access to the Kaggle dataset
- Kaggle credentials configured for KaggleHub, if prompted

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Ingest the raw data

Run this command from the repository root:

```bash
python dags/scripts/ingest_to_lake.py
```

The script downloads OULAD, converts each CSV file to Snappy-compressed
Parquet, and writes the output to `datalake/raw/oulad/`.

Optionally verify the generated tables and their row counts:

```bash
python dags/scripts/profile_all.py
```

### 3. Register the Parquet files in DuckDB

The loader uses paths relative to the `transform_dbt` directory:

```bash
cd transform_dbt
python load_parquet.py
```

This creates `datalake/elearning.duckdb` and registers the raw Parquet files as
DuckDB views.

### 4. Build and test the dbt models

From the `transform_dbt` directory:

```bash
dbt run --profiles-dir .
dbt test --profiles-dir .
```

You can also run both steps together:

```bash
dbt build --profiles-dir .
```

## Transformation layer

The dbt staging models standardize column names, cast fields to analytical
types, and expose consistent concepts such as `student_id`, `module_code`,
`presentation_code`, and `total_clicks`. Schema tests check important fields
for nulls, accepted values, and uniqueness.

Staging models are materialized as DuckDB views. The dbt configuration also
provides conventions for future intermediate views and analytics marts
materialized as tables.

## Project status

This repository currently implements ingestion and the initial staging layer.
The intermediate and marts layers are prepared in the dbt configuration but
have not yet been added. The `stg_student_assessment` model also requires
completion before student submission and score analysis is available.

Potential next steps include:

- Student engagement and performance marts
- Course and presentation-level KPI models
- Early-warning features for withdrawal or failure risk
- Orchestration and scheduled pipeline runs
- Documentation generation with `dbt docs`

## License and data usage

This project's source code is available under the [MIT License](LICENSE).
The OULAD dataset remains subject to its own terms and citation requirements;
review them before redistributing or publishing derived data.
