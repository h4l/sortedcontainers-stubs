from __future__ import annotations

import sys
from typing import Container, TypeVar

import pytest
from sortedcontainers import SortedList

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


@not_py38
def test_creation() -> None:
    # It's possible to subscript SortedList to specify types, despite the actual
    # implementation not being typed. SortedList needs two parameters, because
    # the constructor can return a SortedKeyList which has two. Best not to do
    # this and infer the type via assignment or arguments instead.
    use_sortedlist(int, SortedList[None, int]([]))
    sl = SortedList[None, int]()
    sl.add(1)
    assert sl == [1]


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
        # Not a type error when using Container
        c.__contains__("42")

    with pytest.raises(TypeError):
        # mypy can detect a possible error via comparison-overlap though
        "42" in c  # type: ignore[comparison-overlap]


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
