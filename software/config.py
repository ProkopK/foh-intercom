"""
Configuration and environment variable parsing for FOH Intercom.
"""
import os
from dotenv import load_dotenv
from typing import List, Dict

def parse_pin_list(env_var: str, default: List[int]) -> List[int]:
    val = os.getenv(env_var)
    if val:
        return [int(x) for x in val.split(",")]
    return default

def load_config() -> Dict:
    """Load all configuration from environment variables or .env file."""
    load_dotenv()
    config = {
        'BUTTON_PINS': parse_pin_list("BUTTON_PINS", [17, 27, 22]),
        'LED_PINS': parse_pin_list("LED_PINS", [5, 6, 26]),
        'RGB_PINS': {
            'R': int(os.getenv("RGB_PIN_R", 23)),
            'G': int(os.getenv("RGB_PIN_G", 24)),
            'B': int(os.getenv("RGB_PIN_B", 25)),
        },
        'BLINK_DURATION': int(os.getenv("BLINK_DURATION", 20)),
        'RESPOND_DURATION': int(os.getenv("RESPOND_DURATION", 5)),
        'DEBOUNCE_TIME': float(os.getenv("DEBOUNCE_TIME", 0.2)),
        'STATION_NAME': os.getenv("INTERCOM_STATION", "foh"),
        'MQTT_BROKER': os.getenv("INTERCOM_BROKER", os.getenv("MQTT_BROKER", "192.168.178.11")),
        'MQTT_PORT': int(os.getenv("MQTT_PORT", 1883)),
        'MQTT_TOPIC': os.getenv("MQTT_TOPIC", "intercom/buttons"),
        'STATUS_TOPIC': os.getenv("STATUS_TOPIC", "intercom/system_status"),
    }
    return config
