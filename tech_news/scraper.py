# Requisito 1
import time
from parsel import Selector
import requests
from tech_news.database import create_news


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(
            url, {
                "user-agent": "Fake user-agent"
                },
            timeout=3)
        if response.status_code == 200:
            return response.text
    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    return selector.css("h2.entry-title a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css('.next::attr(href)').get()


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author a::text").get()
    reading_time = int(selector.css(
        '.meta-reading-time::text').get().split(' ')[0])
    summary = selector.xpath("string(//p)").get().strip()
    category = selector.css("span.label::text").get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    new_page = []
    url = 'https://blog.betrybe.com/'
    tech_news = []

    while len(new_page) < amount:
        response = fetch(url)
        new_page.extend(scrape_updates(response))
        url = scrape_next_page_link(response)

    for page in new_page:
        content = fetch(page)
        if len(tech_news) < amount:
            tech_news.append(scrape_news(content))

    create_news(tech_news)
    return tech_news
