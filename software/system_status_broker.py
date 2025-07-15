"""
# system_status_broker.py
This script monitors the status of multiple stations in an intercom system using MQTT. It is ment to run continuously on the FOH station.
It listens for heartbeat messages from each station and publishes the overall system status.
"""
import os
import time
import logging
import paho.mqtt.client as mqtt # type: ignore
from config import load_config

config = load_config()
MQTT_BROKER = config['MQTT_BROKER'] 
MQTT_PORT = config['MQTT_PORT']
STATUS_TOPIC = 'intercom/system_status'
HEARTBEAT_TOPIC = 'intercom/heartbeat'
STATIONS = config['STATIONS']
TIMEOUT = 15

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

last_seen = {station: 0 for station in STATIONS}

def on_heartbeat(client, userdata, msg):
    """Handle incoming heartbeat messages and update last seen times."""
    try:
        payload = msg.payload.decode()
        parts = payload.split(':')
        if len(parts) == 2:
            station, index = parts
            if station in last_seen:
                last_seen[station] = time.time()
                logging.debug(f"Heartbeat received from {station} at index {index}")
        else:
            logging.warning(f"Invalid heartbeat format: {payload}")
    except Exception as e:
        logging.error(f"Error in on_heartbeat: {e}")

def publish_status(client):
    """Publish system status based on which stations are online."""
    now = time.time()
    missing = [s for s, t in last_seen.items() if now - t > TIMEOUT]
    if not missing:
        status = 'all_online'
    else:
        status = 'missing:' + ','.join(missing)
    client.publish(STATUS_TOPIC, status)
    logging.debug(f"Published status: {status}")

def main():
    client = mqtt.Client()
    client.message_callback_add(HEARTBEAT_TOPIC, on_heartbeat)
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.subscribe(HEARTBEAT_TOPIC)
            client.loop_start()
            logging.info("System status broker started.")
            try:
                while True:
                    publish_status(client)
                    time.sleep(5)
            except KeyboardInterrupt:
                logging.info("System status broker stopped by user.")
                break
            finally:
                client.loop_stop()
                client.disconnect()
        except Exception as e:
            logging.error(f"MQTT connection error: {e}. Retrying in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()
