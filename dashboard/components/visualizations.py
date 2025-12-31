import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

# Set global style for cleaner academic look
sns.set_style("whitegrid")

def plot_prevalence(df):
    """Plots prevalence of target diseases."""
    target_diseases = ['HighBP', 'HighChol', 'Stroke', 'HeartDiseaseorAttack']
    available_diseases = [d for d in target_diseases if d in df.columns]
    
    if available_diseases:
        prevalence = df[available_diseases].mean() * 100
        prevalence_df = pd.DataFrame({'Condition': prevalence.index, 'Prevalence (%)': prevalence.values})
        prevalence_df = prevalence_df.sort_values(by='Prevalence (%)', ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        # Fix: Assign y to hue and set legend=False
        sns.barplot(x='Prevalence (%)', y='Condition', data=prevalence_df, hue='Condition', palette='Blues_r', ax=ax, legend=False)
        ax.set_title("Prevalence of Target Diseases", color='#0d47a1')
        st.pyplot(fig)
    else:
        st.error("Target disease columns not found in dataset.")

def plot_diabetes_distribution(df):
    """Plots distribution of diabetes status."""
    diabetes_counts = df['Diabetes_012'].value_counts(normalize=True) * 100
    diabetes_labels = {0: 'No Diabetes', 1: 'Pre-diabetes', 2: 'Diabetes'}
    diabetes_df = pd.DataFrame({
        'Status': [diabetes_labels.get(x, x) for x in diabetes_counts.index],
        'Percentage': diabetes_counts.values
    })
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    # Fix: Assign x to hue and set legend=False
    sns.barplot(x='Status', y='Percentage', data=diabetes_df, hue='Status', palette='Blues', ax=ax2, legend=False)
    ax2.set_title("Distribution of Diabetes Status", color='#0d47a1')
    st.pyplot(fig2)

def plot_network_graph(co_matrix):
    """Plots the disease comorbidity network."""
    G = nx.Graph()
    max_val = co_matrix.max().max() if not co_matrix.empty else 1
    central_nodes = ['HighBP', 'HighChol']
    
    for i, disease1 in enumerate(co_matrix.index):
        for j, disease2 in enumerate(co_matrix.columns):
            if i < j: 
                weight = co_matrix.iloc[i, j]
                if weight > 0:
                    G.add_edge(disease1, disease2, weight=weight)
    
    pos = nx.spring_layout(G, k=0.5, seed=42)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Node colors: Central = Dark Blue (#1565c0), Others = Light Blue (#bbdefb)
    node_colors = ['#1565c0' if node in central_nodes else '#bbdefb' for node in G.nodes()]
    
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    width_scale = [ (w / max_val) * 10 for w in weights]
    
    # Edges in gray
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=11, font_weight='bold', font_color='black', ax=ax)
    nx.draw_networkx_edges(G, pos, width=width_scale, edge_color='#90a4ae', alpha=0.6, ax=ax)
    
    ax.set_title("Disease Co-occurrence Strength (Thicker edge = Stronger link)", fontsize=14, color='#0d47a1')
    ax.axis('off')
    
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Primary Gateway Diseases', markerfacecolor='#1565c0', markersize=15),
        Line2D([0], [0], marker='o', color='w', label='Associated Comorbidities', markerfacecolor='#bbdefb', markersize=15)
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    st.pyplot(fig)

def plot_cluster_distribution(clustering_results, cluster_labels):
    """Plots the distribution of patients across clusters."""
    if 'Cluster' in clustering_results.columns:
        st.subheader("Cluster Distribution")
        counts = clustering_results['Cluster'].value_counts().rename(index=cluster_labels)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        # Fix: Assign y (index) to hue and set legend=False. Note: x is value, y is category.
        sns.barplot(y=counts.index, x=counts.values, hue=counts.index, palette='Blues_d', ax=ax, legend=False)
        ax.set_xlabel("Number of Patients")
        st.pyplot(fig)
    else:
        st.warning("Cluster column not found.")

def plot_cluster_profiles(cluster_summary, cluster_labels):
    """Plots the average disease presence for each cluster."""
    st.subheader("Average Disease Presence per Cluster")
    summary_plot = cluster_summary.rename(index=cluster_labels)
    summary_melted = summary_plot.reset_index().melt(id_vars='Cluster', var_name='Disease', value_name='Average Presence')
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    # Paired palette can work, or custom. Let's stick to 'Paired' or 'Set2' for distinction but soft tone. 
    # Or just 'Blues' with hue? No, hue needs different colors.
    # Let's use a professional palette like "ch:s=.25,rot=-.25" (cubehelix) or just 'viridis' but standard.
    # Actually, for medical, blue-ish variants are good. 'GnBu_d' is nice.
    sns.barplot(data=summary_melted, x='Cluster', y='Average Presence', hue='Disease', palette='GnBu_d', ax=ax2)
    
    # Fix: UserWarning: set_ticklabels() should only be used with a fixed number of ticks.
    # Use tick_params or set_xticks first.
    # Using drawing parameters to rotate ticks.
    plt.setp(ax2.get_xticklabels(), rotation=15, ha='right')
    
    ax2.set_xlabel("")
    ax2.set_title("Disease Profile by Cluster", color='#0d47a1')
    st.pyplot(fig2)
