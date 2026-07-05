import requests
from bs4 import BeautifulSoup
import time

WEBHOOK = "https://discord.com/api/webhooks/1523246464300482590/FVf-o_hl1OoPCyly1tOe19XNNIb9ZSM9NBCZr5rE_54tSmkzKoYz1LlOLlTRPcc9atGT"
URL = "https://shugo.gg/news"

seen = set()

def get_news():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):
        href = a.get("href")
        title = a.text.strip()

        if href and "/news" in href and title:
            full = "https://shugo.gg" + href
            news.append((title, full))

    return news


def send(title, link):
    requests.post(WEBHOOK, json={
        "content": f"🔔 Нов пач!\n\n{title}\n{link}"
    })


print("PatchBot стартира...")

while True:
    try:
        for title, link in get_news():
            if link not in seen:
                print("Нов:", title)
                send(title, link)
                seen.add(link)

    except Exception as e:
        print("Грешка:", e)

    time.sleep(300)