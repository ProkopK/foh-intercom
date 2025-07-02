# Intercom Offenbarung

A networked communication system for theatre FOH and stage, using Raspberry Pi 4B, buttons, LEDs, and headsets.

## Features
- 3-button interface with LED feedback for state communication (e.g., stage free, problem, etc.)
- RGB LED for network/system status
- (Planned) Push-to-talk headset audio
- All devices networked via PoE

## Hardware
- Raspberry Pi 4B (with PoE hats)
- LED Push Buttons
- 1x RGB LED (for status)
- Headset with microphone (future)
- Ethernet switch and Fritzbox

See `hardware/` for wiring diagrams and parts list.

## Software
- Python scripts for button/LED control and network communication
- Systemd service for auto-start
- Update via git pull or script

See `software/` for code and setup instructions.