import requests
import time

# =========================
# KONFIGURACJA
# =========================

TOKEN = "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjoxMDk1OTA4NDgsImFwcF9pZCI6NCwiYXVkIjoiZnIuY29yZS5hcGkiLCJjbGllbnRfaWQiOiJ3ZWIiLCJleHAiOjE3NzMwMDcxNzUsImlhdCI6MTc3Mjk5OTk3NSwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwibG9naW5fdHlwZSI6MywicHVycG9zZSI6ImFjY2VzcyIsInNjb3BlIjoidXNlciIsInNpZCI6IjUwNGFkNGU5LTE3NzI5OTk5NzUiLCJzdWIiOiIxNjA2OTQ0MDAiLCJjYyI6IlBMIiwiYW5pZCI6ImFhY2Y2NjZiLWFmMmEtNGY2Yi1iMzYyLTllNzA5YTEzNzdmNyIsImFjdCI6eyJzdWIiOiIxNjA2OTQ0MDAifX0.HRfrNjx-7mIdlYrEQoo-6qVloqG3WotnC9bKcZqipAWgi7B6jWmgTlqu1jyvC-Q4s41tqmaJuTkpiDyXpEGPgFMz3mQRz0BF73oRtCcyQZeVIoHUALgCUqgxxdVNrnMsS9smw3h5Db4iQHSQGzWGYnde_bgtTSs-qdQ_He2wMfkk6FOfot6r4g0Df0sH3Nk-kNH_c13gDOvupoqCWv3VGfV1TJxRweOHNGeylCw3HgzX0AVdL0LJ4daxUIghyz1ROyY_mT7ha_39J7zSdF4W3wAkNtzv-ky1HCbja_S8nAR3BJuhh7BlGIQ5cW6C27oe3H5PZpUDOWOHiUa0GgFfmg"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1480276065787056243/lO0zOj2__3OWDnvxZY559DWNMyvHOMFDZrsbpuBbZBRsaEl6lr1rNHpuuMAbyRxK6jZ3"

CHECK_DELAY = 2

MAX_PRICE = 600

# modele iphone które chcesz łapać
IPHONE_KEYWORDS = [
    "iphone 13",
    "iphone 14",
    "iphone 15",
    "iphone 12"
]

# czarna lista
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
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

SEARCH_URL = "https://www.vinted.pl/api/v2/catalog/items"

seen_ids = set()


def send_to_discord(title, price, url, image):

    data = {
        "embeds": [
            {
                "title": title,
                "url": url,
                "color": 3066993,
                "fields": [
                    {
                        "name": "Price",
                        "value": f"{price} zł",
                        "inline": True
                    }
                ],
                "image": {
                    "url": image
                },
                "footer": {
                    "text": "Vinted iPhone Sniper"
                }
            }
        ]
    }

    requests.post(DISCORD_WEBHOOK, json=data)


def valid_item(title, price):

    title_lower = title.lower()

    # czy zawiera iphone
    if not any(word in title_lower for word in IPHONE_KEYWORDS):
        return False

    # czarna lista
    if any(word in title_lower for word in BLACKLIST):
        return False

    # cena
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

        r = requests.get(SEARCH_URL, headers=HEADERS, params=params)

        if r.status_code != 200:
            print("API error:", r.status_code)
            return

        data = r.json()
        items = data["items"]

        for item in items:

            item_id = item["id"]

            if item_id in seen_ids:
                continue

            seen_ids.add(item_id)

            title = item["title"]

            price = float(item["price"]["amount"])

            if not valid_item(title, price):
                continue

            url = item["url"]

            image = item["photo"]["url"]

            print("IPHONE FOUND:", title)

            send_to_discord(title, price, url, image)

    except Exception as e:
        print("Error:", e)


while True:

    check_items()

    time.sleep(CHECK_DELAY)

