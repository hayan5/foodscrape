import os

from foodscrape.app import create_app
from foodscrape.config import DevConfig

os.environ["FLASK_APP"] = "main.py"
os.environ["FLASK_ENV"] = "dev"
os.environ["FLASK_DEBUG"] = "1"

if __name__ == "__main__":
    # Set environment variables
    os.environ["FLASK_APP"] = "main.py"
    os.environ["FLASK_ENV"] = "dev"
    os.environ["FLASK_DEBUG"] = "1"

    app = create_app(DevConfig)
