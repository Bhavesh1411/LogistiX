import streamlit as st
import pandas as pd
import json
import os
from auth.session_manager import require_auth
from components.sidebar import render_sidebar

# Protect the page
require_auth()

# Render standard sidebar
render_sidebar()

st.title("Executive Overview")
st.markdown("Top-level KPIs and business metrics.")

# Get base path (RetailPulse root)
current_dir = os.path.dirname(os.path.abspath(__file__)) 
dashboard_dir = os.path.dirname(current_dir)
base_dir = os.path.dirname(dashboard_dir)

@st.cache_data
def load_executive_data():
    data = {}
    
    # 1. Demand Forecasting
    forecast_path = os.path.join(base_dir, "Demand_Forecasting", "datasets", "weekly_forecast_dashboard_data.json")
    if os.path.exists(forecast_path):
        with open(forecast_path, 'r') as f:
            forecast_data = json.load(f)
            data['forecast_accuracy'] = forecast_data.get('model_info', {}).get('val_mape', 0)
            data['forecast_status'] = forecast_data.get('model_info', {}).get('status', 'Unknown')
            data['forecast_model'] = forecast_data.get('model_info', {}).get('model_name', 'Unknown')
            data['forecast_active'] = True
    else:
        data['forecast_accuracy'] = 0
        data['forecast_status'] = 'Not Found'
        data['forecast_model'] = 'Unknown'
        data['forecast_active'] = False

    # 2. Customer Segmentation & Revenue
    segmentation_path = os.path.join(base_dir, "customer_segmentation", "datasets", "customer_segments_kmeans_finalone.csv")
    if os.path.exists(segmentation_path):
        seg_df = pd.read_csv(segmentation_path)
        data['total_customers'] = len(seg_df)
        data['total_revenue'] = seg_df['monetary'].sum() if 'monetary' in seg_df.columns else 0
        data['avg_customer_value'] = data['total_revenue'] / data['total_customers'] if data['total_customers'] > 0 else 0
        data['num_segments'] = seg_df['cluster'].nunique() if 'cluster' in seg_df.columns else 0
        data['high_value_customers'] = len(seg_df[seg_df['high_value_customer_flag'] == 1]) if 'high_value_customer_flag' in seg_df.columns else 0
        data['segmentation_active'] = True
    else:
        data['total_customers'] = 0
        data['total_revenue'] = 0
        data['avg_customer_value'] = 0
        data['num_segments'] = 0
        data['high_value_customers'] = 0
        data['segmentation_active'] = False

    # 3. True Churn Prediction
    churn_path = os.path.join(base_dir, "churn_prediction_true", "predictions", "customer_true_churn_predictions.csv")
    if os.path.exists(churn_path):
        churn_df = pd.read_csv(churn_path)
        if 'risk_category' in churn_df.columns:
            data['high_risk_customers'] = len(churn_df[churn_df['risk_category'] == 'High Risk'])
            data['high_risk_percentage'] = (data['high_risk_customers'] / len(churn_df)) * 100 if len(churn_df) > 0 else 0
        else:
            data['high_risk_customers'] = 0
            data['high_risk_percentage'] = 0
        data['churn_active'] = True
    else:
        data['high_risk_customers'] = 0
        data['high_risk_percentage'] = 0
        data['churn_active'] = False

    # 4. Inventory Optimization
    inventory_path = os.path.join(base_dir, "inventory_optimization", "outputs", "inventory_kpi_summary.csv")
    if os.path.exists(inventory_path):
        inv_df = pd.read_csv(inventory_path)
        inv_dict = dict(zip(inv_df['metric'], inv_df['value']))
        data['inventory_health_score'] = float(inv_dict.get('inventory_health_score', 0))
        data['total_products'] = int(float(inv_dict.get('total_products', 0)))
        data['critical_risk_products'] = int(float(inv_dict.get('risk_category_counts.Critical', 0)))
        data['inventory_active'] = True
    else:
        data['inventory_health_score'] = 0
        data['total_products'] = 0
        data['critical_risk_products'] = 0
        data['inventory_active'] = False
        
    reorder_path = os.path.join(base_dir, "inventory_optimization", "outputs", "reorder_recommendations.csv")
    if os.path.exists(reorder_path):
        reorder_df = pd.read_csv(reorder_path)
        data['reorder_recommendations'] = len(reorder_df)
    else:
        data['reorder_recommendations'] = 0

    return data

data = load_executive_data()

# Helper for status colors
def get_health_status(score):
    if score >= 80: return "Healthy", "#28a745"
    if score >= 50: return "Attention Required", "#ffc107"
    return "Critical", "#dc3545"

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">${data['total_revenue']:,.2f}</div>
            <div style="font-size: 0.8rem; color: #6c757d; margin-top: 5px;">Avg Customer Value: ${data['avg_customer_value']:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    acc = max(0, 100 - data['forecast_accuracy']) if data['forecast_accuracy'] else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Forecast Accuracy</div>
            <div class="metric-value">{acc:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Customers</div>
            <div class="metric-value">{data['total_customers']:,}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">High Risk Customers</div>
            <div class="metric-value">{data['high_risk_customers']:,}</div>
            <div style="font-size: 0.8rem; color: #dc3545; margin-top: 5px; font-weight: bold;">{data['high_risk_percentage']:.1f}% of total</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Products</div>
            <div class="metric-value">{data['total_products']:,}</div>
        </div>
    """, unsafe_allow_html=True)
    
    inv_status, inv_color = get_health_status(data['inventory_health_score'])
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Inventory Health Score</div>
            <div class="metric-value">{data['inventory_health_score']:.2f} <span style="font-size: 1rem; color: #6c757d; font-weight: normal;">/ 100</span></div>
            <div style="font-size: 0.8rem; color: {inv_color}; margin-top: 5px; font-weight: bold;">Status: {inv_status}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("Executive Business Summary")

sum_col1, sum_col2 = st.columns(2)

with sum_col1:
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e9ecef; margin-bottom: 20px;">
        <h4 style="color: #0056b3; margin-top: 0; font-size: 1.1rem;">Demand Forecasting</h4>
        <ul style="list-style-type: none; padding-left: 0; font-size: 0.95rem; color: #495057;">
            <li style="margin-bottom: 8px;">✅ <b>Weekly Forecasting Active</b></li>
            <li style="margin-bottom: 8px;">✅ <b>Forecast Model:</b> {data['forecast_model']}</li>
            <li style="margin-bottom: 8px;">✅ <b>Validation MAPE:</b> {data['forecast_accuracy']:.2f}%</li>
            <li style="margin-bottom: 8px;">✅ <b>Forecast Status:</b> <span style="color: #28a745; font-weight: bold;">{data['forecast_status']}</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    churn_status = "Critical" if data['high_risk_percentage'] >= 20 else ("Attention Required" if data['high_risk_percentage'] >= 10 else "Healthy")
    churn_status_color = "#dc3545" if churn_status == "Critical" else ("#ffc107" if churn_status == "Attention Required" else "#28a745")

    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e9ecef; margin-bottom: 20px;">
        <h4 style="color: #0056b3; margin-top: 0; font-size: 1.1rem;">Customer Analytics</h4>
        <ul style="list-style-type: none; padding-left: 0; font-size: 0.95rem; color: #495057;">
            <li style="margin-bottom: 8px;">✅ <b>Customer Segmentation Completed</b> ({data['num_segments']} Segments)</li>
            <li style="margin-bottom: 8px;">✅ <b>High Value Customers:</b> {data['high_value_customers']:,}</li>
            <li style="margin-bottom: 8px;">✅ <b>True Churn Model Active</b></li>
            <li style="margin-bottom: 8px;">✅ <b>Overall Churn Status:</b> <span style="color: {churn_status_color}; font-weight: bold;">{churn_status}</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with sum_col2:
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e9ecef; margin-bottom: 20px;">
        <h4 style="color: #0056b3; margin-top: 0; font-size: 1.1rem;">Inventory Optimization</h4>
        <ul style="list-style-type: none; padding-left: 0; font-size: 0.95rem; color: #495057;">
            <li style="margin-bottom: 8px;">✅ <b>Inventory Health Score:</b> <span style="color: {inv_color}; font-weight: bold;">{data['inventory_health_score']:.2f}</span></li>
            <li style="margin-bottom: 8px;">✅ <b>Critical Risk Product Count:</b> {data['critical_risk_products']:,}</li>
            <li style="margin-bottom: 8px;">✅ <b>Reorder Recommendations Count:</b> {data['reorder_recommendations']:,}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    status_color = "#28a745" if all([data['segmentation_active'], data['forecast_active'], data['churn_active'], data['inventory_active']]) else "#ffc107"
    sys_status_text = "Operational" if status_color == "#28a745" else "Partially Operational"
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid {status_color}; border-top: 1px solid #e9ecef; border-right: 1px solid #e9ecef; border-bottom: 1px solid #e9ecef;">
        <h4 style="color: #0056b3; margin-top: 0; font-size: 1.1rem;">Overall Platform Status</h4>
        <ul style="list-style-type: none; padding-left: 0; font-size: 0.95rem; color: #495057;">
            <li style="margin-bottom: 8px;">• Segmentation: <b style="color: {'#28a745' if data['segmentation_active'] else '#dc3545'};">{'Active' if data['segmentation_active'] else 'Inactive'}</b></li>
            <li style="margin-bottom: 8px;">• Forecasting: <b style="color: {'#28a745' if data['forecast_active'] else '#dc3545'};">{'Active' if data['forecast_active'] else 'Inactive'}</b></li>
            <li style="margin-bottom: 8px;">• Churn: <b style="color: {'#28a745' if data['churn_active'] else '#dc3545'};">{'Active' if data['churn_active'] else 'Inactive'}</b></li>
            <li style="margin-bottom: 8px;">• Inventory: <b style="color: {'#28a745' if data['inventory_active'] else '#dc3545'};">{'Active' if data['inventory_active'] else 'Inactive'}</b></li>
        </ul>
        <div style="margin-top: 15px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; text-align: center;">
            <b>System Status:</b> <span style="color: {status_color};">RetailPulse Analytics Platform {sys_status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
