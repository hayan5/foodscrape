import gzip
import json

import pytest
import responses
from requests import Session

from foodscrape.exceptions import FoodscrapeException
from foodscrape.fetch import fetch_data_compressed, fetch_data_uncompressed
from foodscrape.logger import get_logger

logger = get_logger(__name__)


@responses.activate
def test_fetch_uncompressed_success():
    responses.add(
        responses.GET,
        "http://test123.com/",
        body='{"body": "success"}',
        status=200,
        content_type="application/json",
    )

    resp = fetch_data_uncompressed("http://test123.com/", session=Session())

    assert json.loads(resp) == {"body": "success"}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://test123.com/"
    assert responses.calls[0].response.text == '{"body": "success"}'


@responses.activate
def test_fetch_uncompressed_fail():
    responses.add(
        responses.GET,
        "http://test123.com/error",
        body='{"error": "error"}',
        status=404,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        "http://test123.com/success",
        body='{"success": "success"}',
        status=200,
        content_type="application/json",
    )

    with pytest.raises(FoodscrapeException):
        fetch_data_uncompressed("http://test123.com/error", session=Session())

    fetch_data_uncompressed("http://test123.com/success", session=Session())

    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == "http://test123.com/error"
    assert responses.calls[1].request.url == "http://test123.com/success"


@responses.activate
def test_fetch_compressed_success():
    body = gzip.compress(bytes('{"body": "success"}', encoding="utf-8"))
    responses.add(
        responses.GET,
        "http://test123.com/",
        body=body,
        status=200,
    )

    resp = fetch_data_compressed("http://test123.com/", session=Session())
    assert json.loads(resp) == {"body": "success"}
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://test123.com/"


@responses.activate
def test_fetch_compressed_fail():
    body = gzip.compress(bytes('{"body": "success"}', encoding="utf-8"))

    responses.add(
        responses.GET,
        "http://test123.com/error1",
        body=body,
        status=404,
        content_type="application/json",
    )
    responses.add(
        responses.GET,
        "http://test123.com/error2",
        body='{"error": "error"}',
        status=200,
    )
    responses.add(
        responses.GET,
        "http://test123.com/success",
        body=body,
        status=200,
    )

    with pytest.raises(FoodscrapeException):
        fetch_data_compressed("http://test123.com/error1", session=Session())
    with pytest.raises(FoodscrapeException):
        fetch_data_compressed("http://test123.com/error2", session=Session())

    fetch_data_compressed("http://test123.com/success", session=Session())
    assert len(responses.calls) == 3
    assert responses.calls[0].request.url == "http://test123.com/error1"
    assert responses.calls[1].request.url == "http://test123.com/error2"
    assert responses.calls[2].request.url == "http://test123.com/success"
