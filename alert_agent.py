import json

def check_alerts():

    with open("data/roads.json") as f:
        roads = json.load(f)

    blocked = []

    for road in roads:
        if road["status"] != "open":
            blocked.append(road["name"])

    return blocked