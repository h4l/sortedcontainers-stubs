from __future__ import annotations

from typing import TYPE_CHECKING

from sortedcontainers import SortedDict

if TYPE_CHECKING:
    # Note: we don't export from sortedcontainers to reduce the chance that
    # people try to import it to use as a runtime type — it's only a type
    # annotation.
    from sortedcontainers.sorteddict import SortedKeyDict


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
