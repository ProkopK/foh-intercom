# Hardware Overview

## Parts List
- 1x Raspberry Pi 4B (with PoE HAT)
- 3x Push Buttons (with integrated LED or separate LED)
- 3x 220Ω resistors (for button LEDs)
- 1x RGB LED (common cathode or anode)
- 3x 220Ω resistors (for RGB LED)
- 1x Headset with microphone (future)
- 1x Ethernet switch
- 1x Fritzbox 7270 v3
- Jumper wires, breadboard or PCB

## Wiring Diagram
- Connect each button to a GPIO pin and ground
- Connect each button LED to a GPIO pin (with resistor) and ground
- Connect RGB LED to 3 GPIO pins (with resistors) and ground
- (Future) Connect headset via USB or audio jack

See [Adafruit Pi GPIO guide](https://learn.adafruit.com/raspberry-pi-gpio-pins) for pinout.

## Example GPIO Pin Assignment
- Button 1: GPIO 17
- Button 2: GPIO 27
- Button 3: GPIO 22
- Button LEDs: GPIO 5, 6, 13
- RGB LED: GPIO 18 (R), 23 (G), 24 (B)

Adjust as needed for your setup.
