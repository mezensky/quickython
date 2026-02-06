"""Tests for sample module."""

from typing import Any

from quickython.sample import samplefunction


def test_samplefunction_prints_hey(capsys: Any) -> None:
    """Test that samplefunction prints 'Hey' to stdout."""
    samplefunction()
    captured = capsys.readouterr()
    assert captured.out == "Hey\n"


def test_samplefunction_returns_none() -> None:
    """Test that samplefunction returns None."""
    assert samplefunction() is None  # type: ignore[func-returns-value]


def test_samplefunction_called_multiple_times(capsys: Any) -> None:
    """Test that samplefunction can be called multiple times."""
    samplefunction()
    samplefunction()
    captured = capsys.readouterr()
    assert captured.out == "Hey\nHey\n"
