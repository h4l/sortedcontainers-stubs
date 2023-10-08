import re

import pytest
from sortedcontainers import SortedSet


def test_contains() -> None:
    s = SortedSet(["a", "b"])
    with pytest.raises(TypeError):
        [] in s  # type: ignore[operator]
    assert "a" in s


def test_element_addition_type_safety() -> None:
    # Because the implementation needs to compare elements for order, it does
    # not support mixing element types that cannot be compared.
    with pytest.raises(
        TypeError,
        match=re.escape("'<' not supported between instances of"),
    ):
        s2 = SortedSet([1, 2])
        SortedSet(["a", "b"]) | s2  # type: ignore[operator]

    # This is different to regular sets, which only hash and compare for
    # equality, so the element types can be mixed.
    with pytest.raises(
        TypeError,
        match=re.escape("unsupported operand type(s) for |: 'set' and 'list'"),
    ):
        {"a", "b"} | [1, 2]  # type: ignore[operator]
    assert {"a", "b"} | {1, 2} == {"a", "b", 1, 2}
