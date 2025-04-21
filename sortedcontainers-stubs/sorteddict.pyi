from collections.abc import (
    Callable,
    Hashable,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    MutableMapping,
    Sequence,
    ValuesView,
)
from typing import Any, Generic, TypeVar, overload
from typing_extensions import Never, Self, TypeAlias

from _typeshed import SupportsKeysAndGetItem

from ._typing import SupportsHashableAndRichComparison

__all__ = [
    "KeyFunc",
    "SortedKeyDict",
    "SortedDict",
    "SupportsHashableAndRichComparison",
]

# Without a key fn, Keys must be hashable and comparable
# With a key fn, Keys must be hashable, and the fn converts them to Comparable
# Values can be anything

_T = TypeVar("_T")
_KT = TypeVar("_KT", bound=Hashable)  # Key type.
_VT = TypeVar("_VT")  # Value type.
_KT_co = TypeVar("_KT_co", covariant=True, bound=Hashable)
_VT_co = TypeVar("_VT_co", covariant=True)
_OrderT = TypeVar(
    "_OrderT", bound=SupportsHashableAndRichComparison, contravariant=True
)

KeyFunc: TypeAlias = Callable[[_KT], _OrderT]

class SortedDict(MutableMapping[_KT, _VT]):
    # mypy 1.5.1 complains about overlapping overloaded function signatures with
    # incompatible return types. This seems to be because the signatures using
    # kwargs can would overlap when no kwargs are present, but there's no way to
    # type a non-empty kwargs param.

    @overload
    def __new__(
        cls,
    ) -> SortedDict[_KT, _VT]: ...
    @overload
    def __new__(
        cls,
        __entries: Iterable[tuple[_OrderT, _VT]] | SupportsKeysAndGetItem[_OrderT, _VT],
        /,
    ) -> SortedDict[_OrderT, _VT]: ...
    @overload
    def __new__(
        cls,
        __entries: Iterable[tuple[str, _VT]] | SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT,
    ) -> SortedDict[str, _VT]: ...
    @overload
    def __new__(
        cls,
        /,
        **kwargs: _VT,
    ) -> SortedDict[str, _VT]: ...
    @overload
    def __new__(
        cls,
        __key: KeyFunc[str, _OrderT],
        /,
        **kwargs: _VT,
    ) -> SortedKeyDict[str, _VT, _OrderT]: ...
    @overload
    def __new__(
        cls,
        __key: KeyFunc[str, _OrderT],
        __entries: Iterable[tuple[str, _VT]] | SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT,
    ) -> SortedKeyDict[str, _VT, _OrderT]: ...
    @overload
    def __new__(
        cls,
        __key: KeyFunc[_KT, _OrderT],
        /,
    ) -> SortedKeyDict[_KT, _VT, _OrderT]: ...
    @overload
    def __new__(
        cls,
        __key: KeyFunc[_KT, _OrderT],
        __entries: Iterable[tuple[_KT, _VT]] | SupportsKeysAndGetItem[_KT, _VT],
        /,
    ) -> SortedKeyDict[_KT, _VT, _OrderT]: ...
    @property
    def key(self) -> KeyFunc[_KT, Any] | None: ...
    @property
    def iloc(self) -> SortedKeysView[_KT]: ...
    def clear(self) -> None: ...
    def __delitem__(self, key: _KT) -> None: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    def __iter__(self) -> Iterator[_KT]: ...
    def __len__(self) -> int: ...
    def __reversed__(self) -> Iterator[_KT]: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
    def copy(self) -> Self: ...
    def __copy__(self) -> Self: ...
    @classmethod
    @overload
    def fromkeys(cls, seq: Iterable[_OrderT]) -> SortedDict[_OrderT, None]: ...
    @classmethod
    @overload
    def fromkeys(
        cls, seq: Iterable[_OrderT], value: _VT
    ) -> SortedDict[_OrderT, _VT]: ...
    def keys(self) -> SortedKeysView[_KT]: ...
    def items(self) -> SortedItemsView[_KT, _VT]: ...
    def values(self) -> SortedValuesView[_VT]: ...
    @overload
    def pop(self, key: _KT, /) -> _VT: ...
    @overload
    def pop(self, key: _KT, /, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT, /, default: _T) -> _VT | _T: ...
    def popitem(self, index: int = ...) -> tuple[_KT, _VT]: ...
    def peekitem(self, index: int = ...) -> tuple[_KT, _VT]: ...
    @overload
    def setdefault(self: MutableMapping[_KT, _T | None], key: _KT) -> _T | None: ...
    # Our overload matches the implementation's permitted arguments, which allows keyword args, unlike SortedDict.
    @overload
    def setdefault(  # pyright: ignore [reportIncompatibleMethodOverride]
        self, key: _KT, default: _VT
    ) -> _VT: ...
    # Our override of update is strictly incompatible in that we only allow
    # kwargs when _KT is str. This is consistent with dict()'s constructor
    # typing, and allowing kwargs with non-str _KT causes TypeErrors at runtime.
    @overload  # type: ignore[override]
    def update(self) -> None: ...
    @overload
    def update(
        self: SortedDict[str, _VT],
        map: SupportsKeysAndGetItem[str, _VT],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def update(self, map: SupportsKeysAndGetItem[_KT, _VT], /) -> None: ...
    @overload
    def update(
        self: SortedDict[str, _VT],
        iterable: Iterable[tuple[str, _VT]],
        /,
        **kwargs: _VT,
    ) -> None: ...
    @overload
    def update(self, iterable: Iterable[tuple[_KT, _VT]], /) -> None: ...
    @overload
    def update(self: SortedDict[str, _VT], **kwargs: _VT) -> None: ...  # type: ignore[override,unused-ignore]
    def __reduce__(
        self,
    ) -> tuple[
        type[SortedDict[_KT, _VT]],
        tuple[Callable[[_KT], Any], list[tuple[_KT, _VT]]],
    ]: ...
    def bisect_left(self, value: _KT) -> int: ...
    def bisect_right(self, value: _KT) -> int: ...
    def bisect(self, value: _KT) -> int: ...
    def index(
        self, value: _KT, start: int | None = ..., stop: int | None = ...
    ) -> int: ...
    def islice(
        self,
        start: int | None = ...,
        stop: int | None = ...,
        reverse: bool = ...,
    ) -> Iterator[_KT]: ...
    def irange(
        self,
        minimum: _KT | None = ...,
        maximum: _KT | None = ...,
        inclusive: tuple[bool, bool] = ...,
        reverse: bool = ...,
    ) -> Iterator[_KT]: ...
    # Despite being named as a private method, this is documented in the API.
    def _reset(self, load: int) -> None: ...

class SortedKeyDict(SortedDict[_KT, _VT], Generic[_KT, _VT, _OrderT]):
    # This is a stub-only type, it doesn't exist at runtime, so the constructor
    # returns Never to prevent creating instances directly. This also seems to
    # cause a type error if the fromkeys() factory is used from this class, so
    # that doesn't need to be hobbled like this.
    def __new__(
        cls,
        *,
        this_type_only_exists_as_a_type_annotation_it_cannot_be_created_directly: Never,
    ) -> Never: ...
    @property
    def key(self) -> KeyFunc[_KT, _OrderT]: ...
    def irange_key(
        self,
        min_key: _OrderT | None = ...,
        max_key: _OrderT | None = ...,
        inclusive: tuple[bool, bool] = ...,
        reverse: bool = ...,
    ) -> Iterator[_KT]: ...
    def bisect_key_left(self, key: _OrderT) -> int: ...
    def bisect_key_right(self, key: _OrderT) -> int: ...
    def bisect_key(self, key: _OrderT) -> int: ...

class SortedKeysView(KeysView[_KT_co], Sequence[_KT_co]):
    @overload
    def __getitem__(self, index: int) -> _KT_co: ...
    @overload
    def __getitem__(self, index: slice) -> list[_KT_co]: ...
    def __delitem__(self, index: int | slice) -> None: ...

class SortedItemsView(ItemsView[_KT_co, _VT_co], Sequence[tuple[_KT_co, _VT_co]]):
    def __iter__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
    @overload
    def __getitem__(self, index: int) -> tuple[_KT_co, _VT_co]: ...
    @overload
    def __getitem__(self, index: slice) -> list[tuple[_KT_co, _VT_co]]: ...
    def __delitem__(self, index: int | slice) -> None: ...

class SortedValuesView(ValuesView[_VT_co], Sequence[_VT_co]):
    @overload
    def __getitem__(self, index: int) -> _VT_co: ...
    @overload
    def __getitem__(self, index: slice) -> list[_VT_co]: ...
    def __delitem__(self, index: int | slice) -> None: ...
