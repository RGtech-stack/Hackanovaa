def get_route(location, blocked_roads):

    routes = [
        ["Main Street", "Hospital Road"],
        ["River Road", "Market Road"],
        ["Bridge Road", "City Center"]
    ]

    safe_routes = []

    for route in routes:

        blocked = False

        for road in route:
            if road in blocked_roads:
                blocked = True

        if not blocked:
            safe_routes.append(route)

    if safe_routes:
        return safe_routes[0]

    return ["No safe route found"]