"""Idiomatic, fully typed examples to copy from.

Demonstrates a frozen dataclass and a typed function with Google-style
docstrings. Replace these with your own domain code.
"""

from dataclasses import dataclass

__all__ = ["Greeting", "greet"]


@dataclass(frozen=True, slots=True)
class Greeting:
    """An immutable greeting addressed to someone.

    Attributes:
        recipient: The name of the person being greeted.
        salutation: The greeting word to use.
    """

    recipient: str
    salutation: str = "Hello"

    def render(self) -> str:
        """Return the greeting as a display string.

        Returns:
            The formatted greeting, e.g. ``"Hello, World!"``.
        """
        return f"{self.salutation}, {self.recipient}!"


def greet(name: str, *, salutation: str = "Hello") -> str:
    """Build a greeting string for ``name``.

    Args:
        name: The recipient's name; surrounding whitespace is stripped.
        salutation: The greeting word to use.

    Returns:
        The rendered greeting.

    Raises:
        ValueError: If ``name`` is empty or only whitespace.
    """
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    return Greeting(recipient=cleaned, salutation=salutation).render()
