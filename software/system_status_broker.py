# This script can be run on the broker (FOH Pi) to monitor all station connections and publish system status.
# It requires paho-mqtt and should be started as a background process or service.

import time
import paho.mqtt.client as mqtt

MQTT_BROKER = 'localhost'  # On FOH Pi
MQTT_PORT = 1883
MQTT_TOPIC = 'intercom/buttons'
STATUS_TOPIC = 'intercom/system_status'
STATIONS = ['foh', 'stage_left', 'stage_right']
TIMEOUT = 30  # seconds

last_seen = {station: 0 for station in STATIONS}

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        parts = payload.split(':')
        if len(parts) == 3:
            station, btn_idx, ts = parts
            if station in last_seen:
                last_seen[station] = time.time()
    except Exception:
        pass

def publish_status(client):
    now = time.time()
    missing = [s for s, t in last_seen.items() if now - t > TIMEOUT]
    if not missing:
        status = 'all_online'
    else:
        status = 'missing:' + ','.join(missing)
    client.publish(STATUS_TOPIC, status)

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

try:
    while True:
        publish_status(client)
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
