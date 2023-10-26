import pandas as pd
import networkx as nx
import os
import scipy.stats
from fitter import Fitter
from collections import deque


def iddfs(residual_graph, source, sink):
    max_depth = 0

    while True:
        result = dfs_with_depth_limit(residual_graph, source, sink, max_depth)
        if result is not None:
            return result
        max_depth += 1


def dfs_with_depth_limit(residual_graph, source, sink, max_depth):
    visited = set()
    stack = [(source, [source])]

    while stack:
        node, path = stack.pop()
        visited.add(node)

        if len(path) > max_depth:
            continue

        for neighbor in residual_graph.neighbors(node):
            if neighbor not in visited and residual_graph[node][neighbor]['capacity'] > 0:
                if neighbor == sink:
                    return path + [neighbor]
                stack.append((neighbor, path + [neighbor]))

    return None



def bfs(residual_graph, source, sink):
    visited = set()
    queue = [(source, [source])]

    while queue:
        node, path = queue.pop(0)
        visited.add(node)

        for neighbor in residual_graph.neighbors(node):
            if neighbor not in visited and residual_graph[node][neighbor]['capacity'] > 0:
                if neighbor == sink:
                    return path + [neighbor]
                queue.append((neighbor, path + [neighbor]))

    return None


def dfs(residual_graph, source, sink):
    visited = set()
    stack = [(source, [source])]

    while stack:
        node, path = stack.pop()
        visited.add(node)

        for neighbor in residual_graph.neighbors(node):
            if neighbor not in visited and residual_graph[node][neighbor]['capacity'] > 0:
                if neighbor == sink:
                    return path + [neighbor]
                stack.append((neighbor, path + [neighbor]))

    return None




folder_path = 'fitter/'

# Load edges from the "edges" sheet
edges_df = pd.read_excel('akademiska.xlsx', sheet_name='edges')

# Load vertices from the "vertices" sheet
vertices_df = pd.read_excel('akademiska.xlsx', sheet_name='vertices')

#Read the Excel file
arrival_df = pd.read_excel('akademiska.xlsx', sheet_name='arrival_rate')

rate_per_hour = arrival_df.iloc[:, 1].tolist()


# Create a directed graph named 'hospital'
hospital = nx.DiGraph()

# Add vertices to the graph
for index, vertex_row in vertices_df.iterrows():
    vertex = vertex_row['vertex']
    beds = vertex_row['beds']  # Assuming the column name is 'beds'
    num_server = vertex_row['beds']  # Assuming the column name is 'num_server'
    hospital.add_node(vertex, beds=beds, num_server=num_server)  # Add 'beds' and 'num_server' attributes to the node

# Add edges, 'buffer', and 'distribution_probability' attributes to the graph
for index, edge_row in edges_df.iterrows():
    source = edge_row['source']
    target = edge_row['target']
    buffer_value = edge_row['buffer']
    distribution_prob = edge_row['distribution_probability']  # Assuming the column name is 'distribution_probability'
    hospital.add_edge(source, target, buffer=buffer_value, distribution_probability=distribution_prob)



directory = 'Fitter'
ignored_files = [directory + "/.DS_Store"]

wards_dists = {}
wards_args = {}

orig_dataset = pd.read_excel("akademiska.xlsx", "service_time")
orig_dataset = orig_dataset.dropna(subset=['los_ward'])

# Assuming your DataFrame is named "orig_dataset"


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and f not in ignored_files:
        dist_params = pd.read_excel(f, index_col=0)
        dist_name = dist_params.columns[0]
        dist_args = dist_params[dist_name].to_dict()
        ward_name = f.replace(directory + "/fitted_distributions_", '').replace('.xlsx', '')

        dataset = orig_dataset.loc[orig_dataset['OA_unit_SV'] == ward_name]
        dataset = dataset[['los_ward']]

        # dataset.info()

        wards_dists[ward_name] = getattr(scipy.stats, dist_name)
        wards_args[ward_name] = dist_args
        vals = wards_dists[ward_name].rvs(**dist_args, size=1000)
        vals_df = pd.DataFrame(vals, columns=[dist_name])
        vals_df2 = vals_df[vals_df[dist_name] < float(dataset.max())]

        pass


for node, data in hospital.nodes(data=True):
    if node in wards_dists:
        distribution_function = wards_dists[node]
        hospital.nodes[node]['distribution_function'] = distribution_function




