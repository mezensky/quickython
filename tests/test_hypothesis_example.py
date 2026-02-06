"""Example of property-based testing with Hypothesis.

This demonstrates how to use Hypothesis for automated test generation.
Uncomment and adapt these tests for your actual use cases.
"""

from hypothesis import given
from hypothesis import strategies as st


# Example 1: Test that reversing a string twice gives the original
@given(st.text())
def test_reverse_twice_is_identity(text: str) -> None:
    """Reversing a string twice should return the original string.

    Args:
        text: A randomly generated string from Hypothesis.
    """
    reversed_once = text[::-1]
    reversed_twice = reversed_once[::-1]
    assert reversed_twice == text


# Example 2: Test mathematical property
@given(st.integers(), st.integers())
def test_addition_is_commutative(a: int, b: int) -> None:
    """Addition should be commutative: a + b = b + a.

    Args:
        a: A randomly generated integer.
        b: Another randomly generated integer.
    """
    assert a + b == b + a


# Example 3: Test with constrained inputs
@given(st.lists(st.integers(), min_size=1, max_size=100))
def test_sorted_list_properties(numbers: list[int]) -> None:
    """Test properties of sorted lists.

    Args:
        numbers: A randomly generated list of integers.
    """
    sorted_numbers = sorted(numbers)

    # Property 1: Sorted list has same length
    assert len(sorted_numbers) == len(numbers)

    # Property 2: All elements are still present
    assert set(sorted_numbers) == set(numbers)

    # Property 3: Elements are in non-decreasing order
    for i in range(len(sorted_numbers) - 1):
        assert sorted_numbers[i] <= sorted_numbers[i + 1]
