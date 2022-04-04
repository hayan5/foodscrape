from functools import partial

from foodscrape.config import Config
from foodscrape.export import export_csv, export_log, export_sitemap_txt
from foodscrape.fetch import fetch_data_compressed, fetch_data_uncompressed
from foodscrape.recipe import scrape_recipe
from foodscrape.scrape import Scraper
from foodscrape.sitemap import scrape_sitemap


def main():
    recipe_fetch_strategy = partial(fetch_data_uncompressed)
    recipe_scrape_strategy = partial(scrape_recipe)
    recipe_export_strategy = partial(
        export_csv, filename=Config.DATA_DIR / "recipes/recipe-1.csv"
    )
    recipe_scraper = Scraper(
        recipe_fetch_strategy, recipe_scrape_strategy, recipe_export_strategy
    )
    count = 0
    with open(Config.DATA_DIR / "sitemaps/sitemap-1.txt", "r", encoding="UTF-8") as f:
        url = f.readline()
        while url and count < 1:
            url = url.strip()
            recipe_scraper.scrape(url)
            count += 1
            url = f.readline()


def create_sitemap_scraper():
    sitemap_fetch_strategy = partial(fetch_data_compressed)
    sitemap_scrape_strategy = partial(scrape_sitemap)
    sitemap_export_strategy = partial(
        export_sitemap_txt, filename=Config.DATA_DIR / "sitemaps/sitemap-1.txt"
    )
    sitemap_scraper = Scraper(
        sitemap_fetch_strategy, sitemap_scrape_strategy, sitemap_export_strategy
    )
    sitemap_scraper.scrape("https://www.food.com/sitemap-1.xml.gz")


if __name__ == "__main__":
    # create_sitemap_scraper()
    main()
