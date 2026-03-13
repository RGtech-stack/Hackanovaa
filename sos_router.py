import requests

from sms_gateway import process_offline_sms
from sms_ip_merge import process_sms_with_ip
from orchestrator import orchestrator


def check_internet():
    """
    Checks if internet connection is available
    """

    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False


def handle_sos(message, sender_ip=None):

    internet_available = check_internet()

    # Case 1: Internet available → API SOS
    if internet_available:

        print("[Router] Internet detected → Using API SOS")

        sos_data = {
            "source": "api",
            "message": message,
            "lat": None,
            "lon": None,
            "people": 1,
            "urgency": 6,
            "flood_risk": 4,
            "waiting_time": 0
        }

        return orchestrator(sos_data)

    # Case 2: No internet → SMS SOS
    else:

        print("[Router] No internet → Using SMS SOS")

        # First check if GPS exists in SMS
        sms_data = process_offline_sms(message)

        if sms_data:
            return orchestrator(sms_data)

        # Otherwise estimate location via IP
        sos_data = process_sms_with_ip(message, sender_ip)

        return orchestrator(sos_data)


# Test
if __name__ == "__main__":

    sms_message = "Water rising please help"
    sender_ip = "8.8.8.8"

    result = handle_sos(sms_message, sender_ip)

    print(result)