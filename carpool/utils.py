from trips.utils import find_route

def calculate_detour(trip, pickup, drop):
    driver_start = trip.start_node
    driver_end = trip.end_node

    # original route
    original = find_route(driver_start, driver_end)
    if not original:
        return None, None

    # new route parts
    path1 = find_route(driver_start, pickup)
    path2 = find_route(pickup, drop)
    path3 = find_route(drop, driver_end)

    if not path1 or not path2 or not path3:
        return None, None

    # combine paths (avoid duplicate nodes)
    new_path = path1[:-1] + path2[:-1] + path3

    original_len = len(original) - 1
    new_len = len(new_path) - 1

    detour = new_len - original_len

    # simple fare (you can upgrade later)
    fare = 10 + detour * 5

    return detour, fare