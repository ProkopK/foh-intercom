import paho.mqtt.client as mqtt
from gpiozero import Button, LED
from signal import pause
import os

# --- CONFIGURATION ---
# You can overwrite these with environment variables for each Pi
STATION = os.getenv("INTERCOM_STATION", "station1")
BROKER = os.getenv("INTERCOM_BROKER", "192.168.178.42")
BUTTON_PINS = [17, 27, 22]
LED_PINS = [5, 6, 13]

# --- Setup GPIO ---
buttons = [Button(pin) for pin in BUTTON_PINS]
leds = [LED(pin) for pin in LED_PINS]

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code", rc)
    client.subscribe("fohintercom/#")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    sender, btn_idx = payload.split(',')
    btn_idx = int(btn_idx)
    print(f"Received from {sender}: button {btn_idx}")
    # Only light LEDs for remote stations
    if sender != STATION:
        leds[btn_idx].on()
        from threading import Timer
        Timer(2, leds[btn_idx].off).start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)

def make_press_handler(idx):
    def handler():
        print(f"Button {idx} pressed")
        client.publish("fohintercom/" + STATION, f"{STATION},{idx}")
        leds[idx].on()
        from threading import Timer
        Timer(2, leds[idx].off).start()
    return handler

for idx, btn in enumerate(buttons):
    btn.when_pressed = make_press_handler(idx)

import threading
threading.Thread(target=client.loop_forever, daemon=True).start()
pause()
