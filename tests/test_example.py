"""Tests for the example module: fixtures, parametrize, and mocking."""

import pytest
from pytest_mock import MockerFixture

from quickython import example
from quickython.example import Greeting, greet


@pytest.fixture
def default_greeting() -> Greeting:
    """A reusable Greeting fixture."""
    return Greeting(recipient="World")


def test_greeting_render(default_greeting: Greeting) -> None:
    """A Greeting renders as 'salutation, recipient!'."""
    assert default_greeting.render() == "Hello, World!"


def test_greeting_is_frozen(default_greeting: Greeting) -> None:
    """Greeting instances are immutable."""
    with pytest.raises(AttributeError):
        setattr(default_greeting, "recipient", "Mars")


@pytest.mark.parametrize(
    ("name", "salutation", "expected"),
    [
        ("World", "Hello", "Hello, World!"),
        ("  Ada ", "Hi", "Hi, Ada!"),
        ("Bob", "Hey", "Hey, Bob!"),
    ],
)
def test_greet_variants(name: str, salutation: str, expected: str) -> None:
    """greet() trims whitespace and applies the salutation."""
    assert greet(name, salutation=salutation) == expected


@pytest.mark.parametrize("bad", ["", "   ", "\t\n"])
def test_greet_rejects_empty(bad: str) -> None:
    """greet() raises ValueError on empty/whitespace names."""
    with pytest.raises(ValueError, match="must not be empty"):
        greet(bad)


def test_greet_delegates_to_render(mocker: MockerFixture) -> None:
    """greet() builds a Greeting and calls its render() (mock/spy example)."""
    spy = mocker.spy(example.Greeting, "render")
    result = greet("World")
    spy.assert_called_once()
    assert result == "Hello, World!"
