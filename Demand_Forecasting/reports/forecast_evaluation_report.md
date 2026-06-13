# Day 5 Forecast Model Development: Technical & Business Report

## Phase 1 & 2: Target and Split
*   **Target Variable**: `sales_amount`
*   **Time Series Split**: Strict chronological split to prevent data leakage.
    *   **Training Period**: 2009-12-01 to 2010-10-10 (284 days)
    *   **Validation Period**: 2010-10-11 to 2010-11-09 (30 days)
    *   **Testing Period**: 2010-11-10 to 2010-12-09 (30 days)

## Phase 3, 4, & 5: Model Training, Evaluation, and Comparison
Both XGBoost and LightGBM regressors were trained utilizing only the approved, strictly historical, leakage-free features. Early stopping was employed on the Validation set.

### XGBoost vs LightGBM Results (Sales Amount)

| Metric | XGBoost | LightGBM |
| :--- | :--- | :--- |
| **Train MAPE** | ~23.3% | 23.40% |
| **Validation MAPE** | ~24.5% | 23.37% |
| **Test MAPE** | ~26.2% | **25.09%** |
| **Test MAE** | ~$14,200 | $13,961.28 |
| **Test R²** | ~0.28 | 0.3006 |

### Model Comparison
*   **Accuracy**: LightGBM outperformed XGBoost on the strictly chronological holdout Test set, achieving a lower MAPE (25.09%) and higher R² (0.3006).
*   **Stability**: LightGBM showed better stability across the Train, Validation, and Test sets, exhibiting less overfitting compared to the traditional XGBoost tree structure.
*   **Generalization**: LightGBM generalized better to unseen future periods when utilizing the recursive multi-step forecasting technique.

**Winner: LightGBM**

## Phase 6: 30-Day Forecast
Using the winning LightGBM model, a recursive 30-day demand forecast was generated for the period immediately following the dataset (2010-12-10 to 2011-01-08).

### Forecast Sample (First 5 Days)
*   **2010-12-10**: $33,346.45
*   **2010-12-11**: $2,184.10 (Weekend Drop-off)
*   **2010-12-12**: $25,873.78
*   **2010-12-13**: $40,342.23 (Weekday Surge)
*   **2010-12-14**: $39,935.72

**Total 30-Day Demand Forecast: $824,934.75**

### Trend Interpretation & Business Implications
1.  **Weekend vs. Weekday Seasonality**: The forecast accurately captures sharp drop-offs on specific weekend days (e.g., $2.1k on 2010-12-11) and subsequent surges on early weekdays (e.g., $40.3k on 2010-12-13). This indicates strong reliance on `weekday_seasonality_index` and `day_of_week`.
2.  **Holiday Season Tapering**: The overall 30-day projection of ~$825k reflects post-peak holiday sales tapering off into January, factoring in negative `sales_growth_rate` constraints.
3.  **Inventory Optimization**: Procurement teams should closely follow the micro-trends (high volume on Mondays/Tuesdays) rather than stocking evenly across the week.
4.  **Actionable Insight**: With the removal of leakage features, the forecast is entirely realistic but highly volatile, reflecting the true underlying difficulty of daily granular B2B/Retail sales prediction without future knowledge.

## Phase 7: Requirement Check

> [!WARNING]
> The target MAPE requirement of $\le 12\%$ was not achieved with the strictly safe feature set. The removal of the highly predictive (but mathematically invalid) leakage features exposed the true baseline predictability of the dataset.

1. **Best Model**: LightGBM
2. **Final MAPE**: 25.09%
3. **Requirement Achieved**: NO
4. **Demand Forecasting Approved**: NO
