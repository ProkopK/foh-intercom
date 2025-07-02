# Software Overview

This folder contains the Python scripts for the Intercom Offenbarung system.

## Structure
- `main.py` — Main script for button/LED control and network communication
- `requirements.txt` — Python dependencies
- `systemd/` — Service files for auto-start

## Setup
1. Install Python 3 (Raspberry Pi OS comes with it)
2. Install requirements: `pip install -r requirements.txt`
3. Run `main.py` to start the system
4. (Optional) Enable systemd service for auto-start

## Updating
To update the software on all Pis:
- Pull the latest code: `git pull`
- Restart the service: `sudo systemctl restart intercom.service`

---

See `main.py` for configuration and usage.
