# Requisito 7
from datetime import datetime
from tech_news.database import search_news


def search_by_title(title):
    search_query = {"title": {"$regex": title, "$options": "i"}}
    return [(_["title"], _["url"]) for _ in search_news(search_query)]


# Requisito 8
def search_by_date(date):
    try:
        date_iso = datetime.fromisoformat(date)
        search_query = {"timestamp": {"$regex": date_iso.strftime("%d/%m/%Y")}}
        return [(_["title"], _["url"]) for _ in search_news(search_query)]
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    search_query = {"category": {"$regex": category, "$options": "i"}}
    return [(_["title"], _["url"]) for _ in search_news(search_query)]
