# FOH Intercom Installation & Setup (Step-by-Step)

## 1. Prepare Hardware
- Assemble hardware as per diagrams in `hardware/`
- Connect all Raspberry Pis to your network via Ethernet (PoE recommended)

## 2. Flash Raspberry Pi OS
- Download and flash Raspberry Pi OS (Lite recommended) to each Pi
- Boot each Pi and set up SSH/network as needed

## 3. Install Required Software on Each Pi
On each Pi, run:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip
sudo apt install -y git
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
cd foh-intercom/intercom
```

## 5. Install Python Dependencies and Set Environment Variables
On each Pi, run:
```bash
pip install -r requirements.txt
echo "export INTERCOM_STATION=$Station Name$" >> ~/.bashrc
echo "export MQTT_BROKER=$IP-Adress of MQTT Broker$" >> ~/.bashrc
source ~/.bashrc
```
Set the Station Name to a unique name for each station: 'foh', 'stage_left', or 'stage_right'

## 6. Enable Auto-Start with systemd
```bash
sudo cp systemd/intercom.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable intercom.service
sudo systemctl start intercom.service
```

## 7. Updating
To update the software on all Pis:
```bash
git pull
sudo systemctl restart intercom.service
```
