import os

import click

# import unittest


FILE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(FILE_PATH, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
def test():
    os.system("pytest --cov=. tests/ --cov-report xml:cov.xml")


def hello():
    print("hello")
    return 1 + 3
