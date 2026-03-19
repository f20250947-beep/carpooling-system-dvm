from trips.utils import find_route

UNIT_PRICE = 10
BASE_FEE = 5

def calculate_detour(trip, pickup_node, dropoff_node):
    remaining_route = list(trip.route.filter(is_passed=False).values_list('node', flat=True))
    if not remaining_route:
        return None, None
    
    from network.models import Node
    remaining_nodes = [Node.objects.get(id=nid) for nid in remaining_route]
    
    original_length = len(remaining_nodes)
    
    # New route with pickup and dropoff inserted
    end_node = remaining_nodes[-1]
    new_route = find_route(remaining_nodes[0], pickup_node)
    if not new_route:
        return None, None
    route_to_dropoff = find_route(pickup_node, dropoff_node)
    if not route_to_dropoff:
        return None, None
    route_to_end = find_route(dropoff_node, end_node)
    if not route_to_end:
        return None, None
    
    new_length = len(new_route) + len(route_to_dropoff) + len(route_to_end) - 3
    detour = new_length - original_length
    
    # Fare calculation
    n = len(route_to_dropoff) - 1
    fare = UNIT_PRICE * sum(1/(i+1) for i in range(n)) + BASE_FEE
    
    return detour, round(fare, 2)