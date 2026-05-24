"""Unit tests for ``marketminds.data.prices``.

All tests mock yfinance — CI never hits the network. This keeps tests fast
(< 1s) and immune to upstream rate limits or API breakage.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from marketminds.data import prices


@pytest.fixture
def sample_prices_df() -> pd.DataFrame:
    """A minimal valid prices DataFrame as yfinance would return."""
    return pd.DataFrame(
        {
            "Open": [100.0, 101.0, 102.0],
            "High": [101.0, 102.0, 103.0],
            "Low": [99.0, 100.0, 101.0],
            "Close": [100.5, 101.5, 102.5],
            "Volume": [1000, 1100, 1200],
        },
        index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    )


def test_cache_path_uppercases_ticker(tmp_path, mocker: MockerFixture) -> None:
    """Cache filename normalizes the ticker to uppercase."""
    mocker.patch.object(prices, "CACHE_DIR", tmp_path)
    p = prices._cache_path("aapl", date(2024, 1, 1), date(2024, 2, 1))
    assert "AAPL" in p.name
    assert "2024-01-01" in p.name
    assert "2024-02-01" in p.name


def test_fetch_prices_writes_cache_on_miss(
    tmp_path,
    sample_prices_df: pd.DataFrame,
    mocker: MockerFixture,
) -> None:
    """On cache miss, yfinance is called once and the result is written to disk."""
    mocker.patch.object(prices, "CACHE_DIR", tmp_path)
    mocked = mocker.patch.object(prices, "_fetch_from_yfinance", return_value=sample_prices_df)

    result = prices.fetch_prices("AAPL", date(2024, 1, 1), date(2024, 2, 1))

    assert mocked.call_count == 1
    assert "Close" in result.columns
    assert len(result) == 3
    # Cache file written
    cache_file = tmp_path / "AAPL_2024-01-01_2024-02-01.csv"
    assert cache_file.exists()


def test_fetch_prices_reads_cache_on_hit(
    tmp_path,
    sample_prices_df: pd.DataFrame,
    mocker: MockerFixture,
) -> None:
    """On cache hit, yfinance is NOT called."""
    mocker.patch.object(prices, "CACHE_DIR", tmp_path)
    # Pre-populate the cache
    cache_file = tmp_path / "AAPL_2024-01-01_2024-02-01.csv"
    sample_prices_df.to_csv(cache_file)

    mocked = mocker.patch.object(prices, "_fetch_from_yfinance")
    result = prices.fetch_prices("AAPL", date(2024, 1, 1), date(2024, 2, 1))

    assert mocked.call_count == 0
    assert "Close" in result.columns
    assert len(result) == 3


def test_fetch_from_yfinance_raises_on_empty(mocker: MockerFixture) -> None:
    """An empty DataFrame from yfinance raises ValueError."""
    mocker.patch("yfinance.download", return_value=pd.DataFrame())
    with pytest.raises(ValueError, match="No price data"):
        prices._fetch_from_yfinance("BADTICKER", date(2024, 1, 1), date(2024, 2, 1))


def test_fetch_from_yfinance_flattens_multiindex(
    sample_prices_df: pd.DataFrame,
    mocker: MockerFixture,
) -> None:
    """MultiIndex columns from yfinance are flattened to single level."""
    multi_df = sample_prices_df.copy()
    multi_df.columns = pd.MultiIndex.from_product([multi_df.columns, ["AAPL"]])
    mocker.patch("yfinance.download", return_value=multi_df)

    result = prices._fetch_from_yfinance("AAPL", date(2024, 1, 1), date(2024, 2, 1))

    assert not isinstance(result.columns, pd.MultiIndex)
    assert "Close" in result.columns
