import requests
import time

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1480276065787056243/lO0zOj2__3OWDnvxZY559DWNMyvHOMFDZrsbpuBbZBRsaEl6lr1rNHpuuMAbyRxK6jZ3"

CHECK_DELAY = 4
MAX_PRICE = 600

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
    "kup teraz",
    "dummy","atrapa",
    "na części","na czesci","części","czesci",
    "housing","ramka",
    "do iphone","dla iphone",
    "zamiana","swap"
]

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.vinted.pl/",
    "Origin": "https://www.vinted.pl"
})

session.cookies.update({
    "access_token_web": "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjoxMDk1OTA4NDgsImFwcF9pZCI6NCwiYXVkIjoiZnIuY29yZS5hcGkiLCJjbGllbnRfaWQiOiJ3ZWIiLCJleHAiOjE3NzMwMTUwMDksImlhdCI6MTc3MzAwNzgwOSwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwibG9naW5fdHlwZSI6MywicHVycG9zZSI6ImFjY2VzcyIsInNjb3BlIjoidXNlciIsInNpZCI6IjUwNGFkNGU5LTE3NzI5OTk5NzUiLCJzdWIiOiIxNjA2OTQ0MDAiLCJjYyI6IlBMIiwiYW5pZCI6ImFhY2Y2NjZiLWFmMmEtNGY2Yi1iMzYyLTllNzA5YTEzNzdmNyIsImFjdCI6eyJzdWIiOiIxNjA2OTQ0MDAifX0.HUu4OVkhVTAujDHDhRoauGBGRlQN6k4pDMjoTLDQ6Zd26_I8lIfpkTd9lTf2zf0FMRfahej_vCnnR-PbdBv2nspgbw5UC7FMSFB3gjY89wUpBi5Y4Q4-J89ZVIrlZRsdFl2THHA0dTqgktkHYXgD_u2c4E70Pzdx5rMQ8G04gAE_5GqhgVgasXqBX9nxL13C5S1-YUuCiN8DQh2rtSx5ttwd_nO5LK9bx8eTu7WO99FD8H08zumF4hq-3____oxKsb1GbhnKxTYQF0MZkqYIR_KquYfGxltZzh-eIH9dlLfyx2bb2M19p2RDn4UJB7Z792nxcGC2dVlEWoeaAaoqAA",
    "cf_clearance": "SdiiGAAY2Wl9jh8rHfh02MgpYgwwU24aZmb5Q_a6m4Y-1773007808-1.2.1.1-K6eBPq40STWvUMEXa2H9y65xfMBBfiNW1p0boiD5Tc3P4iqVvWrlnSwO39emhz06aLVkzUK6EqoAEgtx5aofMfboGgUfdPTh0wvDTih.lRVofzp1eJLkyqlgTbRKxWQj9slY11tb62o4FhbGMVfLotKmEdjq._zYaqVFCS4FXEXPUATcVsGBZiHmqDtvsOJZMd0Is6vhUFUiU22CviQhz_d2KfacQKThysPFRmcK62o",
    "datadome": "GkRlwpvjxhCqORnAcguEJ0UdLF_SEtAPfPOfHJb8nWX3DZIS1AtZj5HteJOOrVE3aF2Qg~G0eD1A~YCfeGB1Yv69hPpwPfmOnbQUs1mKiibsqZbKdVOP1uQnsQIFnS8C"
})

URL = "https://www.vinted.pl/api/v2/catalog/items"

seen_ids = set()


def send_to_discord(title, price, link, image):

    data = {
        "embeds": [
            {
                "title": title,
                "url": link,
                "color": 3066993,
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
        session.post(DISCORD_WEBHOOK, json=data)
    except:
        pass


def valid_item(title, price):

    t = title.lower()

    # musi zawierać model iphone
    if not any(k in t for k in IPHONE_KEYWORDS):
        return False

    # blokujemy tylko gdy tytuł zaczyna się od akcesorium
    accessory_starts = [
        "etui",
        "case",
        "pokrowiec",
        "szkło",
        "szklo",
        "glass",
        "kabel",
        "ładowarka",
        "ladowarka"
    ]

    for word in accessory_starts:
        if t.startswith(word):
            return False

    # blokada części i uszkodzonych
    parts_words = [
        "na części",
        "na czesci",
        "uszkodzony",
        "uszkodzone",
        "zablokowany",
        "blokada icloud",
    ]

    if any(word in t for word in parts_words):
        return False

    if price > MAX_PRICE:
        return False

    return True


def check_items():

    params = {
         "search_text": "iphone",
    "order": "newest_first",
    "per_page": 20,
    "price_from": 100
    }

    r = session.get(URL, params=params)

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

        print("FOUND:", title)

        send_to_discord(title, price, link, image)


while True:

    check_items()

    time.sleep(CHECK_DELAY)

    time.sleep(CHECK_DELAY)






