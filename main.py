from functools import partial

import pandas as pd

from foodscrape.config import Config
from foodscrape.export import export_csv, export_log, export_sitemap_txt, return_as_df
from foodscrape.fetch import fetch_data_compressed, fetch_data_uncompressed
from foodscrape.recipe import scrape_recipe
from foodscrape.scrape import Scraper
from foodscrape.sitemap import scrape_sitemap


def main():
    recipe_fetch_strategy = partial(fetch_data_uncompressed)
    recipe_scrape_strategy = partial(scrape_recipe)
    recipe_export_strategy = partial(return_as_df)
    recipe_scraper = Scraper(
        recipe_fetch_strategy, recipe_scrape_strategy, recipe_export_strategy
    )
    count = 0
    url_df = pd.read_csv(Config.DATA_DIR / "sitemaps/sitemap-1.csv")
    urls = url_df["url"]
    recipe_df = pd.DataFrame()
    i = 0
    for url in urls:
        recipe = recipe_scraper.scrape(url)
        if isinstance(recipe, pd.DataFrame):
            recipe_df = pd.concat([recipe, recipe_df])

        i += 1

        if i >= 10:
            break

    recipe_df.to_csv(Config.DATA_DIR / "recipes/recipe-1.csv")


def create_sitemap_scraper():
    sitemap_fetch_strategy = partial(fetch_data_compressed)
    sitemap_scrape_strategy = partial(scrape_sitemap)
    sitemap_export_strategy = partial(return_as_df)
    sitemap_scraper = Scraper(
        sitemap_fetch_strategy, sitemap_scrape_strategy, sitemap_export_strategy
    )
    df = sitemap_scraper.scrape("https://www.food.com/sitemap-1.xml.gz")
    if isinstance(df, pd.DataFrame):
        df.to_csv(Config.DATA_DIR / "sitemaps/sitemap-1.csv")


if __name__ == "__main__":
    # create_sitemap_scraper()
    main()
