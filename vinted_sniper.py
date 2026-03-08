import requests
import time

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1480276065787056243/lO0zOj2__3OWDnvxZY559DWNMyvHOMFDZrsbpuBbZBRsaEl6lr1rNHpuuMAbyRxK6jZ3"

CHECK_DELAY = 4
MAX_PRICE = 4000

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
    "access_token_web": "eyJraWQiOiJFNTdZZHJ1SHBsQWp1MmNObzFEb3JIM2oyN0J1NS1zX09QNVB3UGlobjVNIiwiYWxnIjoiUFMyNTYifQ.eyJhY2NvdW50X2lkIjoxMDk1OTA4NDgsImFwcF9pZCI6NCwiYXVkIjoiZnIuY29yZS5hcGkiLCJjbGllbnRfaWQiOiJ3ZWIiLCJleHAiOjE3NzMwMDcxNzUsImlhdCI6MTc3Mjk5OTk3NSwiaXNzIjoidmludGVkLWlhbS1zZXJ2aWNlIiwibG9naW5fdHlwZSI6MywicHVycG9zZSI6ImFjY2VzcyIsInNjb3BlIjoidXNlciIsInNpZCI6IjUwNGFkNGU5LTE3NzI5OTk5NzUiLCJzdWIiOiIxNjA2OTQ0MDAiLCJjYyI6IlBMIiwiYW5pZCI6ImFhY2Y2NjZiLWFmMmEtNGY2Yi1iMzYyLTllNzA5YTEzNzdmNyIsImFjdCI6eyJzdWIiOiIxNjA2OTQ0MDAifX0.HRfrNjx-7mIdlYrEQoo-6qVloqG3WotnC9bKcZqipAWgi7B6jWmgTlqu1jyvC-Q4s41tqmaJuTkpiDyXpEGPgFMz3mQRz0BF73oRtCcyQZeVIoHUALgCUqgxxdVNrnMsS9smw3h5Db4iQHSQGzWGYnde_bgtTSs-qdQ_He2wMfkk6FOfot6r4g0Df0sH3Nk-kNH_c13gDOvupoqCWv3VGfV1TJxRweOHNGeylCw3HgzX0AVdL0LJ4daxUIghyz1ROyY_mT7ha_39J7zSdF4W3wAkNtzv-ky1HCbja_S8nAR3BJuhh7BlGIQ5cW6C27oe3H5PZpUDOWOHiUa0GgFfmg",
    "cf_clearance": "ICYRmZJmmptk7gNwp3uwYyTjpBk5CkebbFDL53KzdLU-1773003184-1.2.1.1-YY.pjPOixjQL4zoHuuFrG4xwMlG1LL1Bd8TfaeA7aiAKN0sAH3N15AoxNBZ5ixYllFuPSuKVg53wd5ePDsuzCzHgyrB4uFo7zNfsiAWEiDVH6pIFN3FpzvvVgx3bCvYtT_2rU24f23a.QCFo8m0uWShzgRgqpFnNanGAdJVvivigpltMNa1z2kND90MwUNHdrv.gqyfd4TwcusmYZVzi1rIB8PqMu4JpjMbKnnOtsDk",
    "datadome": "aSvzTzI7Iikhp3GK~kF9vdxb0KHSY18Q3UN7teL0_1udAzZVROwO4tHuVGEEDdxNqZ6kK6bPbJIFYEpbxkR8CjdgwdUxyVr1O3Xt~WErBzY5TxD2jUfpZtNP_YwAQtFB"
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
        "display",
        "wyświetlacz",
        "wyswietlacz"
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
        "per_page": 20
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



