# FOH Intercom

A networked communication system for theatre Front of House (FOH) and stage, using Raspberry Pi 4B, buttons, LEDs, and headsets.


## Features
- 3-button interface with LED feedback for state communication:
  - Button 1: Stage free (green LED)
  - Button 2: Problem/Assistance needed (red LED)
  - Button 3: Custom/Other state (yellow LED)
- RGB LED for network/system status (e.g., connected, error, updating)
- (Planned) Push-to-talk headset audio for direct communication
- All devices networked via Power over Ethernet (PoE) for reliability and easy installation


## Hardware
- Raspberry Pi 4B (with PoE HATs)
- 3x LED Push Buttons (for user input and feedback)
- 1x RGB LED (for system/network status)
- Headset with microphone (planned for future audio features)
- Ethernet switch and Fritzbox (for network connectivity)


See [`hardware/`](hardware/) for wiring diagrams and parts list.


## Software
- Python 3 scripts for button/LED control and network communication
- Systemd service for automatic startup on boot
- Easy updates via `git pull` or update script


See [`software/`](software/) for code and setup instructions.

### Requirements
- Python 3.7 or higher
- See `software/requirements.txt` for required Python packages

### Quick Start
1. Clone this repository to your Raspberry Pi:
   ```bash
   git clone <repo-url>
   ```
2. Install Python dependencies:
   ```bash
   cd software
   pip install -r requirements.txt
   ```
3. Set up the systemd service for auto-start (see `software/systemd/README.md` for details).
4. Connect hardware as shown in the wiring diagrams in `hardware/`.
5. Power up the device via PoE and test button/LED functionality.

### Usage
- Press the buttons to communicate states between FOH and stage. LED feedback will indicate the current state.
- The RGB LED shows system/network status (e.g., green for connected, red for error).

---
For more details, see the documentation in each subfolder.