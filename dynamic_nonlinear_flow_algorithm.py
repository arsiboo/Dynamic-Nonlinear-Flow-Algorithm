from dependencies import dfs

def dynamic_nonlinear_flow(graph, source, sink, arrival_rates=None):
    static_residual_graph = graph.copy()
    dynamic_residual_graph = graph.copy()
    wards_behaviour_list = []
    paths = []
    time = 0

    for arrival_rate in arrival_rates:
        for u, v, data in graph.edges(data=True):
            service_time = 0
            while not (float(graph.nodes[v]['los_min']) <= service_time <= float(graph.nodes[v]['los_max'])):
                service_time = graph.nodes[v]['distribution_function'].rvs(**graph.nodes[v]['distribution_args'])
            #outdeg=graph.out_degree(u)
            #data['distribution_probability'] = 1/outdeg
            service_rate_node = graph.nodes[v]['num_server'] / service_time
            flow_intensity_node = arrival_rate / service_rate_node
            ratio = flow_intensity_node / (1 - flow_intensity_node)
            vertex_cap = graph.nodes[v]['beds'] * ratio
            inflow_edge = data['distribution_probability'] * arrival_rate
            edge_cap = data['buffer'] * inflow_edge
            static_residual_graph[u][v]['capacity'] = edge_cap + vertex_cap

        while True:
            path = dfs(static_residual_graph, source, sink)

            if path is None:
                break
            else:
                paths.append(path)

            min_capacity = min(static_residual_graph[u][v]['capacity'] for u, v in zip(path, path[1:]))

            for u, v in zip(path, path[1:]):
                static_residual_graph[u][v]['capacity'] -= min_capacity

        for u, v, attr in dynamic_residual_graph.edges(data=True):
            if 'max_capacity' not in attr:
                attr['max_capacity'] = 0
            if 'min_capacity' not in attr:
                attr['min_capacity'] = float('inf')
            res = static_residual_graph[u][v]
            attr['max_capacity'] = max(attr['max_capacity'], res['capacity'])
            attr['min_capacity'] = min(attr['min_capacity'], res['capacity'])
            wards_behaviour_list.append([v, time, res['capacity']])
        time += 1

    return dynamic_residual_graph, wards_behaviour_list, paths

