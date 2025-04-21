from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable
from typing_extensions import Never, assert_type

import pytest
from sortedcontainers import SortedSet

if TYPE_CHECKING:
    from sortedcontainers.sortedset import SortedKeySet


def test_constructor() -> None:
    assert_type(
        SortedSet(), SortedSet[Never]  # pyright: ignore[reportAssertTypeFailure]
    )
    assert_type(SortedSet[int](), SortedSet[int])

    assert_type(SortedSet([1, 2, 3]), SortedSet[int])

    l: SortedSet[int] = SortedSet()
    assert_type(l, SortedSet[int])

    def str_to_int(x: str) -> int:
        return int(x)

    assert_type(SortedSet(None, str_to_int), "SortedKeySet[str, int]")

    assert_type(SortedSet(iterable=None, key=str_to_int), "SortedKeySet[str, int]")

    assert_type(SortedSet(key=str_to_int), "SortedKeySet[str, int]")


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
        things1: SortedSet[str] = field(  # pyright: ignore[reportUnknownVariableType]
            default_factory=SortedSet
        )
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


@pytest.mark.xfail(raises=AssertionError)
def test_regression_issue10_constructor_key_only() -> None:
    """
    SortedSet constructor is incorrectly typed to allow a positional key
    argument with no `iterable` arg. This should be a static type error.

    https://github.com/h4l/sortedcontainers-stubs/issues/10
    """

    def key_fn(arg: int) -> str:
        return str(arg)

    with pytest.raises(TypeError, match=r"'function' object is not iterable"):
        # FIXME: this should be a type error
        SortedSet(key_fn)

    assert False, "FIXME"
