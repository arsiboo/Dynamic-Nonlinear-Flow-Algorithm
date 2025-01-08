def dfs(residual_graph, source, sink):
    visited_vertices = set()
    unvisited_paths = [(source, [source])]
    while unvisited_paths:
        current_vertex, current_path = unvisited_paths.pop()
        visited_vertices.add(current_vertex)
        for neighbor in residual_graph.neighbors(current_vertex):
            if neighbor not in visited_vertices and residual_graph[current_vertex][neighbor]['capacity'] > 0:
                if neighbor == sink:
                    return current_path + [neighbor]
                unvisited_paths.append((neighbor, current_path + [neighbor]))

    return None

