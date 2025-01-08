import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


df = pd.read_excel("akademiska.xlsx", sheet_name="edges", usecols=[0, 1])
G = nx.DiGraph()
for index, row in df.iterrows():
    G.add_edge(row[0], row[1])

k_value = 3
pos = nx.spring_layout(G, k=k_value)

plt.figure(figsize=(15, 10))

node_colors = {node: '#55C0F3' for node in G.nodes()}
edge_colors = {edge: '#55C0F3' for edge in G.edges()}
edge_widths = {edge: 1 for edge in G.edges()}


excel_file_path = 'OUTPUT/paths.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

colored6 = "violet"

paths = []
for index, row in df.iterrows():
    path = row.tolist()
    path = [node for node in path if pd.notna(node)]
    paths.append((path, colored6))


for path, color in paths:
    for node in path:
        if node in G.nodes:
            node_colors[node] = color
    for edge in zip(path, path[1:]):
        if edge in G.edges:
            edge_colors[edge] = color
            edge_widths[edge] = 3


y_center = sum(pos[node][1] for node in G.nodes()) / len(G.nodes())

pos['Source'] = (-1.5, y_center)
node_colors['Source'] = '#25C54C'

pos['Sink'] = (1.5, y_center)
node_colors['Sink'] = '#25C54C'

node_colors['EMERGENCY DEPARTMENT'] = 'black'
node_colors['Emergency Department'] = 'black'


nx.draw(G, pos, with_labels=True, node_size=150, node_color=[node_colors[node] for node in G.nodes()],
        edge_color=[edge_colors[edge] for edge in G.edges()], width=[edge_widths[edge] for edge in G.edges()],
        font_size=12, node_shape='o', style='dashed')

plt.show()
