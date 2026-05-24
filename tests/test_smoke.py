"""Smoke tests — confirm package imports and CI plumbing works."""

import marketminds


def test_package_imports() -> None:
    """Package can be imported."""
    assert marketminds is not None


def test_version_is_set() -> None:
    """Version string is present and follows semver-ish."""
    assert hasattr(marketminds, "__version__")
    assert isinstance(marketminds.__version__, str)
    assert len(marketminds.__version__.split(".")) >= 2
