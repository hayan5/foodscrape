import os
import unittest

import click

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(FILE_PATH, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")


@click.command()
def test():
    tests = unittest.TestLoader().discover(TEST_PATH, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


# pytest --cov=. tests/ --cov-report xml:cov.xml


def hello():
    print("hello")
    return 1 + 3
