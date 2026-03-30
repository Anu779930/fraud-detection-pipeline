"""
ETL Pipeline — Fraud Detection Project
Author: Venkata Sai Anusha Kommasani
Description: Extracts, transforms, and loads financial transaction data
             for fraud detection analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os

# ── Logging Setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# ── EXTRACT ────────────────────────────────────────────────────────────────────
def extract_data(filepath: str) -> pd.DataFrame:
    """Load raw transaction data from CSV."""
    logger.info(f"Extracting data from: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Extracted {len(df):,} records with {df.shape[1]} columns.")
    return df


# ── TRANSFORM ──────────────────────────────────────────────────────────────────
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate transaction records."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logger.info(f"Removed {before - after} duplicate records.")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values in the dataset."""
    missing = df.isnull().sum().sum()
    if missing > 0:
        logger.warning(f"Found {missing} missing values. Filling with column medians.")
        df = df.fillna(df.median(numeric_only=True))
    else:
        logger.info("No missing values found.")
    return df


def normalize_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the transaction Amount column using z-score scaling."""
    df["Amount_Normalized"] = (df["Amount"] - df["Amount"].mean()) / df["Amount"].std()
    logger.info("Transaction amounts normalized.")
    return df


def add_risk_category(df: pd.DataFrame) -> pd.DataFrame:
    """Assign risk categories based on transaction amount."""
    conditions = [
        df["Amount"] > 1000,
        df["Amount"] > 500,
        df["Amount"] > 100,
    ]
    choices = ["High Risk", "Medium Risk", "Low Risk"]
    df["Risk_Category"] = np.select(conditions, choices, default="Minimal Risk")
    logger.info("Risk categories assigned.")
    return df


def add_pipeline_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Add pipeline run metadata for tracking."""
    df["pipeline_run_at"] = datetime.utcnow().isoformat()
    df["pipeline_version"] = "1.0.0"
    logger.info("Pipeline metadata added.")
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run all transformation steps."""
    logger.info("Starting data transformation...")
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = normalize_amount(df)
    df = add_risk_category(df)
    df = add_pipeline_metadata(df)
    logger.info(f"Transformation complete. Final record count: {len(df):,}")
    return df


# ── LOAD ───────────────────────────────────────────────────────────────────────
def load_data(df: pd.DataFrame, output_path: str) -> None:
    """Save transformed data to CSV (simulating load to data warehouse)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Data loaded to: {output_path} ({len(df):,} records)")


# ── DATA QUALITY CHECKS ────────────────────────────────────────────────────────
def run_quality_checks(df: pd.DataFrame) -> bool:
    """Run basic data quality validations."""
    logger.info("Running data quality checks...")
    passed = True

    # Check 1: No nulls in key columns
    key_cols = ["Amount", "Class"]
    for col in key_cols:
        if df[col].isnull().any():
            logger.error(f"Quality Check FAILED: Nulls found in '{col}'")
            passed = False

    # Check 2: Class column only contains 0 or 1
    invalid_classes = df[~df["Class"].isin([0, 1])]
    if not invalid_classes.empty:
        logger.error(f"Quality Check FAILED: Invalid values in 'Class' column")
        passed = False

    # Check 3: Amount must be non-negative
    if (df["Amount"] < 0).any():
        logger.error("Quality Check FAILED: Negative transaction amounts found")
        passed = False

    if passed:
        logger.info("All data quality checks PASSED ✓")
    return passed


# ── PIPELINE RUNNER ────────────────────────────────────────────────────────────
def run_pipeline(input_path: str, output_path: str) -> None:
    """Run the full ETL pipeline."""
    logger.info("=" * 60)
    logger.info("FRAUD DETECTION ETL PIPELINE — STARTING")
    logger.info("=" * 60)

    # Extract
    df = extract_data(input_path)

    # Transform
    df = transform_data(df)

    # Quality Check
    checks_passed = run_quality_checks(df)
    if not checks_passed:
        logger.error("Pipeline halted due to quality check failures.")
        return

    # Load
    load_data(df, output_path)

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY ✓")
    logger.info("=" * 60)


# ── MAIN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    INPUT_PATH = "data/sample_data.csv"
    OUTPUT_PATH = "data/processed_transactions.csv"
    run_pipeline(INPUT_PATH, OUTPUT_PATH)
