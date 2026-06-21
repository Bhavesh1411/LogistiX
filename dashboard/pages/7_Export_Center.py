import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from auth.session_manager import require_auth
from components.sidebar import render_sidebar

# Protect the page
require_auth()

# Render standard sidebar
render_sidebar()

# Inject Custom CSS with 8px grid spacing, CSS variables, and reduced motion settings
st.markdown("""
    <style>
    :root {
        --primary-accent: #2563EB;
        --secondary-accent: #0EA5E9;
        --success: #22C55E;
        --warning: #F59E0B;
        --danger: #EF4444;
        --bg-color: #F8FAFC;
        --card-bg: #FFFFFF;
        --text-color: #0F172A;
    }
    
    /* Global reduced motion */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-delay: 0s !important;
            animation-duration: 0s !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0s !important;
            scroll-behavior: auto !important;
        }
    }
    
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin-top: 32px;
        margin-bottom: 16px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
    }
    
    .export-card {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .export-title {
        color: var(--text-color);
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .export-metadata {
        color: #475569;
        font-size: 0.875rem;
        margin-bottom: 16px;
        line-height: 1.5;
    }
    
    .metadata-item {
        margin-bottom: 4px;
    }
    
    .metadata-label {
        font-weight: 500;
        color: #64748B;
    }
    
    .status-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 12px;
        width: fit-content;
    }
    
    .status-active {
        background-color: #DEF7EC;
        color: #03543F;
    }
    
    .status-inactive {
        background-color: #FDE8E8;
        color: #9B1C1C;
    }
    
    /* Premium button styles to override defaults */
    div.stDownloadButton > button {
        background-color: var(--primary-accent) !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #1D4ED8 !important;
        color: white !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<header>
    <h1 style="color:#0F172A; margin-bottom: 8px;">📤 Export Center</h1>
    <p style="color:#64748B; font-size:1.1rem; margin-top:0; margin-bottom:24px;">
        Centralized reporting hub. Download generated platform outputs, data tables, and consolidated summaries.
    </p>
</header>
""", unsafe_allow_html=True)

# Resolve paths
current_dir = os.path.dirname(os.path.abspath(__file__))
dashboard_dir = os.path.dirname(current_dir)
base_dir = os.path.dirname(dashboard_dir)

seg_path = os.path.join(base_dir, "customer_segmentation", "datasets", "customer_segments_kmeans_finalone.csv")
churn_path = os.path.join(base_dir, "churn_prediction_true", "predictions", "customer_true_churn_predictions.csv")
forecast_path = os.path.join(base_dir, "Demand_Forecasting", "datasets", "weekly_forecast_dashboard_data.json")

inventory_dir = os.path.join(base_dir, "inventory_optimization", "outputs")
inv_master_path = os.path.join(inventory_dir, "inventory_master.csv")
reorder_path = os.path.join(inventory_dir, "reorder_recommendations.csv")
stockout_path = os.path.join(inventory_dir, "stockout_risk_report.csv")
inventory_kpi_path = os.path.join(inventory_dir, "inventory_kpi_summary.csv")

# Helper function to read file metadata
def get_file_info(filepath):
    if not os.path.exists(filepath):
        return {
            "exists": False,
            "filename": os.path.basename(filepath),
            "size": "N/A",
            "last_updated": "N/A",
            "records": "N/A"
        }
    
    filename = os.path.basename(filepath)
    size_bytes = os.path.getsize(filepath)
    if size_bytes < 1024:
        size_str = f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        size_str = f"{size_bytes / 1024:.2f} KB"
    else:
        size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        
    mtime = os.path.getmtime(filepath)
    last_updated = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    records_str = "N/A"
    try:
        if filepath.endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                row_count = sum(1 for line in f) - 1
                records_str = f"{max(0, row_count):,}"
        elif filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    records_str = f"{len(data):,}"
                elif isinstance(data, dict):
                    hist_len = len(data.get('historical', []))
                    fut_len = len(data.get('future', []))
                    if hist_len or fut_len:
                        records_str = f"{hist_len + fut_len:,} (Historical: {hist_len}, Future: {fut_len})"
                    else:
                        records_str = f"{len(data.keys()):,} keys"
        elif filepath.endswith('.md') or filepath.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for line in f)
                records_str = f"{line_count:,} lines"
    except Exception:
        records_str = "Error reading"
        
    return {
        "exists": True,
        "filename": filename,
        "size": size_str,
        "last_updated": last_updated,
        "records": records_str
    }

# Helper to render download cards uniformally
def render_export_card(title, filepath, mime_type, icon="📄", extra_info=None):
    info = get_file_info(filepath)
    status_class = "status-active" if info["exists"] else "status-inactive"
    status_text = "Available" if info["exists"] else "Missing"
    
    extra_html = ""
    if extra_info:
        for k, v in extra_info.items():
            extra_html += f'<div class="metadata-item"><span class="metadata-label">{k}:</span> {v}</div>'
            
    # Build HTML string without blank lines
    html_content = f"""<div class="export-card">
<div>
<div class="export-title">{icon} {title}</div>
<div class="status-badge {status_class}">{status_text}</div>
<div class="export-metadata">
<div class="metadata-item"><span class="metadata-label">File Name:</span> {info['filename']}</div>
<div class="metadata-item"><span class="metadata-label">Record Count:</span> {info['records']}</div>
<div class="metadata-item"><span class="metadata-label">File Size:</span> {info['size']}</div>
<div class="metadata-item"><span class="metadata-label">Last Updated:</span> {info['last_updated']}</div>"""

    if extra_html:
        html_content += f"\n{extra_html}"

    html_content += """
</div>
</div>
</div>"""

    st.markdown(html_content, unsafe_allow_html=True)
    
    if info["exists"]:
        try:
            with open(filepath, "rb") as f:
                file_bytes = f.read()
            st.download_button(
                label=f"Download {title}",
                data=file_bytes,
                file_name=info['filename'],
                mime=mime_type,
                key=f"dl_{info['filename']}"
            )
        except Exception as e:
            st.error(f"Error loading download data: {e}")
    else:
        st.button(f"{title} Unavailable", disabled=True, key=f"disabled_{info['filename']}")

# -----------------
# SECTIONS 1 & 2: CUSTOMER ANALYTICS EXPORTS
# -----------------
st.markdown("<div class='section-header'>Sections 1 & 2: Customer Analytics Exports</div>", unsafe_allow_html=True)
col_c1, col_c2 = st.columns(2)

with col_c1:
    render_export_card(
        title="Customer Segmentation Dataset",
        filepath=seg_path,
        mime_type="text/csv",
        icon="👥"
    )

with col_c2:
    render_export_card(
        title="Churn Prediction Predictions",
        filepath=churn_path,
        mime_type="text/csv",
        icon="🎯"
    )

# -----------------
# SECTION 3: DEMAND FORECASTING EXPORTS
# -----------------
st.markdown("<div class='section-header'>Section 3: Demand Forecasting Exports</div>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns(2)

with col_f1:
    # Load model info from json if exists
    extra_f = None
    if os.path.exists(forecast_path):
        try:
            with open(forecast_path, 'r') as f:
                f_data = json.load(f)
            mi = f_data.get('model_info', {})
            extra_f = {
                "Forecast Model": mi.get('model_name', 'XGBoost'),
                "Validation MAPE": f"{mi.get('val_mape', 0.0):.2f}%",
                "Forecast Horizon": mi.get('horizon', '8 Weeks'),
                "Status": mi.get('status', 'Unknown')
            }
        except Exception:
            pass
            
    render_export_card(
        title="Weekly Forecast Dashboard Data",
        filepath=forecast_path,
        mime_type="application/json",
        icon="📊",
        extra_info=extra_f
    )

with col_f2:
    st.markdown("""<div class="export-card" style="margin-bottom: 12px; padding-bottom: 12px;">
<div class="export-title">📋 Forecasting Reports</div>
<div class="export-metadata">Select and download generated analytical reports and business briefs below.</div>
</div>""", unsafe_allow_html=True)
    
    reports = [
        ("Diagnostic Report", "forecast_diagnostic_report.md"),
        ("Evaluation Report", "forecast_evaluation_report.md"),
        ("Readiness Audit", "forecasting_readiness_audit.md"),
        ("Feasibility Assessment", "weekly_feasibility_assessment.md"),
        ("Business Report", "weekly_forecasting_business_report.md")
    ]
    
    for title, fname in reports:
        r_path = os.path.join(base_dir, "Demand_Forecasting", "reports", fname)
        if os.path.exists(r_path):
            r_info = get_file_info(r_path)
            col_lbl, col_btn = st.columns([2, 1])
            with col_lbl:
                st.markdown(f"**{title}** ({r_info['size']})<br><span style='font-size:0.75rem; color:#64748B;'>Updated: {r_info['last_updated']}</span>", unsafe_allow_html=True)
            with col_btn:
                try:
                    with open(r_path, "rb") as f:
                        r_bytes = f.read()
                    st.download_button(
                        label="Download",
                        data=r_bytes,
                        file_name=fname,
                        mime="text/markdown",
                        key=f"dl_{fname}"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.markdown(f"⚠ **{title}** ({fname}) not found.")

# -----------------
# SECTION 4: INVENTORY OPTIMIZATION EXPORTS
# -----------------
st.markdown("<div class='section-header'>Section 4: Inventory Optimization Exports</div>", unsafe_allow_html=True)
col_i1, col_i2 = st.columns(2)
col_i3, col_i4 = st.columns(2)

with col_i1:
    render_export_card(
        title="Inventory Master",
        filepath=inv_master_path,
        mime_type="text/csv",
        icon="📦"
    )

with col_i2:
    render_export_card(
        title="Reorder Recommendations",
        filepath=reorder_path,
        mime_type="text/csv",
        icon="📈"
    )

with col_i3:
    render_export_card(
        title="Stockout Risk Report",
        filepath=stockout_path,
        mime_type="text/csv",
        icon="⚠️"
    )

with col_i4:
    render_export_card(
        title="Inventory KPI Summary",
        filepath=inventory_kpi_path,
        mime_type="text/csv",
        icon="📉"
    )

# -----------------
# SECTION 5: EXECUTIVE SUMMARY REPORT
# -----------------
st.markdown("<div class='section-header'>Section 5: Executive Summary Report</div>", unsafe_allow_html=True)

# Helper function to compile executive summary report dynamically
def compile_executive_report():
    report_lines = []
    report_lines.append("================================================================================")
    report_lines.append("                     RETAILPULSE EXECUTIVE SUMMARY REPORT")
    report_lines.append(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("================================================================================")
    report_lines.append("")
    
    # 1. Platform Status Summary
    report_lines.append("1. PLATFORM MODULE STATUS")
    report_lines.append("-------------------------")
    
    seg_exists = os.path.exists(seg_path)
    churn_exists = os.path.exists(churn_path)
    forecast_exists = os.path.exists(forecast_path)
    inv_exists = os.path.exists(inventory_kpi_path)
    
    report_lines.append(f"- Customer Segmentation:  {'ACTIVE' if seg_exists else 'INACTIVE'}")
    report_lines.append(f"- Churn Prediction:       {'ACTIVE' if churn_exists else 'INACTIVE'}")
    report_lines.append(f"- Demand Forecasting:     {'ACTIVE' if forecast_exists else 'INACTIVE'}")
    report_lines.append(f"- Inventory Optimization: {'ACTIVE' if inv_exists else 'INACTIVE'}")
    report_lines.append("")
    
    # 2. Demand Forecasting KPIs
    report_lines.append("2. DEMAND FORECASTING OVERVIEW")
    report_lines.append("------------------------------")
    if forecast_exists:
        try:
            with open(forecast_path, 'r') as f:
                f_data = json.load(f)
            mi = f_data.get("model_info", {})
            report_lines.append(f"- Forecast Model:          {mi.get('model_name', 'XGBoost Regressor')}")
            report_lines.append(f"- Granularity:             {mi.get('granularity', 'Weekly')}")
            report_lines.append(f"- Validation MAPE:         {mi.get('val_mape', 0.0):.2f}%")
            report_lines.append(f"- Test MAPE:               {mi.get('test_mape', 0.0):.2f}%")
            report_lines.append(f"- Forecast Horizon:        {mi.get('horizon', '8 Weeks')}")
            report_lines.append(f"- Model Status:            {mi.get('status', 'Unknown')}")
            
            future_list = f_data.get('future', [])
            if future_list:
                f_df = pd.DataFrame(future_list)
                x_idx = np.arange(len(f_df))
                y_val = f_df['forecast'].values
                slope, _ = np.polyfit(x_idx, y_val, 1)
                trend = "Growth" if slope > 1000 else ("Decline" if slope < -1000 else "Stable")
                report_lines.append(f"- 8-Week Revenue Trend:    {trend} (Slope: {slope:+.2f}/week)")
                report_lines.append(f"- Next Week Forecast:      ${f_df['forecast'].iloc[0]:,.2f}")
                report_lines.append(f"- Horizon Peak Forecast:   ${f_df['forecast'].max():,.2f}")
        except Exception as e:
            report_lines.append(f"Error loading forecasting data: {e}")
    else:
        report_lines.append("Demand forecasting data not available.")
    report_lines.append("")
    
    # 3. Customer Segmentation KPIs
    report_lines.append("3. CUSTOMER SEGMENTATION & REVENUE")
    report_lines.append("----------------------------------")
    if seg_exists:
        try:
            seg_df = pd.read_csv(seg_path)
            total_customers = len(seg_df)
            total_rev = seg_df['monetary'].sum() if 'monetary' in seg_df.columns else 0.0
            avg_val = total_rev / total_customers if total_customers > 0 else 0.0
            num_seg = seg_df['cluster'].nunique() if 'cluster' in seg_df.columns else 0
            high_val_count = len(seg_df[seg_df['high_value_customer_flag'] == 1]) if 'high_value_customer_flag' in seg_df.columns else 0
            
            report_lines.append(f"- Total Tracked Customers: {total_customers:,}")
            report_lines.append(f"- Total Platform Revenue:  ${total_rev:,.2f}")
            report_lines.append(f"- Average Customer Value:  ${avg_val:,.2f}")
            report_lines.append(f"- Active Customer Clusters: {num_seg}")
            report_lines.append(f"- High-Value Customers:    {high_val_count:,} ({high_val_count/total_customers * 100:.1f}% of total base)")
        except Exception as e:
            report_lines.append(f"Error loading segmentation data: {e}")
    else:
        report_lines.append("Customer segmentation data not available.")
    report_lines.append("")
    
    # 4. True Churn Predictions
    report_lines.append("4. CUSTOMER CHURN RISK ANALYSIS")
    report_lines.append("-------------------------------")
    if churn_exists:
        try:
            churn_df = pd.read_csv(churn_path)
            total_churn_customers = len(churn_df)
            high_risk_df = churn_df[churn_df['churn_probability'] > 0.70]
            high_risk_count = len(high_risk_df)
            high_risk_pct = (high_risk_count / total_churn_customers) * 100 if total_churn_customers > 0 else 0.0
            rev_at_risk = high_risk_df['monetary'].sum() if 'monetary' in high_risk_df.columns else 0.0
            
            report_lines.append(f"- Evaluated Accounts:      {total_churn_customers:,}")
            report_lines.append(f"- High-Risk Customers:     {high_risk_count:,} ({high_risk_pct:.1f}% of total)")
            report_lines.append(f"- Total Revenue at Risk:   ${rev_at_risk:,.2f}")
            report_lines.append(f"- Churn Platform Status:   {'CRITICAL RISK' if high_risk_pct >= 20.0 else ('ATTENTION REQUIRED' if high_risk_pct >= 10.0 else 'HEALTHY')}")
        except Exception as e:
            report_lines.append(f"Error loading churn data: {e}")
    else:
        report_lines.append("Churn prediction data not available.")
    report_lines.append("")
    
    # 5. Inventory Optimization
    report_lines.append("5. INVENTORY & SUPPLY CHAIN OPTIMIZATION")
    report_lines.append("----------------------------------------")
    if inv_exists:
        try:
            inv_df = pd.read_csv(inventory_kpi_path)
            inv_dict = dict(zip(inv_df['metric'], inv_df['value']))
            
            health_score = float(inv_dict.get('inventory_health_score', 0))
            tot_prod = int(float(inv_dict.get('total_products', 0)))
            crit_risk = int(float(inv_dict.get('risk_category_counts.Critical', 0)))
            sim_val = float(inv_dict.get('total_simulated_inventory_value_usd', 0))
            ex_val = float(inv_dict.get('excess_stock_value_usd', 0))
            
            reorder_count = 0
            if os.path.exists(reorder_path):
                reorder_df = pd.read_csv(reorder_path)
                reorder_count = len(reorder_df)
                
            report_lines.append(f"- Inventory Health Score:  {health_score:.2f} / 100")
            report_lines.append(f"- Total Products Tracked:  {tot_prod:,}")
            report_lines.append(f"- Critical Risk Products:  {crit_risk:,} ({crit_risk/tot_prod * 100:.1f}% of catalog)")
            report_lines.append(f"- Reorder Recommendations: {reorder_count:,}")
            report_lines.append(f"- Simulated Stock Value:   ${sim_val:,.2f}")
            report_lines.append(f"- Excess Inventory Value:  ${ex_val:,.2f}")
        except Exception as e:
            report_lines.append(f"Error loading inventory data: {e}")
    else:
        report_lines.append("Inventory optimization data not available.")
    report_lines.append("")
    
    # 6. Priority Alerts Count
    report_lines.append("6. SYSTEM ALERTS SUMMARY")
    report_lines.append("------------------------")
    try:
        c_df = pd.read_csv(churn_path) if churn_exists else pd.DataFrame()
        r_df = pd.read_csv(reorder_path) if os.path.exists(reorder_path) else pd.DataFrame()
        
        with open(forecast_path, 'r') as f:
            d_data = json.load(f) if forecast_exists else {}
            
        t_high_risk = len(c_df[c_df['churn_probability'] > 0.70]) if not c_df.empty else 0
        c_prod = len(r_df[r_df['risk_category'] == 'Critical']) if not r_df.empty else 0
        imm_reorder = len(r_df[r_df['reorder_urgency'] >= 0.80]) if not r_df.empty else 0
        
        d_surges = []
        d_drops = []
        h_peaks = []
        if d_data and 'future' in d_data:
            fut_df = pd.DataFrame(d_data['future'])
            if not fut_df.empty:
                for i, row in fut_df.iterrows():
                    if i == 0:
                        wow = row['growth_from_last_historical']
                    else:
                        wow = (row['forecast'] - fut_df.iloc[i-1]['forecast']) / fut_df.iloc[i-1]['forecast'] * 100
                    if wow > 15:
                        d_surges.append(row)
                    elif wow < -15:
                        d_drops.append(row)
                    if '12-19' in row['date'] or '12-20' in row['date'] or '12-21' in row['date'] or '12-22' in row['date']:
                        h_peaks.append(row)
                        
        crit_alerts = (1 if t_high_risk > 100 else 0) + (1 if c_prod > 50 else 0) + len(d_drops)
        opp_alerts = len(d_surges) + len(h_peaks)
        warn_alerts = (1 if 0 < t_high_risk <= 100 else 0) + (1 if 0 < c_prod <= 50 else 0) + (1 if imm_reorder > 0 else 0)
        tot_alerts = crit_alerts + warn_alerts + opp_alerts
        
        report_lines.append(f"- Active Alerts Count:     {tot_alerts}")
        report_lines.append(f"  • Critical Alerts:       {crit_alerts}")
        report_lines.append(f"  • Warning Alerts:        {warn_alerts}")
        report_lines.append(f"  • Opportunity Alerts:    {opp_alerts}")
        report_lines.append(f"  • Immediate Reorders Req: {imm_reorder}")
    except Exception as e:
        report_lines.append(f"Error calculating alerts: {e}")
        
    report_lines.append("")
    report_lines.append("================================================================================")
    report_lines.append("                        END OF RETAILPULSE EXECUTIVE REPORT")
    report_lines.append("================================================================================")
    
    return "\n".join(report_lines)

# Compile report
report_text = compile_executive_report()

# Executive Summary layout
st.markdown("""<div class="export-card">
<div class="export-title">📋 RetailPulse Executive Summary</div>
<div class="export-metadata">
View the live consolidated business report below. This report brings together key performance indicators across all modules.
</div>
</div>""", unsafe_allow_html=True)

# Preview the text inside Streamlit in a code-block
st.code(report_text, language="text")

# Export as TXT file
st.download_button(
    label="Download Executive Summary (TXT)",
    data=report_text,
    file_name="retailpulse_executive_summary.txt",
    mime="text/plain",
    key="dl_executive_summary"
)
