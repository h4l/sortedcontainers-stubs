from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, cast
from typing_extensions import Never, assert_type

import pytest
from sortedcontainers import SortedDict

if TYPE_CHECKING:
    # Note: we don't export from sortedcontainers to reduce the chance that
    # people try to import it to use as a runtime type — it's only a type
    # annotation.
    from _typeshed import SupportsKeysAndGetItem
    from sortedcontainers.sorteddict import SortedKeyDict


def test_constructor() -> None:
    s, i = cast(str, "a"), cast(int, 1)

    assert_type(SortedDict(), SortedDict[Never, Never])  # pyright: ignore
    assert_type(SortedDict[str, int](), SortedDict[str, int])
    assert_type(SortedDict([(s, i)]), SortedDict[str, int])
    assert_type(SortedDict({"a": 1}), SortedDict[str, int])
    assert_type(SortedDict([("a", 1)], b=2), SortedDict[str, int])
    assert_type(SortedDict({"a": 1}, b=2), SortedDict[str, int])
    assert_type(SortedDict(a=1), SortedDict[str, int])

    d: SortedDict[str, int] = SortedDict()
    assert_type(d, SortedDict[str, int])

    def str_key_fn(x: str) -> int:
        return int(x) if x.isdigit() else 0

    def key_fn(tup: tuple[int, int]) -> int:
        a, b = tup
        return a + b

    assert_type(SortedDict[str, float](str_key_fn), "SortedKeyDict[str, float, int]")
    assert_type(
        SortedDict(str_key_fn),  # pyright: ignore [reportAssertTypeFailure]
        "SortedKeyDict[str, Never, int]",
    )

    assert_type(SortedDict(str_key_fn, a=1.2), "SortedKeyDict[str, float, int]")
    assert_type(SortedDict(str_key_fn, [(s, 1.2)]), "SortedKeyDict[str, float, int]")
    assert_type(SortedDict(str_key_fn, {"01": 1.2}), "SortedKeyDict[str, float, int]")
    assert_type(
        SortedDict(str_key_fn, [("01", 1.2)], a=1.2), "SortedKeyDict[str, float, int]"
    )
    assert_type(
        SortedDict(str_key_fn, {"01": 1.2}, a=1.2), "SortedKeyDict[str, float, int]"
    )

    assert_type(
        SortedDict(key_fn, [((1, 1), 1.2)]),
        "SortedKeyDict[tuple[int, int], float, int]",
    )

    # mypy and pylance can't resolve the overload when using a dict argument for
    # some reason.
    assert [*SortedDict(key_fn, {(1, 1): 1.2, (2, -3): 1.0}).items()] == [  # type: ignore[comparison-overlap,arg-type] # noqa: E501
        ((2, -3), 1.0),
        ((1, 1), 1.2),
    ]
    # But they can when explicitly annotating the SortedDict type
    assert_type(
        SortedDict[tuple[int, int], float](key_fn, {(1, 1): 1.2}),
        "SortedKeyDict[tuple[int, int], float, int]",
    )
    # They also resolve it when using SupportsKeysAndGetItem explicitly...
    assert_type(
        SortedDict(
            key_fn,
            cast("SupportsKeysAndGetItem[tuple[int, int], float]", {(1, 1): 1.2}),
        ),
        "SortedKeyDict[tuple[int, int], float, int]",
    )


def test_constructor_references() -> None:
    _create_sd: Callable[[], SortedDict[str, float]]
    # pyright doesn't allow bare references without explicit annotations, as the
    # params are Any/Unknown.
    _create_sd = SortedDict  # pyright: ignore[reportAssignmentType]
    _create_sd = SortedDict[str, float]
    assert _create_sd() == SortedDict()

    def str_to_int(x: str) -> int:
        return int(x)

    @dataclass
    class Example:
        samples: SortedDict[str, float] = field(default_factory=SortedDict[str, float])
        named_samples: SortedKeyDict[str, float, int] = field(
            default_factory=lambda: SortedDict(str_to_int)
        )

    e = Example()
    e.samples["b"] = 1.2
    e.samples["a"] = 5.0
    assert list(e.samples) == ["a", "b"]
    e.named_samples["40"] = 1.2
    e.named_samples["5"] = 5.0
    assert list(e.named_samples) == ["5", "40"]


def test_constructor_errors() -> None:
    def str_to_int_key(x: str) -> int:
        assert isinstance(x, str)
        return int(x)

    def float_to_int_key(x: float) -> int:
        assert isinstance(x, (float, int))
        return int(x)

    # key func does not accept element type
    with pytest.raises(AssertionError):
        SortedDict(str_to_int_key, [(1, "x")])  # type: ignore[arg-type]

    # kwargs imply str keys — can't mix key types
    with pytest.raises(AssertionError):
        SortedDict(float_to_int_key, a="x")  # type: ignore[arg-type]

    with pytest.raises(
        TypeError, match=r"'<' not supported between instances of 'str' and 'int'"
    ):
        SortedDict([(1, "x")], a="x")  # type: ignore[list-item]

    with pytest.raises(AssertionError):
        SortedDict(float_to_int_key, [(1.2, "x")], a="x")  # type: ignore[arg-type,list-item] # noqa: E501

    # Without a key func, keys must be hashable and comparable.

    # Comparable but not hashable:
    with pytest.raises(TypeError, match=r"unhashable type: 'list'"):
        SortedDict([([], "x")])  # type: ignore[type-var]

    # Hashable but not comparable:
    with pytest.raises(
        TypeError, match=r"'<' not supported between instances of 'object' and 'object'"
    ):
        SortedDict([(object(), "x"), (object(), "y")])  # type: ignore[type-var]

    # With a key func, keys only need to be hashable:

    # Comparable but not hashable:
    with pytest.raises(TypeError, match=r"unhashable type: 'list'"):
        SortedDict(id, [([], "x")])  # type: ignore[arg-type]

    # Hashable but not comparable, not an error:
    assert set(SortedDict(id, [(object(), "x"), (object(), "y")]).values()) == {
        "x",
        "y",
    }


def test_sorted_key_dict() -> None:
    def str_to_int(x: str) -> int:
        return int(x)

    # SortedKeyDict doesn't exist at runtime, but describes the subtype of
    # SortedDict that SortedDict() returns when a key function is used.
    key_dict: SortedKeyDict[str, float, int] = SortedDict(
        str_to_int, {"2": 12.3, "10": 44.2}
    )
    assert key_dict.key is str_to_int
    assert key_dict.bisect_key_left(3) == 1

    sorted_dict: SortedDict[str, float] = SortedDict({"2": 12.3, "10": 44.2})
    assert sorted_dict.key is None
    assert not hasattr(sorted_dict, "bisect_key_left")


def test_unavoidable_type_violations() -> None:
    # See SortedList's constructor (__new__()) for more on the same issue.
    # We can't constrain the key type to be hashable & orderable when no initial
    # values are specified.
    broken: SortedDict[type, int] = SortedDict()
    broken[str] = 42
    with pytest.raises(TypeError):
        broken[bytes] = 12
