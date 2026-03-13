"""
Speech SOS Utility

This module receives speech-to-text output from the frontend
(React Native mobile app) and prepares it for the SOS agent pipeline.
The mobile app handles microphone recording and speech recognition.
"""

def get_voice_message(recognized_text: str):
    """
    Accepts speech-to-text result from the mobile frontend.

    Args:
        recognized_text (str): Text converted from speech on the mobile device

    Returns:
        str | None: Cleaned message or None if empty
    """

    if not recognized_text:
        print("[SPEECH MODULE] No speech text received.")
        return None

    message = recognized_text.strip()

    if message == "":
        print("[SPEECH MODULE] Empty message after processing.")
        return None

    print(f"[SPEECH MODULE] Message received from frontend: {message}")

    return message


# Optional: local test
if __name__ == "__main__":
    sample = "Flood in Andheri East near station 3 people trapped"
    result = get_voice_message(sample)
    print("Processed message:", result)