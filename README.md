# Virtual Power Plant (VPP) Blockchain System

A Flask-based Virtual Power Plant system that integrates real-time energy monitoring, IoT data acquisition, and a custom blockchain layer to securely log system activity and transactions.

## Overview

This project simulates a Virtual Power Plant by combining:

- Real-time energy data from ESP8266 nodes  
- Backend processing and aggregation logic  
- A web-based dashboard for visualization  
- A lightweight blockchain implementation for secure logging  

The system ensures that all critical operations (energy updates, transactions, system states) are stored in an immutable format.

## Core Components (Code-Level)

### app.py
- Main Flask application  
- Defines routes for:
  - Dashboard display  
  - Blockchain explorer  
  - API endpoints for frontend updates  
- Connects frontend with backend modules  

### backend/blockchain.py
- Implements blockchain logic:
  - Block creation  
  - Hash generation  
  - Chain validation  
- Stores data in `blockchain.json`  
- Records:
  - Energy transactions  
  - System updates  

### backend/energy_monitor.py
- Handles energy-related computations:
  - AC power  
  - DC power  
  - Battery charge/discharge  
- Aggregates system metrics for dashboard display  

### backend/esp_interface.py
- Manages communication with ESP8266 devices  
- Fetches live sensor data  
- Updates backend with real-time values  

### templates/
- HTML files rendered by Flask  
- Includes:
  - Dashboard UI  
  - Blockchain explorer view  
- Supports dynamic data rendering  

### static/
- CSS and JavaScript assets  
- Handles:
  - UI styling  
  - Graph rendering  
  - API calls to backend  

## Features

- **Real-Time Dashboard**
  - Displays live energy metrics using backend data  

- **Blockchain Logging**
  - All key updates recorded via blockchain module  

- **IoT Integration**
  - Live data fetched from ESP8266 devices  

- **Cost & Payment Analysis**
  - Displays energy usage, cost distribution, and savings  

## Data Flow

1. ESP8266 sends sensor data  
2. `esp_interface.py` processes incoming data  
3. `energy_monitor.py` computes energy metrics  
4. `blockchain.py` logs transactions  
5. `app.py` serves updated data to frontend  
6. Frontend updates dynamically  

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the application:
   ```bash
   python app.py
3. Open in browser:
   http://localhost:5000

## Important Notes
 - blockchain.json acts as the local blockchain ledger
 - It is excluded via .gitignore to avoid unnecessary commits
 - Include it only when initializing or demonstrating blockchain data

## Future Improvements
-Distributed blockchain implementation
-User authentication and role management
-WebSocket-based real-time updates
-Cloud deployment for public access
