"""
Configuration and environment variable parsing for FOH Intercom.
"""
import os
from dotenv import load_dotenv # type: ignore
from typing import List, Dict

def load_config() -> Dict:
    """Load all configuration from environment variables or .env file."""
    load_dotenv()
    config = {
        'BUTTON_PINS': {
            0: int(os.getenv("BUTTON_PIN_Green", 17)),
            1: int(os.getenv("BUTTON_PIN_Orange", 27)),
            2: int(os.getenv("BUTTON_PIN_Red", 22)),
        },
        'LED_PINS': {
            0: int(os.getenv("LED_PIN_Green", 5)),
            1: int(os.getenv("LED_PIN_Orange", 6)),
            2: int(os.getenv("LED_PIN_Red", 26)),
        },
        'RGB_PINS': {
            'R': int(os.getenv("RGB_PIN_R", 23)),
            'G': int(os.getenv("RGB_PIN_G", 24)),
            'B': int(os.getenv("RGB_PIN_B", 25)),
        },
        'BLINK_DURATION': int(os.getenv("BLINK_DURATION", 20)),
        'RESPOND_DURATION': int(os.getenv("RESPOND_DURATION", 5)),
        'DEBOUNCE_TIME': float(os.getenv("DEBOUNCE_TIME", 0.2)),
        'STATION_NAME': os.getenv("STATION_NAME", "foh"),
        'MQTT_BROKER': os.getenv("MQTT_BROKER", "192.168.178.11"),
        'MQTT_PORT': int(os.getenv("MQTT_PORT", 1883)),
        'STATIONS': os.getenv("STATIONS", "foh,stage_left,stage_right").split(","),
        'TIMEOUT': int(os.getenv("TIMEOUT", 15)),
        'HEARTBEAT_INTERVAL': int(os.getenv("HEARTBEAT_INTERVAL", 10)),
    }
    return config
