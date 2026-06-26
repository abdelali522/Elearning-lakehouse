import kagglehub
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# --- Config ---
KAGGLE_DATASET = "anlgrbz/student-demographics-online-education-dataoulad"
LAKE_PATH = Path("datalake/raw/oulad")

# All 7 OULAD tables
TABLES = [
    "studentInfo",
    "studentRegistration",
    "studentAssessment",
    "studentVle",       # 10M+ rows - the heavy one
    "assessments",
    "vle",
    "courses",
]

def download_dataset() -> Path:
    """Download OULAD from Kaggle and return the local path."""
    logger.info("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download(KAGGLE_DATASET)
    logger.info(f"Dataset downloaded to: {path}")
    return Path(path)

def csv_to_parquet(csv_path: Path, output_path: Path) -> None:
    """Convert a single CSV file to a compressed Parquet file."""
    logger.info(f"Converting {csv_path.name} → Parquet...")
    
    df = pd.read_csv(csv_path)
    
    logger.info(f"  Rows: {len(df):,} | Columns: {list(df.columns)}")
    
    table = pa.Table.from_pandas(df)
    pq.write_table(
        table,
        output_path,
        compression="snappy",   # fast read/write balance
    )
    
    size_mb = output_path.stat().st_size / (1024 * 1024)
    logger.info(f"  Saved to {output_path} ({size_mb:.2f} MB)")

def run():
    # 1. Create lake directory
    LAKE_PATH.mkdir(parents=True, exist_ok=True)
    
    # 2. Download from Kaggle
    source_path = download_dataset()
    
    # 3. Convert each table
    success, failed = [], []
    for table_name in TABLES:
        csv_file = source_path / f"{table_name}.csv"
        parquet_file = LAKE_PATH / f"{table_name}.parquet"
        
        if not csv_file.exists():
            logger.warning(f"  CSV not found: {csv_file}")
            failed.append(table_name)
            continue
        
        try:
            csv_to_parquet(csv_file, parquet_file)
            success.append(table_name)
        except Exception as e:
            logger.error(f"  Failed on {table_name}: {e}")
            failed.append(table_name)
    
    # 4. Summary
    logger.info(f"\n✅ Success: {success}")
    if failed:
        logger.error(f"❌ Failed:  {failed}")

if __name__ == "__main__":
    run()
