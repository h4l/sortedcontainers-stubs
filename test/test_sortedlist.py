from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Callable, Container, TypeVar

import pytest
from sortedcontainers import SortedKeyList, SortedList

T = TypeVar("T")

not_py38 = pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 or higher"
)


def use_sortedlist(type_: type[T], sl: SortedList[T], /) -> None:
    assert isinstance(sl, SortedList)


def use_sorted_list(type_: type[T], sl: SortedList[T], /) -> None:
    assert isinstance(sl, SortedList)


def test_creation_py38() -> None:
    use_sortedlist(int, SortedList([4, 1, 2]))
    use_sortedlist(int, SortedList([4, 1, 2], key=None))
    use_sortedlist(str, SortedList(["4", "1", "2"], key=int))
    use_sortedlist(object, SortedList(key=id))


def test_constructor_references() -> None:
    create: Callable[[], SortedList[int]] = SortedList
    assert create() == SortedList()

    @dataclass
    class Example:
        things1: SortedList[str] = field(default_factory=SortedList)
        things2: SortedKeyList[type, str] = field(
            default_factory=lambda: SortedKeyList(key=str)
        )

    e = Example()
    e.things1.add("a")
    e.things2.add(str)
    e.things2.add(int)


def test_unavoidable_type_violations() -> None:
    # The implementation expects that __contains__ only receives values it can
    # compare to elements, but the Container superclass types it to accept
    # object. As a compromise, we type the method according to the
    # implementation on SortedList, but assigning a SortedList to a more general
    # collection type opens the possibility of a runtime type error.
    sl = SortedList([1, 2, 3])
    c: Container[int] = sl

    with pytest.raises(TypeError):
        # This is a type error when using SortedList directly
        "42" in sl  # type: ignore[operator]

    with pytest.raises(TypeError):
        # Not a type error when using Container (for mypy at least, pyright uses
        # the element type, which is not what the pyi files actually declare).
        c.__contains__("42")  # pyright: ignore

    with pytest.raises(TypeError):
        # mypy can detect a possible error via comparison-overlap though
        "42" in c  # type: ignore[comparison-overlap]

    # __new__ is typed to return SortedList[Any] when no args are given because
    # support for a single generic param in the return position is variable.
    # MyPy supports it, but pyright doesn't. It doesn't seem to be explicitly
    # supported by typing PEPs.
    # As a result, we can create empty SortedList with non-comparable types,
    # which will fail when values are added at runtime.
    types: SortedList[type] = SortedList()
    types.add(str)
    with pytest.raises(TypeError):
        types.add(str)


def test_operators() -> None:
    s = SortedList([1])
    assert s + s == [1, 1]
    s += s
    assert s == [1] * 2
    assert s * 2 == [1] * 4
    assert 2 * s == [1] * 4
    s *= 2
    assert s == [1] * 4

    s2 = SortedList([2])
    assert s < s2
    assert s <= s2
    assert s2 > s
    assert s2 >= s
    assert s == s
    assert s != s2
