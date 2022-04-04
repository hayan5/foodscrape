from bs4 import BeautifulSoup, Tag

from foodscrape.common import Sitemap
from foodscrape.logger import get_logger

logger = get_logger(__name__)


def scrape_sitemap(soup: BeautifulSoup) -> Sitemap:
    sitemap = Sitemap()

    for element in soup.find_all("loc"):
        if isinstance(element, Tag):
            url = element.text.strip()
            sitemap.urls.append(url)

    return sitemap
