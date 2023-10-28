from collections.abc import Hashable
from typing import Any, Protocol, TypeVar
from typing_extensions import TypeAlias

from _typeshed import SupportsDunderGT, SupportsDunderLT

_T_contra = TypeVar("_T_contra", contravariant=True)

class SupportsHashableAndDunderGT(
    Hashable, SupportsDunderGT[_T_contra], Protocol[_T_contra]
): ...
class SupportsHashableAndDunderLT(
    Hashable, SupportsDunderLT[_T_contra], Protocol[_T_contra]
): ...

SupportsHashableAndRichComparison: TypeAlias = (
    SupportsHashableAndDunderLT[Any] | SupportsHashableAndDunderGT[Any]
)

__all__ = ["SupportsHashableAndRichComparison"]
