# Virtual Power Plant (VPP) Blockchain System

This is a comprehensive Virtual Power Plant application designed to track energy metrics (AC/DC power output, battery charge/discharge info) securely using a localized blockchain layer. 

## Features

- **Energy Dashboard**: Real-time energy generation and consumption monitoring.
- **Blockchain Verification**: Transactions (such as peer-to-peer energy trades and system states) are recorded via an internal blockchain mechanism.
- **Hardware Integration**: Integration with external ESP8266 IoT endpoints to get live sensory information.
- **Payment Hub**: View energy bills, generated energy cost splits, and overall power savings.

## File Structure

- `app.py`: Flask entry point for the Web Interface.
- `backend/`: Core service modules, including blockchain algorithms, ESP8266 data aggregators, and system data handling logic.
- `templates/`: HTML frontend components with a premium dynamic design.
- `static/`: Static CSS resources and UI enhancements.

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Application**:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` to view the Dashboard (login with default credentials if prompted).

## Notice

Please do not commit the `blockchain.json` to version control unless seeding the blockchain network. The `.gitignore` is prepared to ignore the local database and installer files.
