"""Module containing currency conversion methods."""

from decimal import Decimal
import requests
import numpy as np
import pandas as pd
from type_aliases import Bitcoin, Satoshi


def _get_btc_rate(fiat: str) -> Decimal:
    """Uses the Coin Desk API to retrieve the BTC rate in a given fiat currency.

    Args:
        fiat: The fiat currency ticker; can be USD, GBP or EUR.
    Returns:
        The BTC rate in the fiat currency supplied.
    """
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    data = response.json()
    rate = Decimal(data["bpi"][fiat]["rate"].replace(",", ""))
    return rate


def btc_to_sats(value_btc: Bitcoin) -> Satoshi:
    """Converts BTC to Sats.

    Args:
        value_btc: The value in BTC.
    Returns:
        The value in Sats.
    """
    return value_btc * Decimal(1e8)


def sats_to_btc(value_sats: Satoshi) -> Bitcoin:
    """Converts Sats to BTC.

    Args:
        value_sats: The value in Sats.
    Returns:
        The value in BTC.
    """
    return value_sats * Decimal(1e-8)


def btc_to_fiat(value_btc: Bitcoin, fiat: str) -> Decimal:
    """Converts a BTC amount to a supplied fiat.

    Args:
        value_btc: The value in BTC.
        fiat: The currency to convert to.
    Returns:
        The value in fiat.
    """
    rate = _get_btc_rate(fiat)
    return value_btc * rate


def fiat_to_btc(value_fiat: Decimal, fiat: str) -> Bitcoin:
    """Converts a fiat amount into a BTC value.

    Args:
        value_fiat: The value in fiat.
        fiat: The fiat ticker.
    Returns:
        The BTC amount of the fiat.
    """
    rate = _get_btc_rate(fiat)
    return value_fiat / rate


def sats_to_fiat(value_sats: Satoshi, fiat: str) -> Decimal:
    """Converts a sats amount into a fiat value.

    Args:
        value_sats: The value in Sats.
        fiat: The fiat ticker.
    Returns:
        The Sats amount of the fiat.
    """
    value_btc = sats_to_btc(value_sats)
    value_fiat = btc_to_fiat(value_btc, fiat)
    return value_fiat


def fiat_to_sats(value_fiat: Decimal, fiat: str) -> Satoshi:
    """Converts and returns a fiat value into Sats.

    Args:
        value_fiat: The amount of fiat to convert.
        fiat: The fiat ticker.
    Returns:
        The amount in Sats.
    """
    value_btc = fiat_to_btc(value_fiat, fiat)
    value_sat = btc_to_sats(value_btc)
    return value_sat
