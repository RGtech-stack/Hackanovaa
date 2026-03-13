import re


def process_offline_sms(sms_text):
    """
    Offline SMS ingestion gateway.
    Extracts GPS coordinates from SMS and converts them into
    structured SOS data for the orchestrator.
    """

    print(f"[SMS Gateway] Processing incoming SMS: '{sms_text}'")

    # Regex pattern for GPS format: LOC:lat,lon
    gps_pattern = r"LOC:\s*([-+]?[0-9]*\.?[0-9]+)\s*,\s*([-+]?[0-9]*\.?[0-9]+)"

    match = re.search(gps_pattern, sms_text)

    if match:
        try:
            latitude = float(match.group(1))
            longitude = float(match.group(2))

            print(f"[SUCCESS] GPS coordinates extracted → Lat: {latitude}, Lon: {longitude}")

            # Create structured SOS data
            sos_data = {
                "source": "offline_sms",
                "lat": latitude,
                "lon": longitude,

                # Default values (can be updated later by agents)
                "people": 1,
                "urgency": 7,  # Slightly higher due to offline condition
                "flood_risk": 4,
                "waiting_time": 0,

                "road_status": "UNKNOWN",
                "volunteers_available": True,
                "internet_available": False,

                # Trust GPS location
                "verified": True
            }

            return sos_data

        except ValueError:
            print("[ERROR] Invalid coordinate format")
            return None

    else:
        print("[INFO] No GPS coordinates found in SMS")
        return None


# Test block
if __name__ == "__main__":

    print("=== Offline SMS Gateway Test ===")

    # Test case 1
    print("\n--- Test 1: Valid GPS SMS ---")
    msg1 = "Need rescue urgently LOC:19.2044,72.8360"
    result1 = process_offline_sms(msg1)
    print("Result:", result1)

    # Test case 2
    print("\n--- Test 2: Message without GPS ---")
    msg2 = "Water level rising near Kandivali station!"
    result2 = process_offline_sms(msg2)
    print("Result:", result2)