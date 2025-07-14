# FOH Intercom Installation & Setup (Step-by-Step)

## 1. Prepare Hardware
- Assemble hardware as per diagrams in `hardware/`
- Connect all Raspberry Pis to your network via Ethernet (PoE recommended)

## 2. Flash Raspberry Pi OS
- Download and flash Raspberry Pi OS (Lite recommended) to each Pi
- Boot each Pi and connect via SSH

## 2.1 Set a Static IP Address (Required for FOH Intercom, optional but recommended for all Pis)
To ensure reliable communication, assign a static IP address to each Raspberry Pi:

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses 192.168.178.11/24
sudo nmcli con mod "Wired connection 1" ipv4.gateway 192.168.178.1
sudo nmcli con mod "Wired connection 1" ipv4.dns "192.168.178.1 8.8.8.8"
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"
```
Repeat for each Pi, changing the IP address (e.g., 192.168.178.12)

Verify the IP address with:
```bash
hostname -I
```

## 3. Install Required Software on Each Pi
On each Pi, run:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip
sudo apt install -y git
```
Check if everything is installed correctly:
```bash
python --version
pip --version
git --version
```

### 3.1 Set Up the FOH Station as MQTT Broker
Only on the FOH Pi:

```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
The broker will now run on the FOH Pi. Find its IP address with:
```bash
hostname -I
```
Use this IP for `MQTT_BROKER` later in your config.

## 4. Clone the Repository on All Pis
```bash
git clone https://github.com/ProkopK/foh-intercom.git
cd foh-intercom/software
```

## 5. Install Python Dependencies and Set Environment Variables
On each Pi run the following commands:
```bash
python3 -m venv ~/foh-intercom/venv
echo "source ~/foh-intercom/venv/bin/activate" >> ~/.bashrc
source ~/.bashrc
pip install -r requirements.txt
```
Set up environment variables for each Pi, change the values. Use the IP address of the FOH Pi as `MQTT_BROKER`, as `STATION_NAME` use `foh` for the FOH Pi and `stage_left` or `stage_right` for the stage Pi:
```bash
touch .env
echo "export STATION_NAME=foh" >> .env
echo "export MQTT_BROKER=192.168.178.11" >> .env
echo "export STATIONS=foh,stage_left,stage_right" >> .env
echo "export MQTT_PORT=1883" >> .env
```

## 6. Enable Auto-Start with systemd
For each Pi, copy the service file and enable it:
```bash
sudo cp systemd/intercom.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable intercom.service
sudo systemctl start intercom.service
```
For the FOH Pi, set up the system status broker service:
```bash
sudo cp systemd/system_status_broker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable system_status_broker.service
sudo systemctl start system_status_broker.service
```

---

## 7. Updating
To update the software on all Pis:
```bash
git pull
sudo systemctl restart intercom.service
sudo systemctl restart system_status_broker.service
```

---

## Code Structure (Modular Python)
- `main.py`: Main entry point for each station. Loads config, sets up GPIO and MQTT, runs the main loop.
- `gpio_control.py`: GPIO setup and all LED/button logic, thread-safe.
- `mqtt_client.py`: MQTT connection, message handling, and reconnect logic.
- `config.py`: Loads configuration from environment variables or `.env` file.
- `system_status_broker.py`: Monitors all stations and publishes system status (run on FOH Pi).

## Advanced .env Configuration (Optional)
You can use the `.env` file in the `software/` directory to override any environment variable. Example:
```
STATION_NAME=foh
MQTT_BROKER=192.168.178.11
MQTT_PORT=1883
STATIONS=foh,stage_left,stage_right
DEBOUNCE_TIME=0.2
RESPOND_DURATION=5
BLINK_DURATION=20
TIMEOUT=15

BUTTON_PIN_Green=17
BUTTON_PIN_Orange=27
BUTTON_PIN_Red=22
LED_PIN_Green=5
LED_PIN_Orange=6
LED_PIN_Red=26
RGB_PIN_R=23
RGB_PIN_G=24
RGB_PIN_B=25
```

Any variable not set in `.env` will fall back to the default in this example code.

---
