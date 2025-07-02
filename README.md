# FOH Intercom

A simple MQTT-powered intercom system for theater, using Raspberry Pis with 3 LED buttons each.

## Features

- Button presses are sent via MQTT to all stations.
- Corresponding LEDs light up on all other stations.
- Built for easy setup and update via Git.
- Designed for future extension (e.g., headset audio communication).

---

## Hardware

- Raspberry Pi (any model with GPIO and network)
- 3x LED pushbuttons, wired to GPIO (edit pins in script if needed)
- Resistors as required
- Breadboard or HAT for connections

---

## Setup Instructions

### 1. Clone the Repository

On each Pi:
```sh
git clone https://github.com/ProkopK/foh-intercom.git
cd foh-intercom/intercom
```

---

### 2. Install Python Dependencies

```sh
pip install -r requirements.txt
```

---

### 3. Install and Configure MQTT Broker (Mosquitto)

You can run the broker on any Pi or server on your LAN.

#### Install Mosquitto Broker
```sh
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

#### Secure the Broker

- **Username/Password:**  
  ```sh
  sudo mosquitto_passwd -c /etc/mosquitto/passwd myuser
  ```
  (Enter your password when prompted.)

- **Configure Mosquitto:**  
  Edit `/etc/mosquitto/conf.d/default.conf` or `/etc/mosquitto/mosquitto.conf` to add:
  ```
  allow_anonymous false
  password_file /etc/mosquitto/passwd
  ```
  Restart Mosquitto:
  ```sh
  sudo systemctl restart mosquitto
  ```

- **(Optional: TLS/ACL):**  
  For advanced security (encrypted connections, topic access control), see Mosquitto docs:  
  [https://mosquitto.org/man/mosquitto-conf-5.html](https://mosquitto.org/man/mosquitto-conf-5.html)

---

### 4. Environment Variables for Configuration

Set configuration easily for each Pi using environment variables.

#### Temporary (for one terminal session):

```sh
export INTERCOM_STATION=foh
export INTERCOM_BROKER=192.168.178.42
python3 foh_intercom_mqtt.py
```

#### Permanent (every boot/user session):

Add to `~/.bashrc`:
```sh
echo "export INTERCOM_STATION=foh" >> ~/.bashrc
echo "export INTERCOM_BROKER=192.168.178.42" >> ~/.bashrc
source ~/.bashrc
```

#### (Optional) Use an environment file with systemd, e.g., `/etc/foh-intercom.env`:
```
INTERCOM_STATION=foh
INTERCOM_BROKER=192.168.178.42
```

---

### 5. Running the Intercom

```sh
python3 foh_intercom_mqtt.py
```

- Set the station name and broker address per Pi as above.
- Press a button to send status to all stations.

---

### 6. Enable Auto-Start at Boot (systemd)

#### Create a systemd service:

```sh
sudo nano /etc/systemd/system/foh-intercom.service
```

Paste:
```
[Unit]
Description=FOH Intercom MQTT Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/foh-intercom/intercom
Environment=INTERCOM_STATION=foh
Environment=INTERCOM_BROKER=192.168.178.42
ExecStart=/usr/bin/python3 /home/pi/foh-intercom/intercom/foh_intercom_mqtt.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
- Adjust paths and station/broker names as needed.

#### Enable and Start Service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable foh-intercom.service
sudo systemctl start foh-intercom.service
```

Check status/logs:
```sh
sudo systemctl status foh-intercom.service
journalctl -u foh-intercom.service
```

---

### 7. Updating

Pull updates on each Pi:

```sh
git pull origin main
```

- Use environment variables or systemd as above for config.
- For multiple Pis, consider using Ansible or a deployment script for automation.

---

### 8. Troubleshooting

- Ensure all Pis are on the same network (via Fritz!Box or similar router).
- Check that each Pi has the correct `INTERCOM_STATION` and `INTERCOM_BROKER` settings.
- If MQTT communication fails, verify broker is running and accessible (`mosquitto_sub -v -t "#" -h BROKER_IP -u myuser -P password`).

---

## Next Steps

- Add headset/audio features in the future.
- Improve UI and LED feedback as needed.
- Secure MQTT further for production (see above).

---

## References

- [Mosquitto Documentation](https://mosquitto.org/man/mosquitto-conf-5.html)
- [gpiozero Library](https://gpiozero.readthedocs.io/en/stable/)
- [paho-mqtt Python Client](https://pypi.org/project/paho-mqtt/)
