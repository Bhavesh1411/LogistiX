# Model Training and Evaluation Report

This report evaluates the performance of Logistic Regression, Random Forest, XGBoost, and LightGBM models trained on the point-in-time true churn dataset.

## Executive Summary

- **Best-Performing Model:** `LightGBM`
- **Test ROC AUC:** `71.7690%`
- **Test Recall:** `62.3100%`
- **Test F1-Score:** `61.1028%`
- **Test Accuracy:** `65.0134%`

---

## 1. Cross-Validation Performance (Training Set)

We performed Stratified 5-Fold Cross-Validation on the training set (80% of the active customer cohort) using class weighting to balance the loss function.

| Model | CV Accuracy | CV Precision | CV Recall | CV F1-Score | CV ROC AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 65.2685% | 58.1933% | 75.7414% | 65.8077% | 71.5103% |
| Random Forest | 65.1007% | 61.4288% | 56.0456% | 58.5802% | 70.7264% |
| XGBoost | 64.2282% | 59.2029% | 60.7605% | 59.9400% | 69.4128% |
| LightGBM | 64.5973% | 58.9797% | 64.8669% | 61.7789% | 70.4064% |

---

## 2. Test Set Performance (Evaluation Set)

Below are the evaluation metrics calculated on the holdout test set (20% of the active customer cohort).

| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 62.8686% | 56.0465% | 73.2523% | 63.5046% | 71.0452% |
| Random Forest | 62.8686% | 58.6093% | 53.7994% | 56.1014% | 69.9066% |
| XGBoost | 62.3324% | 57.1856% | 58.0547% | 57.6169% | 68.8031% |
| LightGBM | 65.0134% | 59.9415% | 62.3100% | 61.1028% | 71.7690% |

---

## 3. Confusion Matrices

Below are the confusion matrices for each of the trained models on the test set (746 total customers).

### Confusion Matrix Legend
- **True Negative (TN):** Active customer correctly classified as Active.
- **False Positive (FP):** Active customer incorrectly flagged as Churned.
- **False Negative (FN):** Churned customer incorrectly flagged as Active.
- **True Positive (TP):** Churned customer correctly classified as Churned.

#### Logistic Regression
- **TN:** 228 | **FP:** 189
- **FN:** 88 | **TP:** 241
- *Total Predictions:* 746 | *True Active:* 417 | *True Churned:* 329
- *Recall (Sensitivity):* 73.25% | *Specificity:* 54.68%
- *Precision:* 56.05%

#### Random Forest
- **TN:** 292 | **FP:** 125
- **FN:** 152 | **TP:** 177
- *Total Predictions:* 746 | *True Active:* 417 | *True Churned:* 329
- *Recall (Sensitivity):* 53.80% | *Specificity:* 70.02%
- *Precision:* 58.61%

#### XGBoost
- **TN:** 274 | **FP:** 143
- **FN:** 138 | **TP:** 191
- *Total Predictions:* 746 | *True Active:* 417 | *True Churned:* 329
- *Recall (Sensitivity):* 58.05% | *Specificity:* 65.71%
- *Precision:* 57.19%

#### LightGBM
- **TN:** 280 | **FP:** 137
- **FN:** 124 | **TP:** 205
- *Total Predictions:* 746 | *True Active:* 417 | *True Churned:* 329
- *Recall (Sensitivity):* 62.31% | *Specificity:* 67.15%
- *Precision:* 59.94%


---

## Conclusion & Best Model Selection

The model **LightGBM** was selected as the champion model because it achieved the highest ROC AUC of **71.77%** on the test set, while maintaining a strong balance between Recall (**62.31%**) and Precision (**59.94%**). 

The class weights worked successfully to pull up model sensitivity, ensuring that the model detects a high proportion of churners without producing an overwhelming number of false alarms.
