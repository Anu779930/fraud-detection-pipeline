"""
Apache Airflow DAG — Fraud Detection Pipeline
Author: Venkata Sai Anusha Kommasani
Description: Orchestrates the fraud detection ETL pipeline using Airflow.
             Runs daily to process new transaction data.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import logging

logger = logging.getLogger(__name__)

# ── Default Arguments ──────────────────────────────────────────────────────────
default_args = {
    "owner": "anusha_kommasani",
    "depends_on_past": False,
    "email": ["vsanushak234@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2026, 1, 1),
}


# ── Task Functions ─────────────────────────────────────────────────────────────
def extract_task(**kwargs):
    """Extract raw transaction data."""
    logger.info("Task 1: Extracting transaction data...")
    import pandas as pd
    df = pd.read_csv("data/sample_data.csv")
    logger.info(f"Extracted {len(df):,} records.")
    # Push record count to XCom for downstream tasks
    kwargs["ti"].xcom_push(key="record_count", value=len(df))


def transform_task(**kwargs):
    """Transform and clean transaction data."""
    logger.info("Task 2: Transforming data...")
    from pipeline.etl_pipeline import extract_data, transform_data
    df = extract_data("data/sample_data.csv")
    df = transform_data(df)
    df.to_csv("data/transformed_transactions.csv", index=False)
    logger.info("Transformation complete.")


def quality_check_task(**kwargs):
    """Run data quality checks."""
    logger.info("Task 3: Running quality checks...")
    import pandas as pd
    from pipeline.etl_pipeline import run_quality_checks
    df = pd.read_csv("data/transformed_transactions.csv")
    passed = run_quality_checks(df)
    if not passed:
        raise ValueError("Data quality checks failed — pipeline halted.")
    logger.info("Quality checks passed.")


def train_model_task(**kwargs):
    """Train the XGBoost fraud detection model."""
    logger.info("Task 4: Training fraud detection model...")
    import pandas as pd
    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report

    df = pd.read_csv("data/transformed_transactions.csv")
    feature_cols = [c for c in df.columns if c.startswith("V")] + ["Amount_Normalized"]
    X = df[feature_cols]
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    logger.info(f"\n{classification_report(y_test, y_pred)}")
    logger.info("Model training complete.")


def load_to_fabric_task(**kwargs):
    """Simulate loading processed data to Microsoft Fabric / Azure."""
    logger.info("Task 5: Loading data to Microsoft Fabric...")
    import pandas as pd
    df = pd.read_csv("data/transformed_transactions.csv")
    # In production: use azure-storage-blob or fabric SDK to upload
    df.to_csv("data/processed_transactions.csv", index=False)
    logger.info(f"Loaded {len(df):,} records to data lake.")


def notify_completion_task(**kwargs):
    """Send pipeline completion notification."""
    record_count = kwargs["ti"].xcom_pull(key="record_count", task_ids="extract")
    logger.info(f"Pipeline completed successfully. Processed {record_count:,} records.")


# ── DAG Definition ─────────────────────────────────────────────────────────────
with DAG(
    dag_id="fraud_detection_pipeline",
    default_args=default_args,
    description="Daily fraud detection ETL and model scoring pipeline",
    schedule_interval="@daily",
    catchup=False,
    tags=["fraud", "etl", "ml", "finance"],
) as dag:

    # Task 1: Extract
    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
        provide_context=True,
    )

    # Task 2: Transform
    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
        provide_context=True,
    )

    # Task 3: Quality Check
    quality_check = PythonOperator(
        task_id="quality_check",
        python_callable=quality_check_task,
        provide_context=True,
    )

    # Task 4: Train Model
    train_model = PythonOperator(
        task_id="train_model",
        python_callable=train_model_task,
        provide_context=True,
    )

    # Task 5: Load to Fabric
    load_to_fabric = PythonOperator(
        task_id="load_to_fabric",
        python_callable=load_to_fabric_task,
        provide_context=True,
    )

    # Task 6: Notify
    notify = PythonOperator(
        task_id="notify_completion",
        python_callable=notify_completion_task,
        provide_context=True,
    )

    # ── Pipeline Flow ──────────────────────────────────────────────────────────
    # extract → transform → quality_check → train_model → load_to_fabric → notify
    extract >> transform >> quality_check >> train_model >> load_to_fabric >> notify
