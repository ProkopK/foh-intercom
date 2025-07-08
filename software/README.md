# FOH Intercom Installation & Setup (Step-by-Step)

## 1. Prepare Hardware
- Assemble hardware as per diagrams in `hardware/`
- Connect all Raspberry Pis to your network via Ethernet (PoE recommended)

## 2. Flash Raspberry Pi OS
- Download and flash Raspberry Pi OS (Lite recommended) to each Pi
- Boot each Pi and set up SSH/network as needed

## 2.1 Set a Static IP Address (Required for FOH Intercom, optional but recommended for all Pis)
To ensure reliable communication, assign a static IP address to each Raspberry Pi:

1. On each Pi, edit the DHCP client configuration:
   ```bash
   sudo nano /etc/dhcpcd.conf
   ```
2. Scroll to the end of the file and add (replace values as needed for your network):
   ```
   interface eth0
   static ip_address=192.168.178.11/24     # Choose a unique IP for each Pi
   static routers=192.168.178.1            # Your network gateway
   static domain_name_servers=192.168.178.1 8.8.8.8
   ```
3. Save and exit (Ctrl+O, Enter, Ctrl+X).
4. Reboot the Pi:
   ```bash
   sudo reboot
   ```
5. Repeat for each Pi, assigning a different static IP address to each one.

After reboot, verify the IP address with:
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
On each Pi run the following commands, replacing `>>Station Name<<` with the appropriate station name (e.g., `foh`, `stage_left`, or `stage_right`) and `>>IP-Adress of MQTT Broker xx.xx.xx.xx<<` with the IP address of the FOH Pi:
```bash
python -m venv ~/foh-intercom/venv
echo "source ~/foh-intercom/venv/bin/activate" >> ~/.bashrc
echo "export INTERCOM_STATION=>>Station Name<<" >> ~/.bashrc
echo "export MQTT_BROKER=>>IP-Adress of MQTT Broker xx.xx.xx.xx<<" >> ~/.bashrc
source ~/.bashrc
pip install -r requirements.txt
```

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
