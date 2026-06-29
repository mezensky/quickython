"""Tests for the sample module."""

import pytest

from quickython.sample import samplefunction


def test_samplefunction_prints_hey(capsys: pytest.CaptureFixture[str]) -> None:
    """Samplefunction prints 'Hey' to stdout."""
    samplefunction()
    captured = capsys.readouterr()
    assert captured.out == "Hey\n"


def test_samplefunction_returns_none() -> None:
    """Samplefunction returns None."""
    assert samplefunction() is None  # type: ignore[func-returns-value]


def test_samplefunction_called_multiple_times(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Samplefunction can be called repeatedly."""
    samplefunction()
    samplefunction()
    captured = capsys.readouterr()
    assert captured.out == "Hey\nHey\n"
