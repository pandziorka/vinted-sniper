import requests
import time

# =========================
# KONFIGURACJA
# =========================

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1480276065787056243/lO0zOj2__3OWDnvxZY559DWNMyvHOMFDZrsbpuBbZBRsaEl6lr1rNHpuuMAbyRxK6jZ3"

CHECK_DELAY = 2

MAX_PRICE =  600

IPHONE_KEYWORDS = [
    "iphone 15",
    "iphone 14",
    "iphone 13",
    "iphone 12"
]

BLACKLIST = [
    "na części",
    "na czesci",
    "uszkodzony",
    "zablokowany",
    "nie wysyłam przez vinted",
    "blik",
    "kup teraz"
]

# =========================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

URL = "https://www.vinted.pl/api/v2/catalog/items"

seen_ids = set()


def send_to_discord(title, price, link, image):

    data = {
        "embeds": [
            {
                "title": title,
                "url": link,
                "color": 3447003,
                "fields": [
                    {
                        "name": "Price",
                        "value": f"{price} zł",
                        "inline": True
                    }
                ],
                "image": {"url": image},
                "footer": {"text": "Vinted iPhone Sniper"}
            }
        ]
    }

    try:
        requests.post(DISCORD_WEBHOOK, json=data)
    except:
        pass


def valid_item(title, price):

    t = title.lower()

    if not any(k in t for k in IPHONE_KEYWORDS):
        return False

    if any(b in t for b in BLACKLIST):
        return False

    if price > MAX_PRICE:
        return False

    return True


def check_items():

    params = {
        "search_text": "iphone",
        "order": "newest_first",
        "per_page": 20
    }

    try:

        r = requests.get(URL, headers=HEADERS, params=params)

        if r.status_code != 200:
            print("API ERROR:", r.status_code)
            return

        items = r.json()["items"]

        for item in items:

            item_id = item["id"]

            if item_id in seen_ids:
                continue

            seen_ids.add(item_id)

            title = item["title"]

            price = float(item["price"]["amount"])

            if not valid_item(title, price):
                continue

            link = item["url"]

            image = item["photo"]["url"]

            print("FOUND:", title, price)

            send_to_discord(title, price, link, image)

    except Exception as e:
        print("Error:", e)


while True:

    check_items()

    time.sleep(CHECK_DELAY)

