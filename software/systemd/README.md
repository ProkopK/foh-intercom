# FOH Intercom systemd Services

## Main Intercom Service
This service runs the main button/LED station logic on each Pi.

**File:** `intercom.service`

```
[Unit]
Description=FOH Intercom Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/foh-intercom/software/main.py
WorkingDirectory=/home/pi/foh-intercom/software/
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Enable and start with:
```bash
sudo cp systemd/intercom.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable intercom.service
sudo systemctl start intercom.service
```

---

## System Status Broker Service
This service runs the status broker to monitor all stations and publish system status.

**File:** `system_status_broker.service`

```
[Unit]
Description=FOH Intercom System Status Broker
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/foh-intercom/software/system_status_broker.py
WorkingDirectory=/home/pi/foh-intercom/software/
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Enable and start with:
```bash
sudo cp systemd/system_status_broker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable system_status_broker.service
sudo systemctl start system_status_broker.service
```
