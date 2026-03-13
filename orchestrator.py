from agents.sos_agent import process_sos
from agents.verification_agent import verify_emergency
from agents.priority_agent import get_priority
from agents.alert_agent import check_alerts
from agents.routing_agent import get_route
from agents.resource_agent import get_resource
from agents.communication_agent import send_notification

# SMS MODULES
from SMS.sms_gateway import receive_sms
from SMS.ip_location import get_location_from_ip
from SMS.sms_ip_merge import merge_sms_ip
from SMS.sos_router import route_sos


def run_agents(raw_message, lat=None, lon=None):

    print("\n========== AGENTIC AI DISASTER RESPONSE ==========")

    # SOS AGENT
    print("\n[SOS AGENT] Processing SOS message...")
    sos_data = process_sos(raw_message)

    if sos_data is None:
        return {"status": "error", "message": "Failed to parse SOS message"}

    # attach GPS
    if lat and lon:
        sos_data["lat"] = lat
        sos_data["lon"] = lon
    else:
        sos_data["lat"] = 19.1136
        sos_data["lon"] = 72.8697

    print("[SOS DATA]", sos_data)

    location = sos_data["location"]
    severity = sos_data["severity"]
    people = sos_data["people"]
    urgency = sos_data["urgency"]

    # VERIFICATION AGENT
    print("\n[VERIFICATION AGENT] Checking emergency validity...")

    verified, verify_msg = verify_emergency(
        location,
        severity,
        sos_data["lat"],
        sos_data["lon"]
    )

    if not verified:
        return {
            "status": "manual_review",
            "reason": verify_msg,
            "sos_data": sos_data
        }

    print("[VERIFICATION RESULT]", verify_msg)

    # PRIORITY AGENT
    print("\n[PRIORITY AGENT] Calculating priority...")
    priority = get_priority(people, urgency)

    print("[PRIORITY RESULT]", priority)

    # ALERT AGENT
    print("\n[ALERT AGENT] Checking blocked routes...")
    blocked_roads = check_alerts()

    print("[BLOCKED ROADS]", blocked_roads)

    # ROUTING AGENT
    print("\n[ROUTING AGENT] Finding safest route...")
    route = get_route(location, blocked_roads)

    print("[ROUTE]", route)

    # RESOURCE AGENT
    print("\n[RESOURCE AGENT] Finding responder...")
    resource = get_resource()

    print("[RESOURCE ASSIGNED]", resource)

    # COMMUNICATION AGENT
    print("\n[COMMUNICATION AGENT] Sending dispatch notification...")
    notification = send_notification(resource, route, priority["priority"])

    print("[DISPATCH COMPLETE]")

    return {
        "status": "active_response",
        "sos_data": sos_data,
        "verification": verify_msg,
        "priority": priority,
        "route": route,
        "resource": resource,
        "notification": notification
    }


# =========================
# SMS ENTRY PIPELINE
# =========================

def sms_orchestrator():

    print("\n📩 Listening for incoming SMS...")

    # 1️⃣ Receive SMS
    sms_data = receive_sms()

    if not sms_data:
        print("No SMS received")
        return

    message = sms_data["message"]
    sender_ip = sms_data["ip"]

    print(f"\n📨 SMS RECEIVED: {message}")

    # 2️⃣ Get location from IP
    lat, lon = get_location_from_ip(sender_ip)

    print(f"\n📍 IP LOCATION: {lat}, {lon}")

    # 3️⃣ Merge SMS + location
    merged_data = merge_sms_ip(message, lat, lon)

    # 4️⃣ Route SOS message
    routed_message = route_sos(merged_data)

    # 5️⃣ Run AI agents
    result = run_agents(routed_message, lat, lon)

    print("\n🚨 FINAL RESPONSE")
    print(result)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    sms_orchestrator()