# Hardware Overview

## Parts List
- 3x Raspberry Pi 4B (with PoE HAT)
- 9x Push Buttons (with integrated LED or separate LED)
- 9x 220Ω resistors (for button LEDs)
- 3x RGB LED (common cathode or anode)
- 9x 220Ω resistors (for RGB LED)
- 0x Headset with microphone (future)
- 1x Ethernet switch
- 1x Fritzbox 7270 v3
- Jumper wires, breadboard or PCB

## Wiring Diagram
- Connect each button to a GPIO pin and ground
- Connect each button LED to a GPIO pin (with resistor) and ground
- Connect RGB LED to 3 GPIO pins (with resistors) and ground
- (Future) Connect headset via USB or audio jack

## GPIO Pin Assignment
- Button Green (NC): GPIO 17
- Button Green (C): Ground
- Button LED Green (+): GPIO 5
- Button LED Green (-): Ground

- Button Orange (NC): GPIO 27
- Button Orange (C): Ground
- Button LED Orange (+): GPIO 6
- Button LED Orange (-): Ground

- Button Red (NC): GPIO 22
- Button Red (C): Ground
- Button LED Red (+): GPIO 26
- Button LED Red (-): Ground

- RGB LED: GPIO 23 (R), 24 (G), 25 (B)
- RGB LED Common Cathode: Ground

## Drawings
- TODO