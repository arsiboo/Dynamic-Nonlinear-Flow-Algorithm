# modified dinitz flow algorithm Description:
# This is a dynamic non-linear flow algorithm based on dinitz flow algorithm.
# The Algorithm has been extended by two feathres: 1) Continous flow, 2) Discrete flow
# Furthermore, the algorithm is modified to provide two type of outputs: 1) Residual graph, 2) minmax graph.
# The residual graph is suitable for continous flow and the minmax graph is suitable for discrete flow, but both can be generated at the same time
# The residual graph's lowest value indicate the bottleneck is higher, the mixmax graph shows the persistency of the botttlneck.
# If the variance in minmax graph is small, it means that there was a persistent bottleneck.

import networkx as nx
import pandas as pd
from inputs_functions import bfs, rate_per_hour, hospital, wards_args, orig_dataset


def dynamic_nonlinear_dinic(graph, source, sink, edge_information=None, node_information=None, flow_rates=None):
    residual_graph = nx.DiGraph()
    min_max_graph = graph.copy()  # This is more useful
    # max_flow = 0
    # dynamic capacity:
    for flow_rate in flow_rates:
        residual_graph = graph.copy()  # enabling provides remaining capaacity for a discrete flow, disabling provides remaining capacity for a continuous flow
        # max_flow = 0
        for u, v, data in hospital.edges(data=True):
            dist = 0
            filtered_df = orig_dataset[orig_dataset.iloc[:, 2] == v]
            while not (filtered_df["los_ward"].min() <= dist <= filtered_df["los_ward"].max()):
                dist = hospital.nodes[v]['distribution_function'].rvs(**wards_args[v])
            usage = flow_rate / (hospital.nodes[v]['num_server'] * dist)
            node_capacity = hospital.nodes[v]['beds'] * usage
            residual_graph[u][v]['capacity'] = (data['buffer'] + node_capacity) * data['distribution_probability']

        while True:
            path = bfs(residual_graph, source, sink)
            if path is None:
                break

            min_capacity = min(residual_graph[u][v]['capacity'] for u, v in zip(path, path[1:]))

            for u, v in zip(path, path[1:]):
                residual_graph[u][v]['capacity'] -= min_capacity  # forward edge
                # if not residual_graph.has_edge(v, u):
                #    residual_graph.add_edge(v, u, capacity=0)
                # residual_graph[v][u]['capacity'] += min_capacity  # backward edge

            # max_flow += min_capacity

        for u, v, data in min_max_graph.edges(data=True): # Extended section
            if 'max_capacity' not in data:
                data['max_capacity'] = 0
            if 'min_capacity' not in data:
                data['min_capacity'] = 0

        for u, v, attr in min_max_graph.edges(data=True): # Extended section
            res = residual_graph[u][v]
            capacity = res['capacity']
            attr['max_capacity'] = max(attr.get('max_capacity', 0), capacity)
            attr['min_capacity'] = min(attr.get('min_capacity', float('inf')), capacity) if attr.get('min_capacity',
                                                                                                     float(
                                                                                                         'inf')) != 0 else capacity

    return residual_graph, min_max_graph  # the lower, the worse, and the closer, the higher the persistency.








# running the function
source = 'Source'
sink = 'Sink'

res_graph, maxmin_graph = dynamic_nonlinear_dinic(hospital, source, sink, edge_information=hospital.edges,
                                                  node_information=hospital.nodes,
                                                  flow_rates=rate_per_hour)

node_labels = sorted(res_graph.nodes())

# The residual graph represents the bottlenecks, the lower the numbers, the higher is the overall bottleneck
df_residual = pd.DataFrame(columns=node_labels, index=node_labels)

for node_i in node_labels:
    for node_j in node_labels:
        if res_graph.has_edge(node_i, node_j):
            edge_weight = res_graph.get_edge_data(node_i, node_j).get('capacity', "N")
            df_residual.loc[node_i, node_j] = f"{edge_weight:.2f}"
        else:
            df_residual.loc[node_i, node_j] = "N"

# Write the DataFrame to an Excel file
df_residual.to_excel('OUTPUT/residual_graph.xlsx', index=True)

# This one represents the lowest and the highest bottlenecks, the closer is the value the higher is the persistency
df_minmax = pd.DataFrame(columns=node_labels, index=node_labels)

for node_i in node_labels:
    for node_j in node_labels:
        if maxmin_graph.has_edge(node_i, node_j):
            edge_data = maxmin_graph.get_edge_data(node_i, node_j)
            min_capacity = edge_data.get('min_capacity', 'N')
            max_capacity = edge_data.get('max_capacity', 'N')
            df_minmax.loc[node_i, node_j] = f"{min_capacity:.2f}-{max_capacity:.2f}"
        else:
            df_minmax.loc[node_i, node_j] = "N"

# Write the DataFrame to an Excel file
df_minmax.to_excel('OUTPUT/minmax_graph.xlsx', index=True)
