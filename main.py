import pandas as pd
from dynamic_nonlinear_flow_algorithm import dynamic_nonlinear_flow
import scipy.stats
import networkx as nx
import os


######################################## Accessing Data in the File ###############################################
hospital_name="mini-hospital"
hospital_file=hospital_name+".xlsx"
directory = hospital_name+"-fitter"
ignored_files = [directory + "/.DS_Store"]

edges_df = pd.read_excel(hospital_file, sheet_name='edges')
vertices_df = pd.read_excel(hospital_file, sheet_name='vertices')
los_df = pd.read_excel(hospital_file, sheet_name="service_time").dropna(subset=['los_ward'])
rate_per_hour = pd.read_excel(hospital_file, sheet_name='arrival_rate')['arrival_rate'].tolist()

wards_dists = {}
wards_args = {}

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and f not in ignored_files:
        dist_params = pd.read_excel(f, index_col=0)
        dist_name = dist_params.columns[0]
        dist_args = dist_params[dist_name].to_dict()
        ward_name = f.replace(directory + "/fitted_distributions_", '').replace('.xlsx', '')
        wards_dists[ward_name] = getattr(scipy.stats, dist_name)
        wards_args[ward_name] = dist_args

######################################## Network Creation and Data Preparation ###############################################
hospital = nx.DiGraph()

for index, vertex_row in vertices_df.iterrows():
    vertex = vertex_row['vertex']
    beds = vertex_row['beds']
    num_server = vertex_row['staff']
    hospital.add_node(vertex, beds=beds, num_server=num_server)

for index, edge_row in edges_df.iterrows():
    source = edge_row['source']
    target = edge_row['target']
    buffer_value = edge_row['buffer']
    distribution_prob = edge_row['distribution_probability']
    hospital.add_edge(source, target, buffer=buffer_value, distribution_probability=distribution_prob)

for node, data in hospital.nodes(data=True):
    if node in wards_dists:
        hospital.nodes[node]['distribution_function'] = wards_dists[node]
        hospital.nodes[node]['distribution_args'] = wards_args[node]
        filtered_df = los_df[los_df['ward_name'] == node]
        hospital.nodes[node]['los_min'] = filtered_df["los_ward"].min()
        hospital.nodes[node]['los_max'] = filtered_df["los_ward"].max()

######################################## Defining vertices for the flow to begin and end ###########################################
source = 'Source'
sink = 'Sink'

######################################## Indicating the duration of the simulation in days ##########################################
Days = 1
rate_per_hour_duration = rate_per_hour * Days

######################################## Calling the dynamic nonlinear flow algorithm ###############################################
dyn_graph, dyn_nonlinear_wards, flow_path = dynamic_nonlinear_flow(hospital, source, sink, arrival_rates=rate_per_hour_duration)

############################### Storing the data to measure the bottlenecks persistency, severity and overflow #################################
node_labels = sorted(dyn_graph.nodes())

df_minmax = pd.DataFrame(columns=node_labels, index=node_labels)

for node_i in node_labels:
    for node_j in node_labels:
        if dyn_graph.has_edge(node_i, node_j):
            edge_data = dyn_graph.get_edge_data(node_i, node_j)
            min_capacity = edge_data.get('min_capacity', 'N')
            max_capacity = edge_data.get('max_capacity', 'N')
            df_minmax.loc[node_i, node_j] = f"{min_capacity:.2f}:{max_capacity:.2f}"
        else:
            df_minmax.loc[node_i, node_j] = "N"

df_minmax.to_excel('OUTPUT/minmax_graph.xlsx', index=True)

##################################### Storing the data to measure the wards dynamic nonlinear behaviour ##########################################
df_all = pd.DataFrame(dyn_nonlinear_wards, columns=["ward", "time", "residual capacity"])
df_all.to_csv("OUTPUT/wards_behaviour.csv", index=False)

######################################## Storing the data to observe the flow through the network paths ###############################################
flow_p = pd.DataFrame(flow_path)
flow_p.to_excel("OUTPUT/paths.xlsx", index=False)

