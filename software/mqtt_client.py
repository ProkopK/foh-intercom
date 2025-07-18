"""
MQTT connection, message handling, and status logic for FOH Intercom.
"""
import paho.mqtt.client as mqtt # type: ignore
import time
import logging
from typing import Callable

class MQTTHandler:
    def __init__(self, broker: str, port: int, button_topic: str, status_topic: str):
        self.broker = broker
        self.port = port
        self.button_topic = button_topic
        self.status_topic = status_topic
        self.client = mqtt.Client()
        self.system_status = 'unknown'
        self.on_button_event: Callable = lambda *args, **kwargs: None
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.message_callback_add(self.status_topic, self._on_status)

    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.button_topic)
        client.subscribe(self.status_topic)
        logging.info(f"Connected to MQTT broker with result code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            parts = payload.split(':')
            if len(parts) == 2:
                station, btn_idx = parts
                self.on_button_event(station, int(btn_idx))
            else:
                logging.warning(f"Invalid message format: {payload}")
        except ValueError as e:
            logging.error(f"Error parsing MQTT message: {e}")
        except Exception as e:
            logging.error(f"MQTT message error: {e}")

    def _on_status(self, client, userdata, msg):
        try:
            self.system_status = msg.payload.decode()
        except Exception as e:
            logging.error(f"Status message error: {e}")
            self.system_status = 'unknown'

    def send_button_event(self, station: str, button_idx: int):
        """
        Send a button event to the MQTT broker.
        Args:
            station (str): The name of the station sending the event.
            button_idx (int): The index of the button pressed.
        """
        try:
            payload = f"{station}:{button_idx}"
            self.client.publish(self.button_topic, payload)
            logging.info(f"Sent MQTT message: {payload}")
        except Exception as e:
            logging.error(f"MQTT send error: {e}")

    def connect(self):
        """
        Connect to the MQTT broker and start the loop. Handles initial connection and auto-reconnect on disconnect.
        """
        self.client.on_disconnect = self._on_disconnect
        while True:
            try:
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_start()
                break
            except Exception as e:
                logging.error(f"MQTT connection failed: {e}, retrying in 5s...")
                time.sleep(5)

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.warning("MQTT disconnected unexpectedly. Attempting to reconnect...")
            self._reconnect()

    def _reconnect(self):
        while True:
            try:
                self.client.reconnect()
                logging.info("MQTT reconnected successfully.")
                break
            except Exception as e:
                logging.error(f"MQTT reconnect failed: {e}, retrying in 5s...")
                time.sleep(5)
