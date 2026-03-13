from ip_location import get_location_from_ip


def process_sms_with_ip(message, ip_address):
    """
    Handles SMS message when GPS is not available.
    Uses sender IP to estimate location.
    """

    print("[SMS Handler] Processing message")

    location = get_location_from_ip(ip_address)

    if location:

        sos_data = {
            "source": "sms_ip",
            "message": message,

            "lat": location["lat"],
            "lon": location["lon"],

            "people": 1,
            "urgency": 6,
            "flood_risk": 4,
            "waiting_time": 0,

            "road_status": "UNKNOWN",
            "volunteers_available": True,
            "internet_available": True
        }

        return sos_data

    return None


# Testing
if __name__ == "__main__":

    sms = "Water rising please help"

    ip = "8.8.8.8"

    result = process_sms_with_ip(sms, ip)

    print(result)