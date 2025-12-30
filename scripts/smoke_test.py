import networkx as nx
import pandas as pd

G = nx.Graph()
G.add_nodes_from(['HighBP','HighChol','Stroke','HeartDiseaseorAttack'])
G.add_edge('HighBP','HighChol', weight=50)
G.add_edge('HighBP','HeartDiseaseorAttack', weight=30)
G.add_edge('HighChol','HeartDiseaseorAttack', weight=25)
G.add_edge('HighBP','Stroke', weight=5)
G.add_edge('HighChol','Stroke', weight=3)
G.add_edge('HeartDiseaseorAttack','Stroke', weight=2)

degree_cent = nx.degree_centrality(G)
bet_cent = nx.betweenness_centrality(G, normalized=True)
close_cent = nx.closeness_centrality(G)

metrics_df = pd.DataFrame({
    'Degree Centrality': degree_cent,
    'Betweenness Centrality': bet_cent,
    'Closeness Centrality': close_cent
})

print(metrics_df)
