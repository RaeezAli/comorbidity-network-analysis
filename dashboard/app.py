import streamlit as st
import pandas as pd
import sys
import os

# Path handling
sys.path.append(os.path.join(os.getcwd(), 'dashboard', 'components'))

try:
    from dashboard.components.data import load_data
    from dashboard.components.metrics import display_kpi_metrics
    from dashboard.components.visualizations import (
        plot_prevalence, 
        plot_diabetes_distribution, 
        plot_network_graph, 
        plot_cluster_distribution, 
        plot_cluster_profiles
    )
except ImportError:
    from components.data import load_data
    from components.metrics import display_kpi_metrics
    from components.visualizations import (
        plot_prevalence, 
        plot_diabetes_distribution, 
        plot_network_graph, 
        plot_cluster_distribution, 
        plot_cluster_profiles
    )

# Page Config
st.set_page_config(
    page_title="Comorbidity Network Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CLEAN MINIMAL THEME =====
st.markdown("""
<style>
    /* ===== FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; box-sizing: border-box; }

    /* ===== THEME COLORS & BASE ===== */
    :root {
        --bg: #f8fafc;
        --card: #ffffff;
        --muted: #6b7280;
        --text: #0f172a;
        --accent: #2563eb;
        --accent-strong: #3b82f6;
    }

    .stApp { background-color: var(--bg); color: var(--text); font-size: 16px; line-height: 1.5; }
    p, span, label { color: #334155; font-size: 0.95rem; }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4 {
        color: var(--text) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        line-height: 1.12 !important;
    }

    /* Page specific header / subheader sizes */
    .page-header { font-size: 2.25rem !important; margin-bottom: 0.5rem !important; color: var(--text) !important; font-weight: 800 !important; }
    .page-subheader { font-size: 0.95rem !important; color: var(--muted) !important; margin-bottom: 1.5rem !important; font-weight: 500 !important; }

    h1 { font-size: 1.875rem !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.125rem !important; }

    /* Images & plot alignment: keep images responsive and centered in columns */
    .stImage, .element-container img, .stPlotlyChart, .stChart, figure img, canvas {
        max-width: 100%;
        height: auto !important;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Better layout for columns containing images/plots */
    [data-testid="column"] > div {
        display: flex !important;
        flex-direction: column !important;
        gap: 1rem !important;
        align-items: center !important;
    }

    /* ===== CARDS ===== */
    .card { background-color: var(--card); padding: 1.5rem; border-radius: 12px; border: 1px solid #e6edf3; margin-bottom: 1.25rem; box-shadow: 0 1px 4px rgba(12,20,30,0.04); }
    .card-title { font-size: 0.9rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.75rem; }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] { background-color: var(--card); border-right: 1px solid #e6edf3; padding-top: 1rem; }
    section[data-testid="stSidebar"] > div { padding: 1rem; }

    .sidebar-brand { padding: 0.75rem 1rem; margin-bottom: 1.25rem; border-bottom: 1px solid #f1f5f9; }
    .sidebar-brand-title { font-size: 1rem; font-weight: 700; color: var(--text); margin: 0; }
    .sidebar-brand-subtitle { font-size: 0.8rem; color: #6b7280; margin: 0; }

    .nav-label { font-size: 0.75rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.12em; padding: 0 1rem; margin-bottom: 0.6rem; }

    /* ===== NAV ITEMS: equal gap & alignment ===== */
    .nav-item-active, section[data-testid="stSidebar"] .stButton button {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.65rem 0.95rem;
        margin: 0.6rem 0;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.97rem;
        text-align: left;
        width: 100%;
    }

    .nav-item-active {
        background-color: #eef2ff;
        color: var(--accent);
        border-left: 3px solid var(--accent-strong);
    }

    section[data-testid="stSidebar"] .stButton button {
        background-color: transparent !important;
        color: #475569 !important;
        border: none !important;
        justify-content: flex-start !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #f8fafc !important;
        color: var(--text) !important;
    }

    /* ===== METRICS ===== */
    div[data-testid="metric-container"] { background-color: var(--card) !important; border: 1px solid #e6edf3 !important; border-radius: 12px !important; padding: 1rem !important; box-shadow: 0 1px 2px rgba(12,20,30,0.03) !important; }
    div[data-testid="metric-container"] label { color: #6b7280 !important; font-size: 0.8rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700 !important; font-size: 1.5rem !important; }

    /* ===== CONTAINERS ===== */
    div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 12px !important; border-color: #e6edf3 !important; background-color: var(--card) !important; }

    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader { background-color: var(--card) !important; border: 1px solid #e6edf3 !important; border-radius: 10px !important; font-weight: 600 !important; color: var(--text) !important; font-size: 0.95rem !important; }

    /* ===== DATAFRAMES ===== */
    .stDataFrame { border-radius: 10px !important; overflow: hidden !important; border: 1px solid #e6edf3 !important; }

    /* ===== MULTISELECT ===== */
    .stMultiSelect > div { border-radius: 10px !important; border-color: #e6edf3 !important; }
    .stMultiSelect > div > div { background-color: var(--card) !important; }

    /* ===== ALERTS ===== */
    .stAlert { border-radius: 10px !important; border: none !important; }
    div[data-testid="stAlert"] { padding: 1rem 1.25rem !important; }

    /* ===== FOOTER ===== */
    .footer { text-align: center; padding: 1.5rem; color: #6b7280; font-size: 0.9rem; border-top: 1px solid #e6edf3; margin-top: 2.5rem; }

    /* ===== HIDE DEFAULT ELEMENTS ===== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
with st.spinner("Loading data..."):
    data_dict = load_data()

if data_dict is None:
    st.error("Missing data files. Please check 'data/processed' or 'results/tables' directories.")
    st.stop()

df = data_dict["cleaned_data"]
clustering_results = data_dict["clustering_results"]
cluster_summary = data_dict["cluster_summary"]
rules = data_dict["association_rules"]
co_matrix = data_dict["co_occurrence"]

# ===== SIDEBAR NAVIGATION =====
pages = ["Overview", "Disease Prevalence", "Comorbidity Network", "Association Rules", "Patient Clusters", "Insights"]
icons = ["🏠", "📊", "🔗", "📋", "👥", "💡"]

if 'page' not in st.session_state:
    st.session_state.page = pages[0]

# Sidebar Brand
st.sidebar.markdown("""
<div class="sidebar-brand">
    <p class="sidebar-brand-title">🏥 Comorbidity Analysis</p>
    <p class="sidebar-brand-subtitle">Network Dashboard</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<p class="nav-label">Navigation</p>', unsafe_allow_html=True)

# Navigation Items
for page_name, icon in zip(pages, icons):
    if st.session_state.page == page_name:
        st.sidebar.markdown(
            f'<div class="nav-item-active">{icon} {page_name}</div>',
            unsafe_allow_html=True
        )
    else:
        if st.sidebar.button(f"{icon}  {page_name}", key=f"nav_{page_name}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Chronic Disease Analysis Dashboard")

# ===== MAIN CONTENT =====

# --- OVERVIEW PAGE ---
if st.session_state.page == "Overview":
    st.markdown('<p class="page-header">Dashboard Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheader">Key metrics and insights from comorbidity analysis</p>', unsafe_allow_html=True)
    
    # KPI Metrics
    st.markdown('<p class="card-title">Key Performance Indicators</p>', unsafe_allow_html=True)
    display_kpi_metrics(df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dataset Preview
    with st.expander("Preview Dataset", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

# --- DISEASE PREVALENCE PAGE ---
elif st.session_state.page == "Disease Prevalence":
    st.markdown('<p class="page-header">Disease Prevalence</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheader">Distribution of chronic diseases in the dataset</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("##### Disease Distribution")
            plot_prevalence(df)
    
    with col2:
        with st.container(border=True):
            st.markdown("##### Diabetes Breakdown")
            plot_diabetes_distribution(df)

# --- COMORBIDITY NETWORK PAGE ---
elif st.session_state.page == "Comorbidity Network":
    st.markdown('<p class="page-header">Comorbidity Network</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheader">Visualizing disease co-occurrence relationships</p>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.info("💡 Edge thickness indicates co-occurrence strength between conditions")
        plot_network_graph(co_matrix)

# --- ASSOCIATION RULES PAGE ---
elif st.session_state.page == "Association Rules":
    st.markdown('<p class="page-header">Association Rules</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheader">Discovered patterns in disease co-occurrence</p>', unsafe_allow_html=True)
    
    # Filters
    diseases_list = ['HighBP', 'HighChol', 'Stroke', 'HeartDiseaseorAttack', 'Diabetes_012']
    selected_disease = st.multiselect("Filter by condition:", diseases_list, default=[])
    
    filtered_rules = rules.copy()
    if selected_disease:
        pattern = '|'.join(selected_disease)
        filtered_rules = filtered_rules[
            filtered_rules['antecedents'].str.contains(pattern, na=False) | 
            filtered_rules['consequents'].str.contains(pattern, na=False)
        ]
    
    st.markdown(f"**Showing {len(filtered_rules)} rules**")
    
    if not filtered_rules.empty:
        def highlight_lift(val):
            if val > 5: return 'background-color: #fef2f2; color: #dc2626; font-weight: 600'
            if val > 3: return 'background-color: #fffbeb; color: #d97706; font-weight: 600'
            if val > 2: return 'background-color: #f0fdf4; color: #16a34a; font-weight: 600'
            return ''
        
        styled = filtered_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].style\
            .map(highlight_lift, subset=['lift'])\
            .format({'support': '{:.3f}', 'confidence': '{:.3f}', 'lift': '{:.2f}'})
        
        st.dataframe(styled, use_container_width=True)
        
        st.markdown("""
        <div style="display: flex; gap: 1rem; margin-top: 0.5rem; font-size: 0.8rem; color: #64748b;">
            <span>🔴 Lift > 5 (Very Strong)</span>
            <span>🟠 Lift > 3 (Strong)</span>
            <span>🟢 Lift > 2 (Moderate)</span>
        </div>
        """, unsafe_allow_html=True)

# --- PATIENT CLUSTERS PAGE ---
elif st.session_state.page == "Patient Clusters":
    st.markdown('<p class="page-header">Patient Clusters</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheader">Risk-based patient segmentation analysis</p>', unsafe_allow_html=True)
    
    cluster_labels = {0: "Hypertension-Dominant", 1: "Low-Risk", 2: "High-Risk Severe"}
    
    with st.container(border=True):
        st.markdown("##### Cluster Distribution")
        plot_cluster_distribution(clustering_results, cluster_labels)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("##### Cluster Profiles")
        st.caption("Average disease prevalence per cluster")
        plot_cluster_profiles(cluster_summary, cluster_labels)

# --- INSIGHTS PAGE ---
elif st.session_state.page == "Insights":
    st.markdown('<p class="page-header">Key Insights</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subheader">Summary of findings and recommendations</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("##### 📌 Major Findings")
            st.markdown("""
            - **Hypertension & High Cholesterol** are primary gateways to severe conditions
            - Strong associations (Lift > 3-5) found with Heart Disease & Stroke
            - High-risk cluster patients need urgent intervention
            - Low-risk groups benefit most from preventive programs
            """)
    
    with col2:
        with st.container(border=True):
            st.markdown("##### ✅ Recommendations")
            st.markdown("""
            - Prioritize BP and Cholesterol screening programs
            - Implement targeted care pathways for high-risk patients
            - Develop preventive interventions for low-risk groups
            - Monitor comorbidity progression in hypertensive patients
            """)

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    <p>Comorbidity Network Analysis Dashboard</p>
</div>
""", unsafe_allow_html=True)