import os

from foodscrape.config import DevConfig


def main() -> None:
    if not os.path.exists(DevConfig.LOG_DIR):
        os.makedirs(DevConfig.LOG_DIR)
    if not os.path.exists(DevConfig.DATA_DIR):
        os.makedirs(DevConfig.DATA_DIR)


if __name__ == "__main__":
    main()
