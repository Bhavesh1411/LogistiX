# Churn Model Target Leakage Audit Report

This report evaluates the feature set engineered for the point-in-time Predictive Churn Model to ensure zero target leakage.

## Leakage Audit Summary

- **Total Features Audited:** 13
- **Leakage Status:** PASS - ZERO LEAKAGE DETECTED
- **High Risk Features (|r| > 0.90):** 0
- **Critical Risk Features (|r| > 0.95):** 0




---

## Detailed Feature Correlation Analysis

The table below lists all engineered features, their correlation with the target variable `true_churn_flag`, and their leakage risk assessment.

| Feature Name | Pearson Correlation ($r$) | Leakage Risk Level | Assessment |
| :--- | :--- | :--- | :--- |
| `customer_loyalty_score` | -0.359432 | Safe | Standard behavioral correlation. |
| `active_months` | -0.353712 | Safe | Standard behavioral correlation. |
| `customer_rank_by_revenue` | 0.325138 | Safe | Standard behavioral correlation. |
| `frequency` | -0.237446 | Safe | Standard behavioral correlation. |
| `recency` | 0.224497 | Safe | Standard behavioral correlation. |
| `high_value_customer_flag` | -0.211739 | Safe | Standard behavioral correlation. |
| `avg_days_between_purchases` | 0.191904 | Safe | Standard behavioral correlation. |
| `customer_tenure` | -0.188050 | Safe | Standard behavioral correlation. |
| `purchase_frequency` | -0.155143 | Safe | Standard behavioral correlation. |
| `monetary` | -0.122726 | Safe | Standard behavioral correlation. |
| `average_purchase_value` | -0.053999 | Safe | Standard behavioral correlation. |
| `weekend_sales_ratio` | -0.016056 | Safe | Standard behavioral correlation. |
| `quantity_per_order` | -0.007382 | Safe | Standard behavioral correlation. |

---

## Point-in-Time Boundary Integrity Check

- **Cutoff Date (T):** `2010-09-10`
- **Data Filtering Verification:**
  - All transactions used for feature aggregations are strictly filtered to dates $\le$ `2010-09-10`.
  - The target variable `true_churn_flag` is constructed strictly using transaction activity starting from `2010-09-11` onwards.
- **Reference Date:** `2010-09-11` was used as the anchor point for computing `recency` and `customer_tenure`, which prevents future date information from entering the calculations.




## Conclusion

[SUCCESS] All features passed the leakage audit. The point-in-time boundary is intact, and no features show signs of target leakage. The dataset is ready for model training.
