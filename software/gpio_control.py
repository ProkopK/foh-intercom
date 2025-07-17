"""
GPIO setup and LED/button logic for FOH Intercom.
"""
import RPi.GPIO as GPIO # type: ignore
import threading
import time
from typing import Dict

class GPIOController:
    def __init__(self, button_pins: Dict[int, int], led_pins: Dict[int, int], rgb_pins: Dict[str, int]):
        self.button_pins = button_pins
        self.led_pins = led_pins
        self.rgb_pins = rgb_pins
        self.led_blink_end = [0] * len(led_pins)
        self.led_respond_end = [0] * len(led_pins)
        self.led_lock = threading.Lock()
        self.last_button = [1] * len(button_pins)
        self.last_press_time = [0] * len(button_pins)
        self.last_station = [None] * len(button_pins)
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.button_pins.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in self.led_pins.values():
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.rgb_pins.values():
            GPIO.setup(pin, GPIO.OUT)

    def set_rgb(self, r: int, g: int, b: int):
        GPIO.output(self.rgb_pins['R'], r)
        GPIO.output(self.rgb_pins['G'], g)
        GPIO.output(self.rgb_pins['B'], b)

    def blink_led(self, idx: int, duration: int):
        def _blink():
            end_time = time.time() + duration
            with self.led_lock:
                self.led_blink_end[idx] = end_time
            while time.time() < end_time:
                with self.led_lock:
                    if self.led_blink_end[idx] != end_time:
                        break
                GPIO.output(self.led_pins[idx], 1)
                time.sleep(0.5)
                GPIO.output(self.led_pins[idx], 0)
                time.sleep(0.5)
            GPIO.output(self.led_pins[idx], 0)
        t = threading.Thread(target=_blink)
        t.daemon = True
        t.start()

    def respond_led(self, idx: int, duration: int):
        def _respond():
            end_time = time.time() + duration
            while time.time() < end_time:
                GPIO.output(self.led_pins[idx], 1)
            GPIO.output(self.led_pins[idx], 0)
        t = threading.Thread(target=_respond)
        t.daemon = True
        t.start()

    def stop_led(self, idx: int):
        with self.led_lock:
            self.led_blink_end[idx] = 0
            self.led_respond_end[idx] = 0

    def read_button(self, idx: int) -> int:
        return GPIO.input(self.button_pins[idx])

    def cleanup(self):
        GPIO.cleanup()
