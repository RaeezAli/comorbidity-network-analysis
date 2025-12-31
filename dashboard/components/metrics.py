import streamlit as st

def display_kpi_metrics(df):
    """
    Displays the Key Performance Indicators (KPIs) cards.
    """
    st.markdown("### Key Performance Indicators (KPIs)")
    
    total_patients = len(df)
    perc_highbp = (df['HighBP'].sum() / total_patients) * 100
    perc_highchol = (df['HighChol'].sum() / total_patients) * 100
    perc_heart = (df['HeartDiseaseorAttack'].sum() / total_patients) * 100
    perc_stroke = (df['Stroke'].sum() / total_patients) * 100
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Patients", f"{total_patients:,}")
    col2.metric("% High BP", f"{perc_highbp:.1f}%")
    col3.metric("% High Cholesterol", f"{perc_highchol:.1f}%")
    col4.metric("% Heart Disease", f"{perc_heart:.1f}%")
    col5.metric("% Stroke", f"{perc_stroke:.1f}%")
    
    st.markdown("---")
