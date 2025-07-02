# FOH Intercom

A simple MQTT-powered intercom system for theater, using Raspberry Pis with 3 LED buttons each.

## Features

- Button presses are sent via MQTT to all stations.
- Corresponding LEDs light up on all other stations.
- Built for easy setup and update via Git.

## Getting Started

### Hardware

- Raspberry Pi (any model with GPIO and network)
- 3x LED pushbuttons, wired to GPIO (edit pins in script if needed)

### Setup

1. Clone this repo on each Pi:

   ```sh
   git clone https://github.com/ProkopK/foh-intercom.git
   cd foh-intercom/intercom
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up your station name and broker address (optional):

   ```sh
   export INTERCOM_STATION=stage
   export INTERCOM_BROKER=192.168.178.42
   ```

   (Or edit the script to hard-code these.)

4. Run the script:

   ```sh
   python3 foh_intercom_mqtt.py
   ```

5. Press a button to send status to all stations!

### Updating

- Use Git to pull updates on each Pi:

  ```sh
  git pull origin main
  ```

- You can also use Ansible or simple deployment scripts for automation as the network grows.

### Next Steps

- Add headset/audio features later.
- Secure your MQTT broker for production use.
