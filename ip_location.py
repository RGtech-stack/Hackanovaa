import requests

def get_location_from_ip(ip_address):
    """
    Convert IP address into approximate GPS coordinates
    using ip-api geolocation service.
    """

    try:
        url = f"http://ip-api.com/json/{ip_address}"

        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":

            location_data = {
                "lat": data["lat"],
                "lon": data["lon"],
                "city": data["city"],
                "region": data["regionName"]
            }

            return location_data

        else:
            print("[IP Service] Location lookup failed")
            return None

    except Exception as e:
        print("[IP Service Error]", e)
        return None


# Testing
if __name__ == "__main__":

    test_ip = "8.8.8.8"

    location = get_location_from_ip(test_ip)

    print("Location:", location)