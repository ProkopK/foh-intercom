import sys
import logging
import time
import signal
import paho.mqtt.client as mqtt
from config import load_config
from gpio_control import GPIOController
from mqtt_client import MQTTHandler
import threading

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load configuration
config = load_config()

HEARTBEAT_TOPIC = 'intercom/heartbeat'
STATUS_TOPIC = 'intercom/system_status'
BUTTON_TOPIC = 'intercom/buttons'
HEARTBEAT_INTERVAL = config['HEARTBEAT_INTERVAL']

# Setup GPIO controller
gpio = GPIOController(
    button_pins=config['BUTTON_PINS'],
    led_pins=config['LED_PINS'],
    rgb_pins=config['RGB_PINS']
)

# Setup MQTT handler
mqtt_handler = MQTTHandler(
    broker=config['MQTT_BROKER'],
    port=config['MQTT_PORT'],
    button_topic=BUTTON_TOPIC,
    status_topic=STATUS_TOPIC
)

# --- Main application logic ---
def handle_button_event(station: str, button_idx: int):
    """Handle a button event from another station."""
    now = time.time()
    if station == config['STATION_NAME']:
        return
    # Protect shared state with lock
    with gpio.led_lock:
        if gpio.led_blink_end[button_idx] > now:
            gpio.led_blink_end[button_idx] = 0
            gpio.respond_led(button_idx, config['RESPOND_DURATION'])
        else:
            gpio.blink_led(button_idx, config['BLINK_DURATION'])

def check_network() -> bool:
    # Simple broker check using MQTT connect
    try:
        client = mqtt.Client()
        client.connect(config['MQTT_BROKER'], config['MQTT_PORT'], 2)
        client.disconnect()
        return True
    except Exception as e:
        logging.warning(f"Network check failed: {e}")
        return False

def cleanup(signum=None, frame=None):
    logging.info("Cleaning up GPIO and exiting...")
    gpio.cleanup()
    sys.exit(0)

def send_heartbeat_loop():
    """Send periodic heartbeat messages to indicate station is online."""
    index = 0
    while True:
        try:
            payload = f"{config['STATION_NAME']}:{index}"
            mqtt_handler.client.publish(HEARTBEAT_TOPIC, payload)
            index += 1
            logging.debug(f"Sent heartbeat: {payload}")
        except Exception as e:
            logging.error(f"Failed to send heartbeat: {e}")
        time.sleep(HEARTBEAT_INTERVAL)

# Register cleanup function for graceful shutdown
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# Register event handler
mqtt_handler.on_button_event = handle_button_event
mqtt_handler.connect()

# Start heartbeat sender thread
heartbeat_thread = threading.Thread(target=send_heartbeat_loop, daemon=True)
heartbeat_thread.start()

def main_loop():
    while True:
        # Network/system status LED
        if not check_network():
            gpio.set_rgb(1, 0, 0)  # Red: No broker
        elif mqtt_handler.system_status == 'all_online':
            gpio.set_rgb(0, 1, 0)  # Green: All online
        elif mqtt_handler.system_status.startswith('missing:'):
            gpio.set_rgb(1, 1, 0)  # Yellow: Some missing
        else:
            gpio.set_rgb(0, 0, 1)  # Blue: Unknown
        # Button check with debounce
        for i, pin in enumerate(config['BUTTON_PINS']):
            state = gpio.read_button(i)
            now = time.time()
            if state == 0 and gpio.last_button[i] == 1 and (now - gpio.last_press_time[i]) > config['DEBOUNCE_TIME']:
                # Button pressed
                mqtt_handler.send_button_event(config['STATION_NAME'], i)
                gpio.blink_led(i, config['BLINK_DURATION'])
                gpio.last_press_time[i] = now
            gpio.last_button[i] = state
        time.sleep(0.05)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt received. Exiting cleanly.")
        cleanup()
    except Exception as e:
        logging.critical(f"Unhandled exception in main loop: {e}", exc_info=True)
        cleanup()
