from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import pytest
from sortedcontainers import SortedDict

if TYPE_CHECKING:
    # Note: we don't export from sortedcontainers to reduce the chance that
    # people try to import it to use as a runtime type — it's only a type
    # annotation.
    from sortedcontainers.sorteddict import SortedKeyDict


def test_constructor_references() -> None:
    def str_to_int(x: str) -> int:
        return int(x)

    @dataclass
    class Example:
        samples: SortedDict[str, float] = field(default_factory=SortedDict)
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
