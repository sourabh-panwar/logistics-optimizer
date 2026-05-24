def calculate_optimal_route(graph, start_node, destinations, demand_factors, lambda_coeff=10.0):
    """
    Executes a modified Nearest-Neighbor Traversal on a complete graph,
    reweighting edge selections dynamically based on destination demand.
    """
    unvisited = set(destinations)
    current_node = start_node
    full_path_sequence = [start_node]
    total_physical_distance = 0.0
    
    while unvisited:
        best_next_node = None
        best_modified_cost = float('inf')
        true_distance_to_best = 0.0
        
        # Evaluate all adjacent edges from the current vertex
        for neighbor, distance in graph.get(current_node, []):
            if neighbor in unvisited:
                # Apply the demand reweighting equation
                demand = demand_factors.get(neighbor, 0.0)
                modified_cost = distance - (lambda_coeff * demand)
                
                # Identify the optimal local minimum
                if modified_cost < best_modified_cost:
                    best_modified_cost = modified_cost
                    best_next_node = neighbor
                    true_distance_to_best = distance
                    
        # Append the optimal selected vertex to our sequence state
        if best_next_node is not None:
            full_path_sequence.append(best_next_node)
            total_physical_distance += true_distance_to_best
            unvisited.remove(best_next_node)
            current_node = best_next_node
        else:
            break

    return {
        "optimal_sequence": full_path_sequence,
        "total_distance_km": round(total_physical_distance, 2),
        "execution_status": "Success"
    }