import math
import networkx as nx
import pandas as pd
import numpy as np
from inputs_functions import dfs, rate_per_hour, hospital, wards_args, orig_dataset

my_ward1 = "Medicinavdelning 30 E"
my_ward2 = "Infektionsavdelning 30 F"
my_ward3 = "EMERGENCY DEPARTMENT"


def dynamic_nonlinear_flow(graph, source, sink, arrival_rates=None):
    static_residual_graph = graph.copy()  # Initialized here to make sure they are not reseted by each arrival rate
    dynamic_residual_graph = graph.copy()  # Initialized here to make sure they are not reseted by each arrival rate
    # max_flow = 0
    mylist1 = []
    mylist2 = []
    mylist3 = []
    debugging = []
    paths = []
    time = 0


    for arrival_rate in arrival_rates:
        # max_flow = 0

        for u, v, data in graph.edges(data=True):
            service_time = 0
            filtered_df = orig_dataset[orig_dataset.iloc[:, 2] == v]
            while not (filtered_df["los_ward"].min() <= service_time <= filtered_df["los_ward"].max()):
                service_time = graph.nodes[v]['distribution_function'].rvs(**wards_args[v])
            #outdeg=graph.out_degree(u)
            #data['distribution_probability'] = 1/outdeg
            service_rate_node = graph.nodes[v]['num_server'] / service_time
            traffic_intensity_node = arrival_rate / service_rate_node
            ratio = traffic_intensity_node / (1 - traffic_intensity_node)
            inflow_edge = data['distribution_probability'] * arrival_rate
            edge_cap = data['buffer'] * inflow_edge
            node_cap = graph.nodes[v]['beds'] * ratio
            adjusted_cap = edge_cap + node_cap
            static_residual_graph[u][v]['capacity'] = adjusted_cap



        while True:
            path = dfs(static_residual_graph, source, sink)

            if path is None:
                break
            else:
                paths.append(path)

            min_capacity = min(static_residual_graph[u][v]['capacity'] for u, v in zip(path, path[1:]))

            for u, v in zip(path, path[1:]):
                static_residual_graph[u][v]['capacity'] -= min_capacity  # forward edge
                # if not static_residual_graph.has_edge(v, u):
                #    static_residual_graph.add_edge(v, u, capacity=0)
                # static_residual_graph[v][u]['capacity'] += min_capacity  # backward edge

            # max_flow += min_capacity
        for u, v, attr in dynamic_residual_graph.edges(data=True):  # Extended section
            if 'max_capacity' not in attr:
                attr['max_capacity'] = 0
            if 'min_capacity' not in attr:
                attr['min_capacity'] = float('inf')
            res = static_residual_graph[u][v]
            attr['max_capacity'] = max(attr['max_capacity'], res['capacity'])
            attr['min_capacity'] = min(attr['min_capacity'], res['capacity'])
            if v == my_ward1:
                mylist1.append([time, res['capacity']])
            if v == my_ward2:
                mylist2.append([time, res['capacity']])
            if v == my_ward3:
                mylist3.append([time, res['capacity']])
        time += 1

    return static_residual_graph, dynamic_residual_graph, mylist1, mylist2, mylist3,debugging, paths









source = 'Source'
sink = 'Sink'

rate_per_hour_for_longer = rate_per_hour * 1

res_graph, maxmin_graph, dyn_nonlinear1, dyn_nonlinear2, dyn_nonlinear3,debug,coll_path = dynamic_nonlinear_flow(hospital, source, sink,
                                                                                                 arrival_rates=rate_per_hour_for_longer)

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
            df_minmax.loc[node_i, node_j] = f"{min_capacity:.2f}:{max_capacity:.2f}"
        else:
            df_minmax.loc[node_i, node_j] = "N" 

df_minmax.to_excel('OUTPUT/minmax_graph.xlsx', index=True)

df1 = pd.DataFrame(dyn_nonlinear1, columns=["time", "residual capacity"])
df2 = pd.DataFrame(dyn_nonlinear2, columns=["time", "residual capacity"])
df3 = pd.DataFrame(dyn_nonlinear3, columns=["time", "residual capacity"])


df1.to_excel("OUTPUT/" + my_ward1 + ".xlsx", index=False)
df2.to_excel("OUTPUT/" + my_ward2 + ".xlsx", index=False)
df3.to_excel("OUTPUT/" + my_ward3 + ".xlsx", index=False)

deb = pd.DataFrame(debug, columns=["Name", "Value"])
deb.to_excel("OUTPUT/debugging/debug.xlsx", index=False)

deb = pd.DataFrame(coll_path)

deb.to_excel("OUTPUT/allpath/paths.xlsx", index=False)

