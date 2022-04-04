from dataclasses import dataclass, field
from typing import Union

import pandas as pd
import requests
from bs4 import BeautifulSoup

from foodscrape.common import (
    ExportStrategyFunction,
    FetchStrategyFunction,
    ScrapeStrategyFunction,
)


@dataclass
class Scraper:
    fetch_strategy: FetchStrategyFunction
    scrape_strategy: ScrapeStrategyFunction
    export_strategy: ExportStrategyFunction
    session: requests.Session = field(init=False, default=requests.Session())

    def scrape(
        self, url: str, fetch: bool = True, soup: BeautifulSoup = BeautifulSoup()
    ) -> Union[None, pd.DataFrame]:
        if fetch:
            fetched_data: bytes = self.fetch_strategy(url, self.session)
            soup = BeautifulSoup(fetched_data, "lxml")

        scraped_data = self.scrape_strategy(soup)
        return self.export_strategy(scraped_data)
