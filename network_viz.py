import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


df = pd.read_excel("akademiska.xlsx", sheet_name="edges", usecols=[0, 1])

# Create a directed graph
G = nx.DiGraph()

# Add edges from the DataFrame data
for index, row in df.iterrows():
    G.add_edge(row[0], row[1])  # Add edge from the first column to the second column

# Use a spring layout with increased spacing
k_value = 3  # Adjust this value as needed
pos = nx.spring_layout(G, k=k_value)


# Set a larger figure size for better visibility
plt.figure(figsize=(15, 10))

# Initialize default color for all nodes and edges
node_colors = {node: '#55C0F3' for node in G.nodes()}
edge_colors = {edge: '#55C0F3' for edge in G.edges()}
edge_widths = {edge: 1 for edge in G.edges()}  # Default edge width



excel_file_path = 'OUTPUT/allpath/DP equally divided/1 year/paths1.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')

colored6 = "violet" # purple

paths = []
for index, row in df.iterrows():
    # Assuming each cell in a row is a node in the path
    path = row.tolist()
    # Remove NaN values which might occur due to empty cells
    path = [node for node in path if pd.notna(node)]
    # Append the path and color to the list
    paths.append((path, colored6))


# Color the nodes and edges according to the paths
for path, color in paths:
    for node in path:
        if node in G.nodes:
            node_colors[node] = color  # Color the node
    for edge in zip(path, path[1:]):
        if edge in G.edges:
            edge_colors[edge] = color  # Color the edge
            edge_widths[edge] = 3      # Increase edge width for visibility


# Calculate the central y-coordinate
y_center = sum(pos[node][1] for node in G.nodes()) / len(G.nodes())

# Manually set the positions of 'Source' and 'Sink'
pos['Source'] = (-1.5, y_center)  # Far left middle of the screen
node_colors['Source'] = '#25C54C'   # Set color for Source

pos['Sink'] = (1.5, y_center)  # Far right middle of the screen
node_colors['Sink'] = '#25C54C'   # Set color for Source

node_colors['EMERGENCY DEPARTMENT'] = 'black'   # Set color for Source


nx.draw(G, pos, with_labels=True, node_size=150, node_color=[node_colors[node] for node in G.nodes()],
        edge_color=[edge_colors[edge] for edge in G.edges()], width=[edge_widths[edge] for edge in G.edges()],
        font_size=8, node_shape='o', style='dashed')

plt.show()
