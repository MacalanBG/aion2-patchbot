import time
import requests
from playwright.sync_api import sync_playwright

WEBHOOK = "https://discord.com/api/webhooks/1523246464300482590/FVf-o_hl1OoPCyly1tOe19XNNIb9ZSM9NBCZr5rE_54tSmkzKoYz1LlOLlTRPcc9atGT"
URL = "https://shugo.gg/news"

seen = set()

def send_discord(title, link):
    requests.post(WEBHOOK, json={
        "content": f"🔔 **Нов AION2 Patch!**\n\n{title}\n{link}"
    })

def fetch_news():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        page.wait_for_timeout(5000)  # изчаква JS да зареди

        links = page.query_selector_all("a")

        news = []

        for l in links:
            try:
                href = l.get_attribute("href")
                title = l.inner_text().strip()

                if href and "/news" in href and title:
                    full = "https://shugo.gg" + href
                    news.append((title, full))
            except:
                pass

        browser.close()
        return news

print("PatchBot PRO стартира...")

while True:
    try:
        news = fetch_news()

        print("Found:", len(news))

        for title, link in news:
            if link not in seen:
                print("NEW:", title)
                send_discord(title, link)
                seen.add(link)

    except Exception as e:
        print("Error:", e)

    time.sleep(300)