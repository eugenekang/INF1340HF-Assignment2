#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]
    assert decide("test_lowercase.json", "watchlist.json", "countries.json") == ["Accept"]


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")
        decide("", "watchlist.json", "countries.json")
        decide("test_returning_citizen.json", "watchlist.json", "")

def test_empty():
    assert decide("test_emptyname.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_emptycountry.json", "watchlist.json", "countries.json") == ["Reject"]

def test_wronginput():
    assert decide("test_wrongpassport.json", "watchlist.json", "countries.json") == ["Reject"]
    assert decide("test_wrongformat.json", "watchlist.json", "countries.json") == ["Reject"]

def test_wrongvisa():
    assert decide("test_wrongvisa.json", "watchlist.json", "countries.json") == ["Reject"]

