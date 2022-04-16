import requests
from bs4 import BeautifulSoup, Tag

from foodscrape.database import db
from foodscrape.fetch import fetch_data_compressed
from foodscrape.logger import get_logger

from .models import Sitemap

logger = get_logger(__name__)


class URL_NOT_FOUND_ERROR(Exception):
    pass


class URL_ALREADY_PRESENT_IN_DB(Exception):
    pass


def scrape_sitemap(url: str):
    session = requests.Session()
    data = fetch_data_compressed(url, session)
    soup = BeautifulSoup(data, "lxml")

    for element in soup.find_all("loc"):
        try:
            url = _get_url(element)
            _save_sitemap(url)

        except URL_NOT_FOUND_ERROR:
            logger.debug("Url not found")
            continue

        except URL_ALREADY_PRESENT_IN_DB:
            logger.error("Url already present in DB")
            continue

    session.close()
    logger.info("Sitemap Successfully Saved")


def _get_url(element) -> str:
    if isinstance(element, Tag):
        url = element.text.strip()
        return url

    raise URL_NOT_FOUND_ERROR()


def _save_sitemap(url: str) -> None:
    sitemap = Sitemap(url=url)

    q = db.session.query(Sitemap.id).filter(Sitemap.url == url)
    if db.session.query(q.exists()).scalar():
        raise URL_ALREADY_PRESENT_IN_DB()

    db.session.add(sitemap)
    db.session.commit()
