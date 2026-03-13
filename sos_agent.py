import json
import re
from langdetect import detect


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


def extract_people_count(message):
    numbers = re.findall(r'\d+', message)
    if numbers:
        return int(numbers[0])
    return 1


def detect_severity(message):

    keywords_high = [
        "flood", "pani", "paani", "baadh", "flooding",
        "trapped", "phas", "atke", "help fast"
    ]

    message = message.lower()

    for word in keywords_high:
        if word in message:
            return 8

    return 4


def process_sos(raw_message):

    print("\n[SOS AGENT] Received message:")
    print(raw_message)

    language = detect_language(raw_message)

    print(f"[SOS AGENT] Detected language: {language}")

    people = extract_people_count(raw_message)

    severity = detect_severity(raw_message)

    # Very simple location extraction (demo version)
    location_keywords = ["andheri", "bandra", "kurla", "dadar", "station"]

    location_found = "unknown"

    for word in location_keywords:
        if word in raw_message.lower():
            location_found = word.title()
            break

    sos_data = {
        "location": location_found,
        "people": people,
        "severity": severity,
        "urgency": "high" if severity >= 7 else "medium",
        "need": "Flood",
        "language": language
    }

    print("[SOS AGENT] Parsed SOS data:", sos_data)

    return sos_data