import requests
import time
import browser_cookie3

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1480276065787056243/lO0zOj2__3OWDnvxZY559DWNMyvHOMFDZrsbpuBbZBRsaEl6lr1rNHpuuMAbyRxK6jZ3"

CHECK_DELAY = 5

MIN_PRICE = 100
MAX_PRICE = 600

SEARCHES = [
    "iphone",
    "iphone 15",
    "iphone 14",
    "iphone 13",
    "iphone 12"
]

BLACKLIST = [
    "na części","na czesci","części","czesci",
    "uszkodzony","uszkodzone","zablokowany",
    "etui","pokrowiec",
    "szkło","szklo",
    "dummy","atrapa",
    "zamiana","swap"
]

URL = "https://www.vinted.pl/api/v2/catalog/items"

seen_ids = set()


def create_session():

    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.vinted.pl/",
        "Origin": "https://www.vinted.pl"
    })

    cookies = browser_cookie3.chrome(domain_name='vinted.pl')
    session.cookies.update(cookies)

    return session


def send_to_discord(title, price, link, image):

    data = {
        "embeds": [{
            "title": title,
            "url": link,
            "color": 3066993,
            "fields": [{
                "name": "Cena",
                "value": f"{price} zł",
                "inline": True
            }],
            "image": {"url": image},
            "footer": {"text": "Vinted Sniper"}
        }]
    }

    try:
        requests.post(DISCORD_WEBHOOK, json=data)
    except:
        pass


def valid_item(title, price):

    t = title.lower()

    if price < MIN_PRICE or price > MAX_PRICE:
        return False

    if any(word in t for word in BLACKLIST):
        return False

    if "iphone" not in t:
        return False

    return True


def check_items(session, search):

    params = {
        "search_text": search,
        "order": "newest_first",
        "per_page": 20
    }

    r = session.get(URL, params=params)

    if r.status_code != 200:
        print("API error:", r.status_code)
        return False

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

    return True


session = create_session()

search_index = 0

while True:

    try:

        search = SEARCHES[search_index]

        ok = check_items(session, search)

        if not ok:
            print("Refreshing cookies...")
            session = create_session()

        search_index += 1

        if search_index >= len(SEARCHES):
            search_index = 0

    except Exception as e:

        print("Error:", e)
        session = create_session()

    time.sleep(CHECK_DELAY)






