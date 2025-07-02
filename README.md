# Intercom Offenbarung

A networked communication system for theatre FOH and stage, using Raspberry Pi 4B, buttons, LEDs, and headsets.

## Features
- 3-button interface with LED feedback for state communication (e.g., stage free, problem, etc.)
- RGB LED for network/system status
- (Planned) Push-to-talk headset audio
- All devices networked via PoE and managed from a central repository

## Hardware
- Raspberry Pi 4B (with PoE hats)
- 3x Push Buttons (with LEDs or RGB LEDs)
- 1x RGB LED (for status)
- Headset with microphone (future)
- Ethernet switch and Fritzbox 7270 v3

See `hardware/` for wiring diagrams and parts list.

## Software
- Python scripts for button/LED control and network communication
- Systemd service for auto-start
- Update via git pull or script

See `software/` for code and setup instructions.

## Installation & Setup (Step-by-Step)

### 1. Prepare Hardware
- Assemble hardware as per diagrams in `hardware/`
- Connect all Raspberry Pis to your network via Ethernet (PoE recommended)

### 2. Flash Raspberry Pi OS
- Download and flash Raspberry Pi OS (Lite recommended) to each Pi
- Boot each Pi and set up SSH/network as needed

### 3. Set Up the FOH Station as MQTT Broker
On the FOH Pi (or your chosen broker device):

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
The broker will now run on the FOH Pi. Find its IP address with:
```bash
hostname -I
```
Use this IP for `MQTT_BROKER` in your code/config.

### 4. Clone the Repository on All Pis
```bash
git clone <your-repo-url>
cd Intercom\ Offenbarung/software
```

### 5. Install Python Requirements
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requirements.txt
```

### 6. Configure Each Station
- Edit `software/station_config.py` and set `STATION_NAME` to one of: `foh`, `stage_left`, or `stage_right` (unique per Pi)
- Edit `main.py` and set `MQTT_BROKER` to the IP address of your FOH Pi

### 7. (Optional) Enable Auto-Start with systemd
On each Pi:
```bash
sudo cp systemd/intercom.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable intercom.service
sudo systemctl start intercom.service
```

### 8. Updating
To update the software on all Pis:
```bash
git pull
sudo systemctl restart intercom.service
```

---

For details, see the subfolders and documentation files.
