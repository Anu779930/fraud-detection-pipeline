# 🔍 Real-Time Fraud Detection & BI Pipeline

## 📌 Overview
An end-to-end data engineering and machine learning pipeline 
that detects fraudulent financial transactions. Covers ETL 
automation, predictive modeling, cloud storage, and business 
intelligence reporting.

---

## 🛠️ Tech Stack
| Category | Tools |
|---|---|
| Languages | Python, SQL |
| Libraries | Pandas, NumPy, Scikit-learn, XGBoost, Imbalanced-learn, Matplotlib, Seaborn |
| Pipeline | Apache Airflow |
| Visualization | Power BI |
| Cloud | Microsoft Fabric, Azure |
| Version Control | Git, GitHub |

---

## 📊 Dataset
- **Source:** Kaggle — Credit Card Fraud Detection
- **Size:** 284,807 transactions
- **Features:** 30 anonymized features + amount + fraud label
- **Challenge:** 0.17% fraud cases — handled with SMOTE

---

## 🏗️ Architecture
```
Raw Data → ETL Pipeline (Airflow) → Data Cleaning (Python/SQL)
→ Feature Engineering → XGBoost Model → Predictions
→ Microsoft Fabric/Azure → Power BI Dashboard
```

---

## 📂 Project Components

### 1️⃣ ETL Pipeline
- Automated ingestion using Apache Airflow DAGs
- Data cleaning and normalization using Python (Pandas)
- SQL-based transformation and validation

### 2️⃣ Machine Learning Model
- Algorithm: XGBoost Classifier
- Class imbalance handled using SMOTE
- Hyperparameter tuning with GridSearchCV
- **Accuracy: 95%+**
- Metrics: Precision, Recall, F1-Score, ROC-AUC

### 3️⃣ Power BI Dashboard
- Real-time fraud pattern visualization
- Risk segmentation by transaction type
- KPI cards: fraud rate, flagged alerts, total transactions
- Drill-through filters by time and risk score

### 4️⃣ Cloud Deployment
- Processed data stored in Microsoft Fabric Lakehouse
- Azure used for pipeline hosting

---

## 📈 Results
| Metric | Score |
|---|---|
| Model Accuracy | 95.3% |
| Fraud Recall | 91.2% |
| ROC-AUC Score | 0.97 |
| Pipeline Automation | 60% reduction in manual effort |

---

## 🚀 How to Run
1. Clone the repo
```
   git clone https://github.com/Anu779930/fraud-detection-pipeline
```
2. Install dependencies
```
   pip install -r requirements.txt
```
3. Run ETL pipeline
```
   python pipeline/etl_pipeline.py
```
4. Trigger Airflow DAG
```
   airflow dags trigger fraud_detection_dag
```

---

## 👩‍💻 Author
**Venkata Sai Anusha Kommasani**
- 📧 vsanushak234@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/anusha-k-915047288)
- 💻 [GitHub](https://github.com/Anu779930)
```

---
