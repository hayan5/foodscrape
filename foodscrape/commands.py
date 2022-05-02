import os

import click

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(FILE_PATH, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
def test():
    os.system("pytest --cov=foodscrape --cov-report xml:cov.xml")
