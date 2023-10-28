from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

import pytest
from sortedcontainers import SortedSet

if TYPE_CHECKING:
    from sortedcontainers.sortedset import SortedKeySet


def test_contains() -> None:
    s = SortedSet(["a", "b"])
    with pytest.raises(TypeError):
        [] in s  # type: ignore[operator]
    assert "a" in s


def test_constructor_references() -> None:
    create: Callable[[], SortedSet[int]] = SortedSet
    assert create() == SortedSet()

    @dataclass
    class Example:
        things1: SortedSet[str] = field(default_factory=SortedSet)
        things2: SortedKeySet[type, str] = field(
            default_factory=lambda: SortedSet(key=str)
        )

    e = Example()
    e.things1.add("a")
    e.things2.add(str)
    e.things2.add(int)


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


def test_unavoidable_type_violations() -> None:
    # See SortedList's constructor (__new__()) for more on the same issue.
    # We can't constrain the key type to be hashable & orderable when no initial
    # values are specified.
    broken: SortedSet[type] = SortedSet()
    broken.add(str)
    with pytest.raises(TypeError):
        broken.add(bytes)
