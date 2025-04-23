# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

Version numbers track
[sortedcontainers versions](https://github.com/grantjenks/python-sortedcontainers/blob/master/HISTORY.rst).
The major and minor versions correspond to the same sortedcontainers major,
minor version; the patch version increments independently to release fixes.

## [Unreleased]

- Nothing yet

## [2.4.3] — 2025-04-23

### Fixed

- `SortedDict()` constructor:
  - Now allows `SortedDict(key_fn)` where `key_fn` accepts a non-string key.
    Previously this call was not matched by any overload, and an explicit
    `iterable` argument had to be provided. Thanks to [@tomtung] for reporting
    and helping to fix this. (issue [#6], fixed in [#11])
  - Now allows annotating the constructor explicitly with
    `SortedDict[xxx, yyy]()`. Previously mypy failed to handle this. ([#11])
- `SortedList()` constructor:
  - No longer accepts `SortedList(key_fn)`, which resulted in a type error at
    runtime. Calls without an iterable must be `SortedList(key=key_fn)`. (issue
    [#10], fixed in[#11])
  - Now allows annotating the constructor explicitly with `SortedList[xxx]()`.
    Previously mypy failed to handle this. ([#11])
- `SortedKeyList()` constructor:
  - No longer accepts `SortedKeyList(key_fn)`, which resulted in a type error at
    runtime. Calls without an iterable must be `SortedKeyList(key=key_fn)`.
    (issue [#10], fixed in[#11])
  - No longer accepts `SortedKeyList(key=None)`, which resulted in a type error
    at runtime. `key` is now required to not be None. (issue [#12], fixed
    in[#11])
- `SortedSet()` constructor:
  - No longer accepts `SortedSet(key_fn)`, which resulted in a type error at
    runtime. Calls without an iterable must be `SortedSet(key=key_fn)`. (issue
    [#10], fixed in[#11])
  - Now allows annotating the constructor explicitly with `SortedSet[xxx]()`.
    Previously mypy failed to handle this. ([#11])

[@tomtung]: https://github.com/tomtung
[#6]: https://github.com/h4l/sortedcontainers-stubs/issues/6
[#10]: https://github.com/h4l/sortedcontainers-stubs/issues/10
[#11]: https://github.com/h4l/sortedcontainers-stubs/issues/11
[#12]: https://github.com/h4l/sortedcontainers-stubs/issues/12

## [2.4.2] — 2023-10-28

### Fixed

- Using the SortedList (and the other) types as a function that creates an
  instance of the type works in pyright now. ([#3], [#4])

[#3]: https://github.com/h4l/sortedcontainers-stubs/issues/3
[#4]: https://github.com/h4l/sortedcontainers-stubs/issues/4

### Changed

- Because of the fix to allow pyright to allow using the types as functions, the
  constructors with no arguments had to be widened to permit assignment to
  non-comparable/hashable types. The result is that it's unfortunately not a
  type error to do something like `sl: SortedList[type] = SortedList()` even
  though subsequently adding multiple values to this list will fail at runtime.

  It doesn't seem to be possible to type the signature of `__new__` to constrain
  `SortedList()` to only allow comparable element types in a standard way (mypy
  supported the previous method which worked, but other checkers don't).

- The signature definition of SortedDict.setdefault was restructured to satisfy
  pyright, but the effect of the signature itself remains the same.

- pyright runs in CI now

## [2.4.1] — 2023-10-10

### Fixed

- Add `__all__` to define the explicit exports of `sortedcontainers.sorteddict`
- Remove an internal `TypeVar` from the `__all__` of
  `sortedcontainers.sortedlist`

## [2.4.0] — 2023-10-09

### Added

- Stubs now published as a standalone package from this separate repo.
- Tests for stubs using `pytest-mypy-plugins`
- Stub-only types for `SortedKeySet` and `SortedKeyDict` which describe the
  differences that apply when key functions are used (mirrors `SortedKeyList`).

### Changed

- Constructors return types that reflect the API differences that apply when key
  functions are used
- The restrictions on key/value types are enforced by the types. Keys/values
  need to be hashable and or comparable, or unrestricted, according to the
  collection type and whether a key function is used.
- Unsafe operations that would cause type errors at runtime are disallowed. For
  example, taking a union of two sets with different element types, that could
  cause a type error due to types not being orderable with respect to each
  other.

### Fixed

- A few minor typos, missing methods etc.

### Removed

- Most private methods, except `_reset()` (which is documented and used to
  change the SortedList load factor for performance reasons).

## Unreleased — [PR to sortedcontainers proposing stubs]

[PR to sortedcontainers proposing stubs]:
  https://github.com/grantjenks/python-sortedcontainers/pull/107

Created by Martin Larralde with review from several people in the PR.

[unreleased]:
  https://github.com/h4l/sortedcontainers-stubs/compare/v2.4.1...HEAD
[2.4.3]: https://github.com/h4l/sortedcontainers-stubs/compare/v2.4.2...2.4.3
[2.4.2]: https://github.com/h4l/sortedcontainers-stubs/compare/v2.4.1...2.4.2
[2.4.1]: https://github.com/h4l/sortedcontainers-stubs/compare/v2.4.0...2.4.1
[2.4.0]: https://github.com/h4l/sortedcontainers-stubs/releases/tag/v2.4.0
