import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    """
    Loads necessary CSV files from the data and results directories.
    Returns a dictionary of DataFrames.
    """
    # Assuming the app is run from the project root, so paths are relative to root
    data_paths = {
        "cleaned_data": "data/processed/cleaned_data.csv",
        "clustering_results": "results/tables/clustering_results.csv",
        "cluster_summary": "results/tables/cluster_summary.csv",
        "association_rules": "results/tables/association_rules.csv",
        "co_occurrence": "results/tables/co_occurrence_matrix.csv"
    }
    
    dfs = {}
    for key, path in data_paths.items():
        if os.path.exists(path):
            if key == "co_occurrence":
                dfs[key] = pd.read_csv(path, index_col=0) 
            elif key == "cluster_summary":
                dfs[key] = pd.read_csv(path, index_col=0)
            else:
                dfs[key] = pd.read_csv(path)
        else:
            return None
    return dfs
