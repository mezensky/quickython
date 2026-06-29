"""Property-based tests for the example module using Hypothesis.

These demonstrate asserting *properties* that hold for all inputs, instead of
hand-picked cases. Adapt the strategies and properties to your own code.
"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from quickython.example import Greeting, greet

# Text that is still non-empty after stripping (greet rejects blank names).
nonblank_text = st.text(min_size=1).filter(lambda s: s.strip())


@given(recipient=st.text(), salutation=st.text())
def test_greeting_render_matches_format(recipient: str, salutation: str) -> None:
    """Greeting.render() formats as 'salutation, recipient!' for any text."""
    greeting = Greeting(recipient=recipient, salutation=salutation)
    assert greeting.render() == f"{salutation}, {recipient}!"


@given(name=nonblank_text, salutation=st.text())
def test_greet_embeds_stripped_name(name: str, salutation: str) -> None:
    """greet() applies the salutation and the whitespace-stripped name."""
    result = greet(name, salutation=salutation)
    assert result == f"{salutation}, {name.strip()}!"
    assert name.strip() in result


@given(blank=st.text(alphabet=" \t\n\r\f\v"))
def test_greet_rejects_blank_names(blank: str) -> None:
    """greet() raises ValueError for any empty or whitespace-only name."""
    with pytest.raises(ValueError, match="must not be empty"):
        greet(blank)
