from collections.abc import Callable, Hashable, Iterable, Iterator, MutableSet, Sequence
from collections.abc import Set as AbstractSet
from typing import Any, Generic, TypeVar, overload
from typing_extensions import Never, Self, TypeAlias

from ._typing import SupportsHashableAndRichComparison

__all__ = [
    "KeyFunc",
    "SortedKeySet",
    "SortedSet",
    "SupportsHashableAndRichComparison",
]

_T = TypeVar("_T", bound=Hashable)
_OrderT = TypeVar("_OrderT", bound=SupportsHashableAndRichComparison)
KeyFunc: TypeAlias = Callable[[_T], _OrderT]

class SortedSet(MutableSet[_T], Sequence[_T]):
    @overload
    def __new__(cls, iterable: Iterable[_OrderT]) -> SortedSet[_OrderT]: ...
    @overload
    def __new__(cls, key: KeyFunc[_T, _OrderT]) -> SortedKeySet[_T, _OrderT]: ...
    @overload
    def __new__(cls, iterable: None = ..., key: None = ...) -> SortedSet[_OrderT]: ...
    @overload
    def __new__(cls, iterable: Iterable[_OrderT], key: None) -> SortedSet[_OrderT]: ...
    @overload
    def __new__(
        cls,
        iterable: Iterable[_T] | None,
        key: KeyFunc[_T, _OrderT],
    ) -> SortedKeySet[_T, _OrderT]: ...
    @property
    def key(self) -> KeyFunc[_T, Any] | None: ...
    # We have to constrain value to be _T rather than object/Any
    def __contains__(self, value: _T) -> bool: ...  # type: ignore[override]
    @overload
    def __getitem__(self, index: int) -> _T: ...
    @overload
    def __getitem__(self, index: slice) -> list[_T]: ...
    def __delitem__(self, index: int | slice) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __lt__(self, other: Iterable[_T]) -> bool: ...
    def __gt__(self, other: Iterable[_T]) -> bool: ...
    def __le__(self, other: Iterable[_T]) -> bool: ...
    def __ge__(self, other: Iterable[_T]) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...
    def __reversed__(self) -> Iterator[_T]: ...
    def add(self, value: _T) -> None: ...
    def clear(self) -> None: ...
    def copy(self: Self) -> Self: ...
    def __copy__(self: Self) -> Self: ...
    def count(self, value: _T) -> int: ...
    def discard(self, value: _T) -> None: ...
    def pop(self, index: int = ...) -> _T: ...
    def remove(self, value: _T) -> None: ...
    # difference / intersection methods only subtract from our elements, so they
    # can accept Any.
    def difference(self, *iterables: Iterable[Any]) -> Self: ...
    def __sub__(self, iterable: Iterable[Any]) -> Self: ...
    def difference_update(self, *iterables: Iterable[Any]) -> Self: ...
    def __isub__(self, iterable: Iterable[Any]) -> Self: ...
    def intersection(self, *iterables: Iterable[Any]) -> Self: ...
    def __and__(self, iterable: Iterable[Any]) -> Self: ...
    def __rand__(self, iterable: Iterable[Any]) -> Self: ...
    def intersection_update(self, *iterables: Iterable[Any]) -> Self: ...
    def __iand__(self, iterable: Iterable[Any]) -> Self: ...
    def symmetric_difference(self, other: Iterable[_T]) -> Self: ...
    # The additive dunder methods are incompatible with the superclass because
    # we restrict operand to be T, rather than Any. (We can't compare
    # arbitrary values for order with T.)
    def __xor__(self, other: Iterable[_T]) -> Self: ...  # type: ignore[override]
    def __rxor__(self, other: Iterable[_T]) -> Self: ...
    def symmetric_difference_update(self, other: Iterable[_T]) -> Self: ...
    def __ixor__(self, other: Iterable[_T]) -> Self: ...  # type: ignore[override]
    def union(self, *iterables: Iterable[_T]) -> Self: ...
    def __or__(self, iterable: Iterable[_T]) -> Self: ...  # type: ignore[override]
    def __ror__(self, iterable: Iterable[_T]) -> Self: ...
    def update(self, *iterables: Iterable[_T]) -> Self: ...
    def __ior__(self, iterable: Iterable[_T]) -> Self: ...  # type: ignore[override]
    def __reduce__(
        self,
    ) -> tuple[type[SortedSet[_T]], AbstractSet[_T], Callable[[_T], Any]]: ...
    def bisect_left(self, value: _T) -> int: ...
    def bisect_right(self, value: _T) -> int: ...
    def bisect(self, value: _T) -> int: ...
    def islice(
        self,
        start: int | None = ...,
        stop: int | None = ...,
        reverse: bool = ...,
    ) -> Iterator[_T]: ...
    def irange(
        self,
        minimum: _T | None = ...,
        maximum: _T | None = ...,
        inclusive: tuple[bool, bool] = ...,
        reverse: bool = ...,
    ) -> Iterator[_T]: ...
    def index(
        self, value: _T, start: int | None = ..., stop: int | None = ...
    ) -> int: ...
    # Despite being named as a private method, this is documented in the API.
    def _reset(self, load: int) -> None: ...

# This type doesn't actually exist at runtime, but class SortedSet dynamically
# adds these methods to its instances if it has a key function.
class SortedKeySet(SortedSet[_T], Generic[_T, _OrderT]):
    # This is a stub-only type, it doesn't exist at runtime, so the
    # constructor returns Never to prevent creating instances directly.
    def __new__(
        cls,
        *,
        this_type_only_exists_as_a_type_annotation_it_cannot_be_created_directly: Never,
    ) -> Never: ...
    @property
    def key(self) -> KeyFunc[_T, _OrderT]: ...
    def irange_key(
        self,
        min_key: _OrderT | None = ...,
        max_key: _OrderT | None = ...,
        inclusive: tuple[bool, bool] = ...,
        reverse: bool = ...,
    ) -> Iterator[_T]: ...
    def bisect_key_left(self, key: _OrderT) -> int: ...
    def bisect_key_right(self, key: _OrderT) -> int: ...
    def bisect_key(self, key: _OrderT) -> int: ...
