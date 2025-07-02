import RPi.GPIO as GPIO
import time
import requests
import paho.mqtt.client as mqtt
import os
import threading

# GPIO pin assignments
BUTTON_PINS = [17, 27, 22]
LED_PINS = [5, 6, 26]
RGB_PINS = {'R': 23, 'G': 24, 'B': 25}

# Station configuration
os.getenv("INTERCOM_STATION", default="foh")

# MQTT settings
MQTT_BROKER = os.getenv("INTERCOM_BROKER", default="192.168.178.21")
MQTT_PORT = 1883
MQTT_TOPIC = 'intercom/buttons'
STATUS_TOPIC = 'intercom/system_status'

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in BUTTON_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
for pin in RGB_PINS.values():
    GPIO.setup(pin, GPIO.OUT)

# Helper: Set RGB LED
def set_rgb(r, g, b):
    GPIO.output(RGB_PINS['R'], r)
    GPIO.output(RGB_PINS['G'], g)
    GPIO.output(RGB_PINS['B'], b)

# Helper: Network status (local broker check)
def check_network():
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 2)
        client.disconnect()
        return True
    except:
        return False


led_blink_end = [0, 0, 0]
led_respond_end = [0, 0, 0]

def blink_led(idx, duration=20):
    def _blink():
        end_time = time.time() + duration
        led_blink_end[idx] = end_time
        while time.time() < end_time and led_blink_end[idx] == end_time:
            GPIO.output(LED_PINS[idx], 1)
            time.sleep(0.5)
            GPIO.output(LED_PINS[idx], 0)
            time.sleep(0.5)
        GPIO.output(LED_PINS[idx], 0)
    t = threading.Thread(target=_blink)
    t.daemon = True
    t.start()

def respond_led(idx, duration=5):
    def _respond():
        GPIO.output(LED_PINS[idx], 1)
        time.sleep(duration)
        GPIO.output(LED_PINS[idx], 0)
    led_respond_end[idx] = time.time() + duration
    t = threading.Thread(target=_respond)
    t.daemon = True
    t.start()

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        # Format: station:button_idx:timestamp
        parts = payload.split(':')
        if len(parts) == 3:
            station, btn_idx, ts = parts
            btn_idx = int(btn_idx)
            ts = float(ts)
            handle_button_event(station, btn_idx, ts)
    except Exception as e:
        print(f"MQTT message error: {e}")

def send_mqtt_message(station, button_idx):
    try:
        payload = f"{station}:{button_idx}:{time.time()}"
        mqtt_client.publish(MQTT_TOPIC, payload)
    except Exception as e:
        print(f"MQTT send error: {e}")

def handle_button_event(station, button_idx, ts):
    now = time.time()
    if station == STATION_NAME:
        return
    # If we are blinking, and someone else presses the same button, show respond
    if led_blink_end[button_idx] > now:
        led_blink_end[button_idx] = 0  # Stop blinking
        respond_led(button_idx)
    else:
        # Start blinking for 20s
        blink_led(button_idx, 20)

# Persistent MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

system_status = 'unknown'
def on_status(client, userdata, msg):
    global system_status
    try:
        system_status = msg.payload.decode()
    except Exception:
        system_status = 'unknown'

mqtt_client.message_callback_add(STATUS_TOPIC, on_status)
mqtt_client.subscribe(STATUS_TOPIC)

try:
    last_button = [1, 1, 1]
    while True:
        # Network/system status LED
        if not check_network():
            set_rgb(1, 0, 0)  # Red: No broker
        elif system_status == 'all_online':
            set_rgb(0, 1, 0)  # Green: All online
        elif system_status.startswith('missing:'):
            set_rgb(1, 1, 0)  # Yellow: Some missing
        else:
            set_rgb(0, 0, 1)  # Blue: Unknown
        # Button check
        for i, pin in enumerate(BUTTON_PINS):
            state = GPIO.input(pin)
            if state == 0 and last_button[i] == 1:
                # Button pressed
                send_mqtt_message(STATION_NAME, i)
                blink_led(i, 20)
            last_button[i] = state
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
