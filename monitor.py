import requests
import threading
import time
import random
from datetime import datetime

SANDBOXES = [
    "https://abc123.csb.app",
    "https://mybot.csb.app",
    "https://panelxyz.csb.app",
    "https://test123.csb.app"
]

REQUEST_INTERVAL = 10
TIMEOUT = 20
THREADS_PER_SANDBOX = 3

ENDPOINTS = [
    "/",
    "/health",
    "/?keepalive=1",
    "/favicon.ico",
]

USER_AGENTS = [
    "Mozilla/5.0",
    "Chrome/124.0",
    "Safari/537.36",
    "Edge/122.0",
]

def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

def keep_alive(base_url):

    session = requests.Session()

    while True:

        try:

            endpoint = random.choice(ENDPOINTS)

            random_id = random.randint(100000, 999999)

            if "?" in endpoint:
                url = f"{base_url}{endpoint}&t={random_id}"
            else:
                url = f"{base_url}{endpoint}?t={random_id}"

            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Connection": "keep-alive",
                "Accept": "*/*",
            }

            start = time.time()

            response = session.get(
                url,
                headers=headers,
                timeout=TIMEOUT,
                allow_redirects=True
            )

            ping = round((time.time() - start) * 1000)

            if response.status_code == 200:
                log(f"ONLINE ✅ {base_url} ({ping}ms)")

            else:
                log(f"STATUS {response.status_code} ⚠️ {base_url}")

        except Exception as e:
            log(f"ERROR ❌ {base_url}")
            log(str(e))

            time.sleep(2)
            continue

        time.sleep(REQUEST_INTERVAL)

print("🚀 MULTI CODESANDBOX MONITOR STARTED")

for sandbox in SANDBOXES:

    for i in range(THREADS_PER_SANDBOX):

        t = threading.Thread(
            target=keep_alive,
            args=(sandbox,)
        )

        t.daemon = True
        t.start()

while True:
    time.sleep(999999)
