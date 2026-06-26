import duckdb

con = duckdb.connect()

# Check all 7 tables loaded
tables = [
    "studentInfo", "studentRegistration", "studentAssessment",
    "studentVle", "assessments", "vle", "courses"
]

for t in tables:
    result = con.execute(
        f"SELECT COUNT(*) as rows FROM 'datalake/raw/oulad/{t}.parquet'"
    ).fetchone()
    print(f"{t:<25} → {result[0]:>10,} rows")
    