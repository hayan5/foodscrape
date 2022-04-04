import pathlib

import pandas as pd

from foodscrape.common import ScrapedElement, Sitemap
from foodscrape.logger import get_logger

logger = get_logger(__name__)


def export_sitemap_txt(data: ScrapedElement, filename: pathlib.Path) -> None:
    # export_filename = self.export_dir / filename
    # try:
    #     self.export_dir.mkdir(parents=True)
    # except OSError as err:
    #     logger.error(err)
    # print(data)
    if isinstance(data, Sitemap):
        with open(filename, "w", encoding="UTF-8") as f:
            for url in data.urls:
                f.write(url + "\n")

    logger.info("Data exported to file %s", filename)


def export_log(data: ScrapedElement) -> None:
    logger.info(data)


def export_csv(data: ScrapedElement, filename: pathlib.Path) -> None:
    df = pd.DataFrame.from_dict([data.__dict__])
    df.to_csv(filename)
    logger.info(df)


def return_as_df(data: ScrapedElement) -> pd.DataFrame:
    return data.to_dataframe()
