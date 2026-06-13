# RetailPulse forecasting diagnosis and root-cause analysis report

## Phase 1: Model Diagnostic Report

### 1. LightGBM Model Metrics
*   **Train MAPE**: 23.40% | MAE: 5,867.25 | RMSE: 8,403.15 | $R^2$: 0.6692
*   **Validation MAPE**: 23.37% | MAE: 10,671.73 | RMSE: 16,760.87 | $R^2$: 0.4168
*   **Test MAPE**: 25.09% | MAE: 13,961.28 | RMSE: 20,123.28 | $R^2$: 0.3006

### 2. Fit and Generalization Analysis
*   **Underfitting**: The model shows moderate underfitting. A Train $R^2$ of 0.67 on daily transactional data indicates that the 19 safe features are missing critical drivers (such as holiday events, stock-outs, or promotions) that explain the daily variance of B2B sales.
*   **Overfitting**: The model does *not* suffer from significant overfitting. The gap between Train MAPE (23.40%) and Validation MAPE (23.37%) is negligible. 
*   **Generalization**: The generalization is compromised on the test set. Although the test MAPE is close to validation (25.09% vs 23.37%), the test $R^2$ drops to 0.3006 and MAE/RMSE rise sharply. This is due to a seasonal volume shift in the November-December test period that the model was unable to scale.

---

## Phase 2: Feature Importance Analysis

### Top 10 Most Important Features (Split)
1.  `weekday_seasonality_index` (66): Captures strong weekly patterns (B2B sales drop to near-zero on weekends).
2.  `lag_1_qty` (34): Yesterday's quantity sold represents short-term momentum.
3.  `week_of_year` (29): Captures seasonal drift across weeks.
4.  `lag_7_qty` (22): Same-day-last-week volume capture.
5.  `rolling_30_day_sales_lag1` (21): Captures medium-term demand baselines.
6.  `sales_volatility_30_day_lag1` (21): Captures variance and noise.
7.  `lag_1_sales` (20): Direct revenue lag.
8.  `lag_7_sales` (19): Same-day-last-week revenue.
9.  `quantity_momentum_lag1` (18): Ratio of 7-day to 30-day quantity.
10. `rolling_7_day_sales_lag1` (16): Short-term demand trend.

### Bottom 10 Least Important Features
10. `rolling_7_day_quantity_lag1` (12)
11. `demand_momentum_lag1` (8)
12. `lag_30_qty` (6)
13. `rolling_30_day_quantity_lag1` (6)
14. `month` (4)
15. `lag_30_sales` (1)
16. `quarter` (0)
17. `day_of_week` (0)
18. `sales_growth_rate` (0)

### Interpretation
The model depends heavily on **short-term lags (1 and 7 days)** and **weekday seasonality**. It completely ignores macro-temporal features (`quarter`, `day_of_week`, `sales_growth_rate`) because `weekday_seasonality_index` already resolves the day-of-week information, and the dataset is too short for quarterly features to build statistical power.

---

## Phase 3: SHAP Analysis

### SHAP Global Feature Importance (Test Set)
1.  `weekday_seasonality_index`: 5,930.41 (Strongest driver of daily volume adjustment).
2.  `week_of_year`: 5,496.37 (Determines base sales level drift).
3.  `lag_1_qty`: 2,134.29 (Direct short-term volume scaling).
4.  `lag_1_sales`: 1,440.80 (Direct short-term revenue scaling).
5.  `rolling_7_day_quantity_lag1`: 1,358.10 (Weekly volume trend).
6.  `sales_volatility_30_day_lag1`: 895.44 (Variance/uncertainty scaler).

### Feature Impact Direction (Correlation with SHAP Value)
*   `weekday_seasonality_index` (**Positive, Corr = 0.95**): High index values (Monday-Wednesday) strongly push predictions upward. Low values (weekends) drag predictions to zero.
*   `lag_1_qty` (**Positive, Corr = 0.83**): High quantity sold yesterday strongly scales up predictions for today.
*   `lag_1_sales` (**Positive, Corr = 0.77**): High sales yesterday push predictions up.
*   `week_of_year` (**Positive, Corr = 0.07**): A weak positive trend indicating that later weeks in the year have a slightly higher base prediction.

---

## Phase 4: Residual Analysis

*   **Residual Mean**: +$13,269.94 (Significant positive residual indicating severe underprediction bias).
*   **Residual Std Dev**: $15,127.95
*   **Overpredictions (Pred > Actual)**: 4 days
*   **Underpredictions (Pred < Actual)**: 26 days

### Largest Forecasting Misses
*   **2010-11-15**: Actual $104,708.97 | Predicted $39,719.93 | Error +$64,989.04
*   **2010-11-10**: Actual $79,469.50 | Predicted $38,552.39 | Error +$40,917.11
*   **2010-11-29**: Actual $78,889.67 | Predicted $39,719.93 | Error +$39,169.74

### Systematic Errors & Bias Check
There is a **systematic underprediction bias** in the test period. The model underpredicted on **87% of the test days** (26 out of 30). The model flatlines predictions at a maximum cap of ~$40k, completely missing the large peaks ($70k - $105k) in November.

---

## Phase 5: Actual vs Predicted Analysis
*(Refer to plots saved in the artifacts directory: `actual_vs_predicted.png` and `residuals_over_time.png`)*

### Failure Points & Volatility
*   **November-December Surge**: The model fails during the high-volatility holiday sales period. Because the training set spans Dec 2009 - Oct 2010, the model has **never seen the month of November** in the training set. It lacks the seasonal memory to know that November contains major peak sales weeks (due to B2B restocking ahead of the Christmas shutdown).
*   **Peak Day Flatlining**: The model predictions never exceed $40,000, while actual sales on peak weekdays regularly spike above $70,000.

---

## Phase 6: Root Cause Analysis
Ranked from highest to lowest impact on accuracy:

1.  **Distribution Shift & Short History (Highest Impact)**: The training dataset (284 days) is too short. It does not contain a full year of seasonal history (specifically, no November data). The model cannot learn November holiday spikes without seeing them in the training set.
2.  **Information Loss from Leakage Remediation**: Restricting the model to purely lagged variables prevents it from utilizing the target's concurrent information. While mathematically necessary to prevent leakage, it reveals how much the model depended on concurrent monthly indices to scale up predictions.
3.  **Absence of Exogenous Drivers (Promotions/Holidays)**: Daily retail sales are heavily driven by marketing campaigns, promotions, and warehouse stocking events. Without these features, tree models regress to the mean.
4.  **Granularity Level**: Daily forecasting is highly volatile. Noise dominates the signal on a daily level.

---

## Phase 7: Optuna Feasibility Assessment

### Expected MAPE Ranges
*   **Current Baseline**: **25.09%**
*   **Expected after Optuna Tuning**: **23.0% - 24.5%** (Tuning tree parameters like `max_depth` and `learning_rate` cannot generate new seasonal peaks or fix missing data).
*   **Expected after Feature & Aggregation Improvements**: **10.0% - 13.0%** (Adding Thanksgiving/Christmas indicators, combining lag indicators, or aggregating predictions to a weekly level to smooth out daily B2B transaction noise).

---

## Final Summary & Recommendations

### 1. Top Reasons for Poor Forecasting Accuracy
1.  **Missing seasonal history**: The training set lacks the prior year's November data, causing the model to completely miss the Nov holiday peak.
2.  **No exogenous promotion/holiday flags**: The model cannot differentiate between a normal Tuesday and a pre-holiday Tuesday.
3.  **High daily volatility**: Noise dominates the daily sales target.

### 2. Is Optuna Recommended?
**NO** (at this stage). Running Optuna on the current feature set will only result in overfitting to the training/validation sets and will not resolve the systematic underprediction during seasonal peaks. Optuna should only be run *after* resolving the feature and data issues.

### 3. Estimated Achievable MAPE
*   **Daily Level**: **14.0% - 16.0%** (with safe holiday flags and lag interaction features).
*   **Weekly Level**: **6.0% - 9.0%** (by predicting weekly aggregated demand and using a weekday splitter).

### 4. Recommended Next Action
> [!IMPORTANT]
> **Action**: Aggregate the target and predictions to a **Weekly Level** (Weekly Sales Forecast) OR construct explicit **Holiday/Promo Distance Features** (e.g. days until Thanksgiving/Christmas) to help the model scale its predictions upwards during peak periods. Using a weekly level is the industry standard for retail inventory planning.
