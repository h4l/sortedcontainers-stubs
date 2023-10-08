from collections.abc import Hashable
from typing import Any, Protocol
from typing_extensions import TypeAlias

from _typeshed import SupportsDunderGT, SupportsDunderLT, _T_contra  # noqa: F401

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
