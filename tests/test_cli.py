"""Tests for the command-line interface."""

import pytest

from quickython.__main__ import main


def test_main_default(capsys: pytest.CaptureFixture[str]) -> None:
    """No args greets the world and exits 0."""
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Hello, World!\n"


def test_main_with_name_and_salutation(capsys: pytest.CaptureFixture[str]) -> None:
    """A positional name and --salutation are used in the greeting."""
    exit_code = main(["Ada", "--salutation", "Hi"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Hi, Ada!\n"


def test_main_empty_name_errors(capsys: pytest.CaptureFixture[str]) -> None:
    """An empty name triggers argparse's usage error (exit code 2)."""
    with pytest.raises(SystemExit) as excinfo:
        main(["   "])
    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "must not be empty" in captured.err
