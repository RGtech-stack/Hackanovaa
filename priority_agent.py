def get_priority(people, urgency):

    urgency_map = {
        "low":1,
        "medium":2,
        "high":3,
        "critical":4
    }

    score = people * urgency_map.get(urgency,1)

    if score >= 10:
        level = "CRITICAL"
    elif score >= 6:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {"priority": level, "score": score}