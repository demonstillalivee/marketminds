"""Historical price fetching with retry + on-disk CSV caching.

Public surface: ``fetch_prices(ticker, start, end) -> pd.DataFrame``.

Caching strategy (v1, see ADR-0002):
  * Cache key = (TICKER_UPPER, start_iso, end_iso).
  * Cache file = ``~/.market_minds_cache/{TICKER}_{start}_{end}.csv``.
  * No TTL — caller can delete the cache file to force a refetch.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Final

import pandas as pd
import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

CACHE_DIR: Final[Path] = Path.home() / ".market_minds_cache"


def _cache_path(ticker: str, start: date, end: date) -> Path:
    """Return the on-disk cache path for a (ticker, start, end) tuple."""
    filename = f"{ticker.upper()}_{start.isoformat()}_{end.isoformat()}.csv"
    return CACHE_DIR / filename


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)
def _fetch_from_yfinance(ticker: str, start: date, end: date) -> pd.DataFrame:
    """Fetch raw daily prices from yfinance. Retries on transient failure.

    Raises:
        ValueError: if yfinance returns an empty frame (bad ticker, no data in range).
    """
    data: pd.DataFrame = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=True,
    )
    if data.empty:
        raise ValueError(f"No price data returned for {ticker!r} between {start} and {end}.")
    # yfinance occasionally returns MultiIndex columns even for a single ticker;
    # collapse to single-level so downstream code is simpler.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data


def fetch_prices(ticker: str, start: date, end: date) -> pd.DataFrame:
    """Fetch historical daily prices for ``ticker``, caching on disk.

    Args:
        ticker: Yahoo Finance ticker (e.g. ``"AAPL"`` or ``"RELIANCE.NS"``).
        start: First date to include (inclusive).
        end: Last date to include (exclusive, per yfinance convention).

    Returns:
        DataFrame indexed by date, with at minimum a ``Close`` column.
    """
    cache_file = _cache_path(ticker, start, end)

    if cache_file.exists():
        return pd.read_csv(cache_file, index_col=0, parse_dates=True)

    df = _fetch_from_yfinance(ticker, start, end)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_file)
    return df
