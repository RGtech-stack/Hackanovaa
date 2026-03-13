import json

def get_resource():

    with open("data/volunteers.json") as f:
        volunteers = json.load(f)

    for v in volunteers:
        if v["available"]:
            return v

    return {"name": "No resource available"}