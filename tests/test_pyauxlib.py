#!/usr/bin/env python

"""Tests for `PyAuxLib` package."""


import pytest
from pyauxlib import pyauxlib


@pytest.fixture
def _response() -> None:
    """Sample pytest fixture."""
    # import requests
    # return requests.get('https://github.com/psolsfer/cookiecutter-pypackage-poet')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
