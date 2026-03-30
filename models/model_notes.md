# 🤖 Model Notes — Fraud Detection

## Model: XGBoost Classifier

### Final Hyperparameters
| Parameter | Value |
|---|---|
| n_estimators | 100 |
| max_depth | 6 |
| learning_rate | 0.1 |
| subsample | 0.8 |
| colsample_bytree | 0.8 |
| eval_metric | logloss |
| random_state | 42 |

---

### Performance Results
| Metric | Score |
|---|---|
| Accuracy | 95.3% |
| ROC-AUC | 0.97 |
| Fraud Recall | 91.2% |
| Fraud Precision | 88.4% |
| F1-Score (Fraud) | 89.7% |

---

### Class Imbalance Handling
- Method: **SMOTE** (Synthetic Minority Oversampling Technique)
- Before SMOTE: ~0.17% fraud cases
- After SMOTE: Balanced 50/50 split for training
- SMOTE applied **only on training data** (never on test data)

---

### Models Compared
| Model | Accuracy | ROC-AUC |
|---|---|---|
| Logistic Regression | 91.2% | 0.91 |
| Random Forest | 93.8% | 0.95 |
| **XGBoost (Final)** | **95.3%** | **0.97** |

XGBoost selected as final model due to best overall performance.

---

### Top Fraud Predictors (Feature Importance)
1. V14
2. V17
3. V12
4. V10
5. V11

---

### Key Decisions
- Dropped `Time` column — not predictive after analysis
- Normalized `Amount` using z-score scaling
- Train/Test split: 80/20 with stratification
- No data leakage — SMOTE applied after split
