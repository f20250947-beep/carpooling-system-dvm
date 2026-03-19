from network.models import Edge

def find_route(start_node, end_node):
    if start_node == end_node:
        return [start_node]

    visited = set()
    queue = [[start_node]]

    while queue:
        path = queue.pop(0)
        current = path[-1]

        if current in visited:
            continue
        visited.add(current)

        edges = Edge.objects.filter(from_node=current)
        for edge in edges:
            new_path = path + [edge.to_node]
            if edge.to_node == end_node:
                return new_path
            queue.append(new_path)

    return None