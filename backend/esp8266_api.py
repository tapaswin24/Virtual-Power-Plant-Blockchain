import requests

# -------- CLOUD 1 (Battery + Rectifier) --------
CHANNEL_1 = "3298417"
API_KEY_1 = "997BYBV8KRXZEVK2"

URL_1 = f"https://api.thingspeak.com/channels/{CHANNEL_1}/feeds.json?api_key={API_KEY_1}&results=2"


# -------- CLOUD 2 (Solar + AC Grid) --------
CHANNEL_2 = "3298424"
API_KEY_2 = "9H5UMMBB6RUUXCXP"

URL_2 = f"https://api.thingspeak.com/channels/{CHANNEL_2}/feeds.json?api_key={API_KEY_2}&results=2"


# -------- FETCH FUNCTIONS --------

def fetch_cloud_1():
    try:
        res = requests.get(URL_1, timeout=5)
        data = res.json().get("feeds", [])
        return data
    except Exception as e:
        print("Cloud 1 Error:", e)
        return []


def fetch_cloud_2():
    try:
        res = requests.get(URL_2, timeout=5)
        data = res.json().get("feeds", [])
        return data
    except Exception as e:
        print("Cloud 2 Error:", e)
        return []


def fetch_both():
    data1 = fetch_cloud_1()
    data2 = fetch_cloud_2()
    return data1, data2

def fetch_history(results=8000):
    """
    Pulls a deep chronological history directly from ThingSpeak arrays.
    """
    try:
        url1 = f"https://api.thingspeak.com/channels/{CHANNEL_1}/feeds.json?api_key={API_KEY_1}&results={results}"
        url2 = f"https://api.thingspeak.com/channels/{CHANNEL_2}/feeds.json?api_key={API_KEY_2}&results={results}"
        d1 = requests.get(url1, timeout=15).json().get("feeds", [])
        d2 = requests.get(url2, timeout=15).json().get("feeds", [])
        return d1, d2
    except Exception as e:
        print("Historical Fetch Error:", e)
        return [], []