import requests
import time

WEBHOOK = "https://discord.com/api/webhooks/1480276065787056243/lO0zOj2__3OWDnvxZY559DWNMyvHOMFDZrsbpuBbZBRsaEl6lr1rNHpuuMAbyRxK6jZ3"

CHECK_DELAY = 3

SEARCHES = [
    {"query": "iphone 13", "max_price": 1200},
    {"query": "iphone 13 mini", "max_price": 900},
    {"query": "iphone 14", "max_price": 1500},
    {"query": "iphone 12 pro", "max_price": 900},
]

BLOCKED_WORDS = [
    "na części",
    "na czesci",
    "uszkodzony",
    "blokada icloud",
    "nie sprzedaje przez kup teraz",
    "blik",
    "tylko przelew",
    "zamiana",
    "rezerwacja",
]

seen_ids = set()

headers = {
    "User-Agent": "Mozilla/5.0"
}


def contains_blocked(text):
    text = text.lower()
    for word in BLOCKED_WORDS:
        if word in text:
            return True
    return False


def send_discord(item):
    title = item["title"]
    price = item["price"]
    url = item["url"]

    message = {
        "content": f"📱 **NOWA OFERTA**\n{title}\n💰 {price} zł\n{url}"
    }

    requests.post(WEBHOOK, json=message)


def check_search(search):

    url = f"https://www.vinted.pl/api/v2/catalog/items?search_text={search['query']}&order=newest_first&per_page=20"

    r = requests.get(url, headers=headers)

    items = r.json()["items"]

    for item in items:

        item_id = item["id"]

        if item_id in seen_ids:
            continue

        seen_ids.add(item_id)

        title = item["title"].lower()

        if contains_blocked(title):
            continue

        price = float(item["price"])

        if price > search["max_price"]:
            continue

        send_discord(item)

        print("Nowa oferta:", item["title"], price)


while True:

    try:

        for search in SEARCHES:

            check_search(search)

        time.sleep(CHECK_DELAY)

    except Exception as e:

        print("Błąd:", e)

        time.sleep(10)