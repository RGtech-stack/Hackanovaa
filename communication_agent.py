def send_notification(resource, route, priority):

    message = f"""
    EMERGENCY RESPONSE

    Priority: {priority}
    Resource: {resource['name']}
    Route: {' -> '.join(route)}

    Help is on the way.
    """

    print(message)

    return message