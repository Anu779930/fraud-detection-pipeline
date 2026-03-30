# 🔍 Real-Time Fraud Detection & BI Pipeline

## 📌 Overview
An end-to-end data engineering and machine learning pipeline that detects fraudulent financial transactions. This project covers ETL automation, predictive modeling, cloud storage, and business intelligence reporting — built to simulate a real-world enterprise fraud detection system.

---

## 📊 Key Results
| Metric | Score |
|---|---|
| Model Accuracy | 95.3% |
| ROC-AUC Score | 0.97 |
| Fraud Recall | 91.2% |
| Pipeline Automation | 60% reduction in manual effort |
| Transactions Processed | 284,807 |

---

## 🛠️ Tech Stack
| Category | Tools |
|---|---|
| Languages | Python, SQL |
| Libraries | Pandas, NumPy, Scikit-learn, XGBoost, Imbalanced-learn, Matplotlib, Seaborn |
| Pipeline Orchestration | Apache Airflow |
| Visualization | Power BI |
| Cloud | Microsoft Fabric, Azure |
| Version Control | Git, GitHub |

---

## 📊 Dataset
- **Source:** [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)
- **Size:** 284,807 transactions
- **Features:** 30 anonymized PCA features + Amount + Class label
- **Challenge:** Highly imbalanced — only 0.17% fraud cases (handled with SMOTE)

---

## 🏗️ Pipeline Architecture

```
Raw Data (CSV)
     │
     ▼
ETL Pipeline (Python + Apache Airflow)
     │  ├── Data Extraction
     │  ├── Data Cleaning & Normalization
     │  ├── Data Quality Checks
     │  └── Risk Category Assignment
     ▼
SQL Transformations
     │  ├── Deduplication
     │  ├── KPI Aggregations
     │  └── Fraud Rate Analysis
     ▼
ML Model (XGBoost + SMOTE)
     │  ├── Feature Engineering
     │  ├── SMOTE Oversampling
     │  ├── Hyperparameter Tuning
     │  └── Model Evaluation
     ▼
Microsoft Fabric / Azure (Cloud Storage)
     │
     ▼
Power BI Dashboard (Real-Time Monitoring)
```

---

## 📂 Project Structure

```
fraud-detection-pipeline/
│
├── data/
│   └── sample_data.csv          # Sample transaction dataset
│
├── notebooks/
│   ├── 01_EDA.ipynb             # Exploratory Data Analysis
│   └── 02_model_training.ipynb  # XGBoost model training & evaluation
│
├── pipeline/
│   ├── etl_pipeline.py          # ETL pipeline (Extract, Transform, Load)
│   └── airflow_dag.py           # Apache Airflow DAG orchestration
│
├── models/
│   └── model_notes.md           # Model parameters, results & decisions
│
├── dashboard/
│   └── dashboard_screenshot.png # Power BI dashboard screenshots
│
├── sql/
│   └── transformations.sql      # SQL transformation & analysis queries
│
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🔧 Project Components

### 1️⃣ ETL Pipeline (`pipeline/etl_pipeline.py`)
- Automated data ingestion from CSV sources
- Data cleaning: deduplication, null handling, normalization
- Risk category assignment (High / Medium / Low / Minimal)
- Data quality checks with pass/fail logging
- Modular functions for easy maintenance and testing

### 2️⃣ Airflow DAG (`pipeline/airflow_dag.py`)
- Scheduled daily pipeline execution (`@daily`)
- 6-task DAG: Extract → Transform → Quality Check → Train → Load → Notify
- XCom used for passing metadata between tasks
- Email alerts on failure with 2 automatic retries

### 3️⃣ Machine Learning Model (`notebooks/02_model_training.ipynb`)
- Algorithm: **XGBoost Classifier**
- Class imbalance resolved using **SMOTE** oversampling
- Hyperparameter tuning with GridSearchCV
- Evaluation: Accuracy, ROC-AUC, Precision, Recall, F1-Score
- Feature importance analysis (V14, V17, V12 top predictors)

### 4️⃣ SQL Transformations (`sql/transformations.sql`)
- Data deduplication and normalization
- KPI aggregation queries for dashboard
- Fraud rate by risk category
- Data quality validation queries

### 5️⃣ Power BI Dashboard
- Real-time fraud pattern visualization
- Risk segmentation by transaction type and amount
- KPI cards: total transactions, fraud rate, flagged alerts
- Drill-through filters by time and risk score
- Connected to Microsoft Fabric Lakehouse

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Anu779930/fraud-detection-pipeline.git
cd fraud-detection-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the ETL pipeline**
```bash
python pipeline/etl_pipeline.py
```

**4. Run the notebooks**
```bash
jupyter notebook notebooks/01_EDA.ipynb
jupyter notebook notebooks/02_model_training.ipynb
```

**5. Trigger Airflow DAG**
```bash
airflow dags trigger fraud_detection_pipeline
```

---

## 👩‍💻 Author

**Venkata Sai Anusha Kommasani**
- 📧 vsanushak234@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/anusha-k-915047288)
- 💻 [GitHub](https://github.com/Anu779930)
