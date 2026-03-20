from backend.esp8266_api import fetch_both, fetch_history
from backend.data_handler import DataHandler
from backend.blockchain import Blockchain

handler = DataHandler()
blockchain = Blockchain()

import json, os
from datetime import datetime

reset_ts = None
try:
    conf_path = os.path.join(os.path.dirname(__file__), "reset_config.json")
    with open(conf_path, "r") as f:
        conf = json.load(f)
        reset_ts = datetime.fromisoformat(conf["reset_timestamp"])
except:
    pass

print("Bootstrapping cumulative energy from ThingSpeak Cloud history...")
try:
    data1, data2 = fetch_history(8000)
    length = min(len(data1), len(data2))
    processed_count = 0
    if length > 1:
        for i in range(1, length):
            try:
                dt_str = str(data1[i]["created_at"]).replace("Z", "+00:00")
                dt = datetime.fromisoformat(dt_str)
                if reset_ts and dt < reset_ts:
                    continue
            except:
                pass
            handler.process(data1[i-1], data1[i], data2[i-1], data2[i], is_history_replay=True)
            processed_count += 1
        print(f"Bootstrap complete. Processed {processed_count} historical payloads (ignored {length - 1 - processed_count} pre-reset vectors).")
except Exception as e:
    print("Failed to bootstrap history:", e)

try:
    blockchain.load()
except Exception:
    pass

def get_latest_data():
    data1, data2 = fetch_both()

    if len(data1) >= 2 and len(data2) >= 2:
        data = handler.process(
            data1[-2], data1[-1],
            data2[-2], data2[-1]
        )

        data["new_block_minted"] = False

        if not (data.get("is_duplicate") or data.get("is_stale")):
            blockchain.add_block(data)
            blockchain.save()
            data["new_block_minted"] = True

        data["block_index"] = len(blockchain.chain)
        return data

    return {}