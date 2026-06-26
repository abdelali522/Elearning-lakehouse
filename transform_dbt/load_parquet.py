import duckdb

con = duckdb.connect("../datalake/elearning.duckdb")

tables = {
    "studentInfo":         "../datalake/raw/oulad/studentInfo.parquet",
    "studentRegistration": "../datalake/raw/oulad/studentRegistration.parquet",
    "studentAssessment":   "../datalake/raw/oulad/studentAssessment.parquet",
    "studentVle":          "../datalake/raw/oulad/studentVle.parquet",
    "assessments":         "../datalake/raw/oulad/assessments.parquet",
    "vle":                 "../datalake/raw/oulad/vle.parquet",
    "courses":             "../datalake/raw/oulad/courses.parquet",
}

for table_name, path in tables.items():
    con.execute(f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM '{path}'")
    print(f"✅ Loaded: {table_name}")

con.close()

