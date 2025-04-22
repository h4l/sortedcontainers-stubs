from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Container, TypeVar
from typing_extensions import Never, assert_type

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


def test_constructor_cannot_be_subscripted_with_1_param() -> None:
    # Because __new__'s overloads use 0, 1 or 2 two generic types for different
    # overloads, mypy gets confused and complains that specifying 1 type arg is
    # too few, and 2 is too many. So it's not possible to subscript the
    # constructor. Instead, specify the type of the thing the constructor is
    # assigned to.
    _ = SortedList[int]()  # type: ignore[misc] # Type application has too few types (2 expected) # noqa: E501

    # It's only the constructor that has problems
    sl: SortedList[int] = SortedList([3, 2, 1])
    assert list(assert_type(sl, SortedList[int])) == [1, 2, 3]


@pytest.mark.xfail
def test_constructor_cannot_be_subscripted_with_2_params() -> None:
    # Too many generic type params

    # FIXME: this used to be a type error but causes mypy 1.15.0 to crash with
    #        an internal error.
    # assert_type(SortedList[None, int](), Any)  # type: ignore[misc] # Type application has too many types (1 expected) # noqa: E501
    assert False, "FIXME"


def test_constructor() -> None:
    assert_type(
        SortedList(), SortedList[Never]  # pyright: ignore[reportAssertTypeFailure]
    )

    assert_type(SortedList([1, 2, 3]), SortedList[int])

    l: SortedList[int] = SortedList()
    assert_type(l, SortedList[int])

    def str_to_int(x: str) -> int:
        return int(x)

    # SortedList constructor returns SortedKeyList when a key function is passed
    assert_type(SortedList(None, str_to_int), SortedKeyList[str, int])
    assert_type(SortedList(key=str_to_int), SortedKeyList[str, int])


def test_SortedKeyList_constructor() -> None:
    # SortedKeyList constructor always returns SortedKeyList
    assert_type(SortedKeyList[int, int](), SortedKeyList[int, int])

    assert_type(
        SortedKeyList(),  # pyright: ignore[reportAssertTypeFailure]
        SortedKeyList[Never, Never],
    )

    assert_type(SortedKeyList([1, 2, 3]), SortedKeyList[int, int])

    _l: SortedKeyList[int, int] = SortedKeyList()  # noqa: F841

    # Can create a SortedList with a non-comparable type like this
    _l2: SortedList[object] = SortedKeyList([[], object()], key=id)  # noqa: F841

    def str_to_int(x: str) -> int:
        return int(x)

    assert_type(SortedKeyList(None, str_to_int), SortedKeyList[str, int])

    assert_type(SortedKeyList(key=str_to_int), SortedKeyList[str, int])


def test_constructor_references() -> None:
    create: Callable[[], SortedList[int]] = SortedList
    assert create() == SortedList()

    @dataclass
    class Example:
        things1: SortedList[str] = field(  # pyright: ignore[reportUnknownVariableType]
            default_factory=SortedList
        )
        things2: SortedKeyList[type, str] = field(
            default_factory=lambda: SortedKeyList(key=str)
        )

    e = Example()
    e.things1.add("a")
    e.things2.add(str)
    e.things2.add(int)

    def str_to_int(x: str) -> int:
        if not isinstance(x, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"x must be str, not {type(x)}")
        return int(x)

    # Wrong key type is (static and runtime) type error
    @dataclass
    class InvalidExample:
        named_samples: SortedKeyList[float, int] = field(
            default_factory=lambda: SortedKeyList(key=str_to_int)  # type: ignore[arg-type] # noqa: E501
        )

    ex = InvalidExample()
    with pytest.raises(TypeError):
        ex.named_samples.add(1.5)


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


@pytest.mark.xfail(raises=AssertionError)
def test_regression_issue10_constructor_key_only() -> None:
    """
    SortedList constructor is incorrectly typed to allow a positional key
    argument with no `iterable` arg. This should be a static type error.

    https://github.com/h4l/sortedcontainers-stubs/issues/10
    """

    def key_fn(arg: int) -> str:
        return str(arg)

    with pytest.raises(TypeError, match=r"'function' object is not iterable"):
        # FIXME: this should be a type error
        SortedList(key_fn)

    with pytest.raises(TypeError, match=r"'function' object is not iterable"):
        # FIXME: this should be a type error
        SortedKeyList(key_fn)

    assert False, "FIXME"


@pytest.mark.xfail(raises=AssertionError)
def test_regression_issue12_sortedkeylist_constructor_key_none() -> None:
    """
    SortedKeyList constructor is incorrectly typed to allow `key` to be None.
    In fact `key` must be a callable, None is not converted to the identity
    function, despite the default key value being identity if not provided.

    https://github.com/h4l/sortedcontainers-stubs/issues/12
    """

    with pytest.raises(TypeError, match=r"'NoneType' object is not callable"):
        # FIXME: should be a type error
        SortedKeyList[Any, Any](key=None).add(1)

    assert False, "FIXME"
