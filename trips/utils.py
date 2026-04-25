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

def calculate_detour(driver_start, driver_end, pickup, drop):
    original = find_route(driver_start, driver_end)

    path1 = find_route(driver_start, pickup)
    path2 = find_route(pickup, drop)
    path3 = find_route(drop, driver_end)

    if not original or not path1 or not path2 or not path3:
        return None

    new_path = path1[:-1] + path2[:-1] + path3

    original_len = len(original) - 1
    new_len = len(new_path) - 1

    return new_len - original_len