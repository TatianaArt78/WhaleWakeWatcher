import requests
import time
import datetime
from eth_utils import from_wei

ETHERSCAN_API_KEY = "YourEtherscanAPIKeyHere"
MIN_TRANSFER_ETH = 1000  # отслеживаем только переводы свыше 1000 ETH

def get_large_tx():
    url = f"https://api.etherscan.io/api?module=account&action=txlistinternal&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "1":
        print("Ошибка API:", data.get("message"))
        return []

    big_transfers = []
    for tx in data["result"]:
        value_eth = from_wei(int(tx["value"]), 'ether')
        if value_eth >= MIN_TRANSFER_ETH:
            big_transfers.append({
                "from": tx["from"],
                "to": tx["to"],
                "value": value_eth,
                "time": datetime.datetime.fromtimestamp(int(tx["timeStamp"]))
            })
    return big_transfers

def monitor():
    print("🔍 Начинаем отслеживание китов...")
    seen = set()
    while True:
        try:
            transfers = get_large_tx()
            for tx in transfers:
                tx_id = (tx["from"], tx["to"], tx["value"], tx["time"])
                if tx_id not in seen:
                    seen.add(tx_id)
                    print(f"[{tx['time']}] 🐋 {tx['from']} → {tx['to']} : {tx['value']} ETH")
            time.sleep(60)
        except KeyboardInterrupt:
            print("🛑 Остановка мониторинга")
            break
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(30)

if __name__ == "__main__":
    monitor()
